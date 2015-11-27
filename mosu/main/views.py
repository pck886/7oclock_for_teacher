# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
import math
from mosu.docs.models import Question, QuestionUnit1, QuestionUnit2, QuestionUnit3, QuestionUnit4
from mosu.home.models import get_or_none, Union, Group, School, UnionUser, GroupUser
from mosu.main.models import TestPaper, TestPaperQuestion, TestPaperForm

def main(request):
    if request.user.id is None:
        return HttpResponseRedirect("/home/")

    this_union = get_or_none(Union,id=request.GET.get("id",0))

    union_list = []

    for u in Union.objects.filter(user=request.user,is_active=True):
        union_list.append(u.id)
    for u in Group.objects.filter(unionuser__user=request.user,is_active=True):
        union_list.append(u.union.id)

    unions = Union.objects.filter(id__in=union_list,is_active=True).order_by("is_paid")

    if this_union == None :
        this_union = unions[0]

    context = {
        'user':request.user,
        'unions':unions,
        'this_union':this_union,
        'appname':'main'
    }
    return render(request, 'main.html', context)

def main_dashboard(request):
    union = get_or_none(Union, id=request.POST.get('union_id',0))
    context = {
        'user': request.user,
        'union':union,
    }
    return render(request, 'main_dashboard.html', context)

def main_dashboard_union(request):
    union = get_or_none(Union, id=request.POST.get('union_id',0))
    user = request.user

    testpapers = TestPaper.objects.filter(union=union,user=user).order_by("-id")

    context = {
        'user': user,
        'union':union,
        'testpapers':testpapers
    }
    return render(request, 'main_dashboard_union.html', context)

def main_inventory(request):
    q = request.GET.get('q', '')
    union = get_or_none(Union, id=request.POST.get('union_id',0))

    testpapers = TestPaper.objects.filter(user=request.user,union=union,title__icontains=q,is_shown=True).order_by("-id")

    context = {
        'user': request.user,
        'query':q,
        'union':union,
        'testpapers':testpapers
    }
    return render(request, 'main_inventory.html', context)

def main_select(request):
    arr = []
    q = request.GET.get('q','')

    u1 = get_or_none(QuestionUnit1,id=request.GET.get('unit1',0))
    u2 = get_or_none(QuestionUnit2,id=request.GET.get('unit2',0))
    u3 = get_or_none(QuestionUnit3,id=request.GET.get('unit3',0))
    u4 = get_or_none(QuestionUnit4,id=request.GET.get('unit4',0))
    unit1, unit2, unit3, unit4 = None, None, None, None


    unit1 = QuestionUnit1.objects.filter(is_active=True)
    query = None

    if u1 :
        unit2 = QuestionUnit2.objects.filter(unit=u1,is_active=True)
        query = None
        if u2 :
            unit3 = QuestionUnit3.objects.filter(unit=u2,is_active=True)
            query = Q(unit__unit__unit__unit=u2)
            if u3 :
                unit4 = QuestionUnit4.objects.filter(unit=u3,is_active=True)
                query = query&Q(unit__unit__unit=u3)
                if u4 :
                    query = query&Q(unit__unit=u4)

    questions = []
    if query :
        questions = Question.objects.filter(query).values('unit').annotate(count=Count('unit'))

    for question in questions:
        tmp = Question.objects.filter(unit=question['unit'])
        if tmp :
            type_0 = tmp.filter(unit=tmp[0].unit, type=0)
            type_1 = tmp.filter(unit=tmp[0].unit, type=1)
            arr.append({'count':question['count'],'unit':tmp[0].unit,'element':tmp[0],'type_0':type_0,'type_1':type_1})

    context = {
        'user': request.user,
        'query':q,
        'unit1':unit1,'unit2':unit2,'unit3':unit3,'unit4':unit4,
        'u1':u1,'u2':u2,'u3':u3,'u4':u4,
        'questions':arr
    }
    return render(request, 'main_select.html', context)

def main_select_post_maketest(request):
    test_title = request.POST.get('title')
    union = get_or_none(Union,id=int(request.POST.get('union_id',0)))
    tpid = request.POST.get('tpid')
    str_questions = request.POST.get('questions')
    purpose = int(request.POST.get('purpose', 0))

    if tpid :
        tpid = get_or_none(TestPaper,id=tpid)
        tp = TestPaper.objects.create(form=tpid.form, user=request.user, title=test_title, union=union, purpose=purpose, is_exported=False)
        if tp :
            for question in reversed(tpid.get_questions()) :
                TestPaperQuestion.objects.create(testpaper=tp,question=question)
    else :
        arr_questions = str_questions.split(',')
        arr_questions = reversed(arr_questions)

        form = get_or_none(TestPaperForm, id=1)

        tp = TestPaper.objects.create(form=form, user=request.user, title=test_title, union=union, purpose=purpose, is_exported=False)

        if tp :
            for question in arr_questions :
                TestPaperQuestion.objects.create(testpaper=tp,question=get_or_none(Question,id=question))

    return main_testpaper(request,tp=tp)

def main_select_post_maketest_chkname(request):
    keyword = request.POST.get('keyword')
    tp = TestPaper.objects.filter(title=keyword,is_shown=True,user=request.user)
    if tp or keyword == '' : return HttpResponse(1)
    return HttpResponse(0)

def main_testpaper(request, tp=None):
    if tp == None : tp = get_or_none(TestPaper,id=int(request.GET.get('tpid',0)))
    groups = Group.objects.filter(union=tp.union,unionuser__user=request.user).order_by("id")

    pages = []
    n = 0

    for i in range(0,int(math.ceil((len(tp.get_questions())/6.0)))):
        tmp = []
        for j in range(0,6):
            try:
                tmp.append(tp.get_questions()[n])
                n = n+1
            except Exception as e:
                break
        pages.append(tmp)

    explain_pages = []
    explain_page = []
    explain_lines = []
    explain_questions = []

    tp_questions = tp.get_questions()
    page_h = 280

    line_h = 0
    qno = 0
    for question in tp_questions:
        qno = qno + 1
        question.no = qno
        if question.explain :
            img_h =(question.explain.height*155)/1010
            line_h = line_h + img_h
            if len(explain_lines) > 2 : page_h = 330
            if line_h >= page_h :
                line_h = img_h
                explain_lines.append(explain_questions[:])
                explain_questions = []
            explain_questions.append(question)

    if explain_questions :
        explain_lines.append(explain_questions[:])

    for line in explain_lines:
        explain_page.append(line)
        if len(explain_page) > 1 :
            explain_pages.append(explain_page[:])
            explain_page = []

    if explain_page :
        explain_page.append([])
        explain_pages.append(explain_page[:])

    context = {
        'user': request.user,
        'pages':pages,
        'testpaper':tp,
        "explain_pages":explain_pages,
        'groups':groups,
        'mode':'main_testpaper'
    }
    return render(request, 'main_testpaper.html', context)

def main_testpaper_modify(request):
    arr = []
    q = request.GET.get('q','')
    tp = get_or_none(TestPaper,id=request.GET.get('tpid'))

    u1 = get_or_none(QuestionUnit1,id=request.GET.get('unit1',0))
    u2 = get_or_none(QuestionUnit2,id=request.GET.get('unit2',0))
    u3 = get_or_none(QuestionUnit3,id=request.GET.get('unit3',0))
    u4 = get_or_none(QuestionUnit4,id=request.GET.get('unit4',0))
    unit1, unit2, unit3, unit4 = None, None, None, None


    unit1 = QuestionUnit1.objects.filter(is_active=True)
    query = None

    if u1 :
        unit2 = QuestionUnit2.objects.filter(unit=u1,is_active=True)
        query = None
        if u2 :
            unit3 = QuestionUnit3.objects.filter(unit=u2,is_active=True)
            query = Q(unit__unit__unit__unit=u2)
            if u3 :
                unit4 = QuestionUnit4.objects.filter(unit=u3,is_active=True)
                query = query&Q(unit__unit__unit=u3)
                if u4 :
                    query = query&Q(unit__unit=u4)

    questions = []
    if query :
        questions = Question.objects.filter(query).values('unit').annotate(count=Count('unit'))

    for question in questions:
        tmp = Question.objects.filter(unit=question['unit'])
        if tmp :
            type_0 = tmp.filter(unit=tmp[0].unit, type=0)
            type_1 = tmp.filter(unit=tmp[0].unit, type=1)
            arr.append({'count':question['count'],'unit':tmp[0].unit,'element':tmp[0],'type_0':type_0,'type_1':type_1})

    context = {
        'user': request.user,
        'query':q,
        'unit1':unit1,'unit2':unit2,'unit3':unit3,'unit4':unit4,
        'u1':u1,'u2':u2,'u3':u3,'u4':u4,
        'questions':arr,
        'testpaper':tp
    }
    return render(request, 'main_testpaper_modify.html', context)

def main_testpaper_form(request):
    q = request.GET.get('q','')
    tp = get_or_none(TestPaper,id=request.GET.get('tpid'))

    forms = TestPaperForm.objects.filter((Q(union=None)|Q(union=tp.union))&Q(title__icontains=q))

    context = {
        'user': request.user,
        'query':q,
        'forms':forms,
        'testpaper':tp
    }
    return render(request, 'main_testpaper_form.html', context)

def main_testpaper_similar(request, tp=None):
    if tp == None : tp = get_or_none(TestPaper,id=int(request.GET.get('tpid',0)))

    pages = []
    n = 0

    for i in range(0,int(math.ceil((len(tp.get_questions())/6.0)))):
        tmp = []
        for j in range(0,6):
            try:
                tmp.append(tp.get_questions()[n])
                n = n+1
            except Exception as e:
                break
        pages.append(tmp)

    context = {
        'user': request.user,
        'pages':pages,
        'testpaper':tp,
        'mode':'main_testpaper_similar'
    }
    return render(request, 'main_testpaper.html', context)

def main_testpaper_post_modify(request):
    tp = get_or_none(TestPaper,id=int(request.POST.get('tpid',0)))
    str_questions = request.POST.get('questions')
    arr_questions = str_questions.split(',')
    arr_questions = reversed(arr_questions)

    if tp :
        tpqs = TestPaperQuestion.objects.filter(testpaper=tp)
        for tpq in tpqs :
            tpq.delete()
        for question in arr_questions :
            TestPaperQuestion.objects.create(testpaper=tp,question=get_or_none(Question,id=question))

    return main_testpaper(request,tp=tp)

def main_testpaper_post_similar(request):
    tp = get_or_none(TestPaper,id=int(request.POST.get('tpid',0)))
    str_questions = request.POST.get('question_ids')
    arr_questions = str_questions.split(',')
    arr_questions = reversed(arr_questions)

    if tp :
        tpqs = TestPaperQuestion.objects.filter(testpaper=tp)
        for tpq in tpqs :
            tpq.delete()
        for question_id in arr_questions:
            question = get_or_none(Question,id=question_id)
            if question : TestPaperQuestion.objects.create(testpaper=tp,question=question)

    return main_testpaper(request,tp=tp)

def main_testpaper_post_delete(request):
    tp = get_or_none(TestPaper,id=int(request.GET.get('tpid',0)))
    if tp.is_exported :
        tp.is_shown = False
        tp.save()
    else :
        tp.delete()
    return HttpResponseRedirect("/inventory/")

def main_testpaper_post_form(request):
    tp = get_or_none(TestPaper,id=int(request.POST.get('tpid',0)))
    form = get_or_none(TestPaperForm,id=int(request.POST.get('fid',0)))

    tp.form = form
    tp.save()

    return main_testpaper(request,tp=tp)

def main_testpaper_post_group(request):
    tp = get_or_none(TestPaper,id=int(request.POST.get('tpid',0)))
    str_group = request.POST.get('groups',None)
    is_exported = request.POST.get('is_exported',None)

    if is_exported :
        tp.is_exported = True
        tp.save()

    if str_group :
        arr_group = str_group.split(',')
        tp.groups.clear()
        for group in arr_group:
            sy = get_or_none(Group,id=int(group))
            if sy : tp.groups.add(sy)
        tp.save()

    groups = Group.objects.filter(union=tp.union).order_by('id')

    context = {
        'user': request.user,
        'testpaper':tp,
        'groups':groups
    }
    return render(request, 'main_testpaper_group.html', context)

def main_progress(request):

    q = request.GET.get('q','')
    select_year = int(request.GET.get('year',0))

    if select_year != 0 : testpapers = TestPaper.objects.filter(user__id=1,title__icontains=q,year=select_year).order_by("-id")
    else : testpapers = TestPaper.objects.filter(user__id=1,title__icontains=q).order_by("-id")

    context = {
        'user': request.user,
        'query':q,
        'select_year':str(select_year),
        'testpapers':testpapers
    }
    return render(request, 'main_progress.html', context)

def main_groupuser(request):
    q = request.GET.get('q', '')
    union = get_or_none(Union, id=request.POST.get('union_id',0))
    this_group = get_or_none(Group,id=int(request.GET.get("id",0)))

    groups = Group.objects.filter(union=union).order_by('id')

    if this_group == None : this_group = groups[0]

    context = {
        'user': request.user,
        'query':q,
        'union':union,
        'this_group':this_group,
        'groups':groups
    }
    return render(request, 'main_groupuser.html', context)

def main_groupuser_post_groupuser_move(request):
    user = get_or_none(User,id=int(request.POST.get('uid',0)))
    union = get_or_none(Union, id=request.POST.get('union_id',0))
    unionuser = get_or_none(UnionUser, union=union, user=user)
    this_group = get_or_none(Group,id=int(request.GET.get("id",0)))
    if this_group.unionuser != unionuser :
        gu, created = GroupUser.objects.get_or_create(unionuser=unionuser,group=this_group)
        if gu :
            gu.in_group = True
            gu.is_active = True
            gu.save()
    return main_groupuser(request)

def main_groupuser_post_groupuser_delete(request):
    user = get_or_none(User,id=int(request.POST.get('uid',0)))
    union = get_or_none(Union, id=request.POST.get('union_id',0))
    unionuser = get_or_none(UnionUser, union=union, user=user)
    this_group = get_or_none(Group,id=int(request.GET.get("id",0)))
    if unionuser :
        if user != request.user :
            if this_group.unionuser == unionuser :
                unionuser_new = get_or_none(UnionUser,user=union.user,union=union)
                this_group.unionuser = unionuser_new
                this_group.save()
                gu = get_or_none(GroupUser,unionuser=unionuser_new,group=this_group)
                if gu : gu.delete()
            unionuser.delete()
    return main_groupuser(request)

def main_groupuser_post_groupuser_cancel(request):
    user = get_or_none(User,id=int(request.POST.get('uid',0)))
    union = get_or_none(Union, id=request.POST.get('union_id',0))
    unionuser = get_or_none(UnionUser, union=union, user=user)
    this_group = get_or_none(Group,id=int(request.GET.get("id",0)))
    if unionuser :
        gu = get_or_none(GroupUser,unionuser=unionuser,group=this_group)
        if gu :
            gu.delete()
    return main_groupuser(request)

def main_groupuser_post_groupuser_teacher(request):
    user = get_or_none(User,id=int(request.POST.get('uid',0)))
    union = get_or_none(Union, id=request.POST.get('union_id',0))
    unionuser = get_or_none(UnionUser, union=union, user=user)
    this_group = get_or_none(Group,id=int(request.GET.get("id",0)))
    if this_group.unionuser != unionuser :
        gu = get_or_none(GroupUser,unionuser=unionuser,group=this_group)
        if gu :
            gu_new, created = GroupUser.objects.get_or_create(unionuser=this_group.unionuser,group=this_group)
            if gu_new :
                gu_new.in_group = True
                gu_new.is_active = True
                gu_new.save()
                this_group.unionuser = unionuser
                this_group.save()
                gu.delete()
    return main_groupuser(request)

def main_mypage(request):
    context = {
        'user': request.user
    }
    return render(request, 'main_mypage.html', context)

def main_mypage_post_group_change(request):
    user = request.user
    Group = get_or_none(Group,id=int(request.POST.get('sid',0)))
    if Group :
        user.profile.group = Group
        user.profile.save()
        return HttpResponse("True")
    return HttpResponse("False")

def main_mypage_post_pw_change(request):
    pw_now = request.POST.get("pw_now","")
    pw_c = request.POST.get("pw_c","")

    user = authenticate(username=request.user.username, password=pw_now)

    if user :
        if pw_c :
            user.set_password(pw_c)
            user.save()
        return HttpResponse("True")
    return HttpResponse("False")

def main_mypage_post_info_change(request):
    user = request.user
    first_name = request.POST.get("first_name","")
    email = request.POST.get("email","")
    phone = request.POST.get("phone","")
    gender = request.POST.get("gender","")

    if first_name : user.first_name = first_name
    if email : user.email = email
    if phone : user.profile.phone = phone
    if gender : user.profile.gender = gender
    user.save()
    user.profile.save()

    return HttpResponse("True")

def main_dashboard_post_school_register(request):
    user = request.user
    grade = request.POST.get("grade","")
    school_id = request.POST.get("school_id",0)

    if school_id:
        user.profile.school = get_or_none(School, id=school_id)
    if grade :
        if user.profile.school :user.profile.year = grade[-1]
        else : user.profile.year = 0
        user.profile.grade_code = grade

    user.profile.save()

    union_obj, err = Union.objects.get_or_create(
        user=user,
        title=u"%s's 임시소속"%user.first_name,
        address="",
        phone=user.profile.phone,
        icon="/static/img/main/icon_union_tmp.png",
        is_paid=False,
        is_active=True
    )

    unionuser_obj, err = UnionUser.objects.get_or_create(
        union = union_obj,
        user = user,
        is_active = True
    )

    Group.objects.get_or_create(
        union = union_obj,
        unionuser = unionuser_obj,
        title = u"무료그룹1",
        is_paid=False,
        is_active=True
    )

    return HttpResponse("True")