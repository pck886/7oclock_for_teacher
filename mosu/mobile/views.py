# -*- coding: utf-8 -*-
import json
import operator
from tempfile import NamedTemporaryFile
import urllib2

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.base import ContentFile, File
from django.db.models import Q, Count
from django.http import HttpResponse


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import sys
from mosu.docs.models import QuestionUnit1, QuestionUnit2, QuestionUnit3, QuestionUnit4, QuestionUnit5, Question, \
    QuestionFeedback
from mosu.home.models import get_or_none, Group, UserProfile, Group, School, Union, UnionUser
from mosu.main.models import TestPaper, TestPaperQuestion, TestPaperSubmit
from mosu.mobile.models import QuestionInventory

def get_user(request):
    userid = request.GET.get("user_id")
    password = request.GET.get("password")
    login_from = int(request.GET.get("login_from",0))
    if login_from != 0 :
        password = "%d_%s"%(login_from,password)

    user = authenticate(username=userid, password=password)
    if user.id :
        arr = [{
            'id':user.id,
        }]
        return HttpResponse(json.dumps(arr, default=date_handler), content_type="application/json")
    else:
        return HttpResponse(json.dumps([{}], default=date_handler), content_type="application/json")
    return HttpResponse(json.dumps([{}], default=date_handler), content_type="application/json")

def get_user_info(request):
    uid = int(request.GET.get("uid",0))
    user = get_or_none(User,id=uid)
    if user.id :
        shool_id, school_name, grade_code = 0, "", ""
        if user.profile.school :
            shool_id = user.profile.school.id
            school_name = user.profile.school.name
        if user.profile.grade_code:
            grade_code = user.profile.grade_code
        arr = [{
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'first_name':user.first_name,
            'shool_id':"%d"%shool_id,
            'school_name':"%s"%school_name,
            'school_year':"%d"%user.profile.year,
            'login_from':user.profile.login_from,
            'grade_code':"%s"%grade_code,
            'src':user.profile.get_src(),
            'phone':user.profile.phone,
            'gender':user.profile.get_gender()
        }]
        return HttpResponse(json.dumps(arr, default=date_handler), content_type="application/json")
    else:
        return HttpResponse(json.dumps([{}], default=date_handler), content_type="application/json")
    return HttpResponse(json.dumps([{}], default=date_handler), content_type="application/json")

def get_school_name(request):
    q = request.GET.get('q')
    schools = list(School.objects.filter(name__contains=q)[:20].values())
    return HttpResponse(json.dumps(schools, default=date_handler), content_type="application/json")

def set_user(request):
    login_from = int(request.GET.get("login_from", 0))
    user_id = request.GET.get("user_id")
    password = request.GET.get("password")
    user_name = request.GET.get("user_name","")
    user_email = request.GET.get("user_email","@")
    phone = request.GET.get("user_phone","-")
    gender = int(request.GET.get("user_gender",0))
    img_url = request.GET.get("img_url","")

    profile_img = None
    if login_from != 0 :
        password = "%d_%s"%(login_from,password)
        if img_url :
            profile_img = NamedTemporaryFile(delete=True)
            profile_img.write(urllib2.urlopen(img_url).read())
            profile_img.flush()

    user = User.objects.create_user(username=user_id,password=password,email=user_email,first_name=user_name)
    if user :
        profile = UserProfile.objects.create(user=user,gender=gender,login_from=login_from,phone=phone)
        if profile_img : profile.src.save("%s.jpg"%user_id, File(profile_img))
        user = authenticate(username=user_id, password=password)
        if user :
            arr = [{
                'id':user.id
            }]
            return HttpResponse(json.dumps(arr, default=date_handler), content_type="application/json")
    return HttpResponse(json.dumps([{}], default=date_handler), content_type="application/json")

# def set_user_profilepic(request):
#     pictures = request.FILES.getlist("picture")
#     uid = int(request.GET.get("uid",0))
#     user = get_or_none(User,id=uid)
#     for picture in pictures:
#         user.profile.src.save("%s.jpg"%picture.name, ContentFile(picture.read()))
#     return get_user_info(request)
#
# def set_user_passwd(request):
#     user_login = get_or_none(User,id=int(request.GET.get("uid",0)))
#     pw_now = request.POST.get("pw_now","")
#     pw_new = request.POST.get("pw_new","")
#
#     user = authenticate(username=user_login.username, password=pw_now)
#
#     if user :
#         if pw_new :
#             user.set_password(pw_new)
#             user.save()
#             return HttpResponse("True", status=200)
#     return HttpResponse("False", status=401)
#
def set_user_info(request):
    user = get_or_none(User,id=int(request.GET.get("uid",0)))
    str_name = request.POST.get("name","")
    str_email = request.POST.get("email","")
    str_phone = request.POST.get("phone","")
    str_gender = request.POST.get("gender",0)

    if user :
        user.first_name = str_name
        user.email = str_email
        user.profile.phone = str_phone
        user.profile.gender = str_gender
        user.save()
        user.profile.save()
        return HttpResponse("True", status=200)
    return HttpResponse("False", status=401)

def set_school_info(request):
    user = get_or_none(User,id=int(request.POST.get("uid",0)))
    grade = request.POST.get("grade","")
    school_id = request.POST.get("school_id",0)

    if user :
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
            icon="/static/img/main/union_tmp.png",
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
        return HttpResponse("True", status=200)
    return HttpResponse("False", status=401)

# def get_question_unit(request):
#     u1 = int(request.GET.get('u1',0))
#     u2 = int(request.GET.get('u2',0))
#     u3 = int(request.GET.get('u3',0))
#     u4 = int(request.GET.get('u4',0))
#
#     arr = list(QuestionUnit1.objects.filter(is_active=True).values())
#     if u1 != 0 :
#         arr = list(QuestionUnit2.objects.filter(unit__id=u1,is_active=True).values())
#     if u2 != 0 :
#         arr = list(QuestionUnit3.objects.filter(unit__id=u2,is_active=True).values())
#     if u3 != 0 :
#         arr = list(QuestionUnit4.objects.filter(unit__id=u3,is_active=True).values())
#     if u4 != 0 :
#         arr = list(QuestionUnit5.objects.filter(unit__id=u4,is_active=True).values())
#     return HttpResponse(json.dumps(arr, default=date_handler), content_type="application/json")
#
# def get_question_list(request):
#     q = request.GET.get("q","")
#     limit = request.GET.get('limit')
#
#     u1 = get_or_none(QuestionUnit1,id=request.GET.get('u1'))
#     u2 = get_or_none(QuestionUnit2,id=request.GET.get('u2'))
#     u3 = get_or_none(QuestionUnit3,id=request.GET.get('u3'))
#     u4 = get_or_none(QuestionUnit4,id=request.GET.get('u4'))
#     u5 = get_or_none(QuestionUnit5,id=request.GET.get('u5'))
#
#     q = q.split()
#     if q : query = reduce(operator.and_, (Q(keyword__icontains = item) for item in q))
#     else : query = Q()
#
#     if u5 : query = query&Q(unit=u5)
#     elif u4 : query = query&Q(unit__unit=u4)
#     elif u3 : query = query&Q(unit__unit__unit=u3)
#     elif u2 : query = query&Q(unit__unit__unit__unit=u2)
#     elif u1 : query = query&Q(unit__unit__unit__unit__unit=u1)
#
#     if limit :
#         limit = limit.split(':')
#         limit = [int(item) for item in limit]
#         questions = Question.objects.filter(query)[limit[0]:limit[1]]
#     else :
#         questions = Question.objects.filter(query)
#
#     arr = []
#
#     for question in questions[0:1] :
#         if question :
#             if question.src : src = question.src.url
#             else : src = ""
#             if question.explain : explain = question.explain.url
#             else : explain = ""
#             arr.append({
#                 "id":question.id,"type":question.type,"unit":question.unit.id,"unit_title":question.unit.title,"src":src,"explain":explain,"keyword":question.keyword,
#                 "video":question.video,"answer":question.answer,"is_active":question.is_active,"date_created":"%s"%set_date(question.date_created)
#             })
#
#     return HttpResponse(json.dumps(arr), content_type="application/json")
#
# def get_question_search(request):
#     query = request.GET.get("q","")
#     query = query.split()
#     if query : query = reduce(operator.and_, (Q(keyword__icontains = item) for item in query))
#     else : query = Q()
#
#     questions_all = Question.objects.filter(query)
#
#     arr_u1 = []
#
#     questions_u1 = questions_all.values('unit__unit__unit__unit__unit').annotate(count=Count('unit__unit__unit__unit__unit'))
#     for q_u1 in questions_u1:
#         questions_unit1 = questions_all.filter(unit__unit__unit__unit__unit=q_u1["unit__unit__unit__unit__unit"]
#                                                ,unit__unit__unit__unit__unit__is_active=True
#                                                ,unit__unit__unit__unit__is_active=True
#                                                ,unit__unit__unit__is_active=True
#                                                ,unit__unit__is_active=True
#                                                ,unit__is_active=True
#                                                ,is_active=True)
#         if questions_unit1 :
#             questions_u2 = questions_all.values('unit__unit__unit__unit').annotate(count=Count('unit__unit__unit__unit'))
#             arr_u2 = []
#             for q_u2 in questions_u2:
#                 questions_unit2 = questions_all.filter(unit__unit__unit__unit=q_u2["unit__unit__unit__unit"])[:2]
#                 if questions_unit2 :
#                     arr_questions = []
#                     for question in questions_unit2 :
#                         arr_questions.append({
#                             "id":question.id,"type":question.type,"unit_id":question.unit.id,"unit":question.unit.title,"src":question.src.url,"explain":question.explain.url,"keyword":question.keyword,
#                             "video":question.video,"answer":question.answer,"is_active":question.is_active,"date_created":"%s"%set_date(question.date_created)
#                         })
#                     arr_u2.append({"title":questions_unit2[0].unit.unit.unit.unit.title,"quetions":arr_questions})
#             arr_u1.append({"title":questions_unit1[0].unit.unit.unit.unit.unit.title,"unit":arr_u2})
#
#     return HttpResponse(json.dumps(arr_u1), content_type="application/json")
#
# def get_question_feedback(request):
#     user = get_or_none(User,id=request.GET.get('uid',0))
#     question = get_or_none(Question,id=request.GET.get('qid',0))
#     feedback = get_or_none(QuestionFeedback,user=user,question=question)
#     if feedback :
#         return HttpResponse(json.dumps([{'question':feedback.question.id, 'is_good':feedback.is_good}], default=date_handler), content_type="application/json")
#     return HttpResponse(json.dumps([{}], default=date_handler), content_type="application/json")
#
# def set_question_feedback(request):
#     user = get_or_none(User,id=request.GET.get('uid',0))
#     question = get_or_none(Question,id=request.GET.get('qid',0))
#     is_good = request.GET.get('is_good','1')
#
#     feedback, created = QuestionFeedback.objects.get_or_create(question=question,user=user)
#
#     if is_good == '1' :
#         is_good = True
#     elif is_good == '-1' :
#         feedback.delete()
#         return HttpResponse(json.dumps([{}], default=date_handler), content_type="application/json")
#     else :
#         is_good = False
#
#     if feedback :
#         feedback.is_good = is_good
#         feedback.save()
#         return HttpResponse(json.dumps([{'question':feedback.question.id, 'is_good':feedback.is_good}], default=date_handler), content_type="application/json")
#     return HttpResponse(json.dumps([{}], default=date_handler), content_type="application/json")
#
# def get_testpaper_list(request):
#     user = get_or_none(User,id=request.GET.get("uid",0))
#
#     arr = []
#
#     testpapers = TestPaper.objects.filter(groups__year=user.profile.group.year,groups__group=user.profile.group.group,Group=user.profile.group.group,is_shown=True,is_exported=True).order_by('-id')
#
#     for testpaper in testpapers :
#         arr.append({'id':testpaper.id, 'title':testpaper.title, 'year':testpaper.year,
#                     'date':set_date(testpaper.date_created), 'Group_name':testpaper.group.title, 'user':testpaper.user.first_name,
#                     "purpose":testpaper.get_purpose(),"question_len":len(testpaper.get_questions())})
#
#     return HttpResponse(json.dumps(arr, default=date_handler), content_type="application/json")
#
# def get_testpaper_question_list(request):
#     testpaper = get_or_none(TestPaper,id=request.GET.get('tpid',0))
#     user = get_or_none(User,id=request.GET.get('uid',0))
#     limit = request.GET.get('limit','')
#
#     arr = []
#
#     if limit == '':
#         tpqs = TestPaperQuestion.objects.filter(testpaper_id=testpaper).order_by('-id')
#     else :
#         limit = limit.split(':')
#         if limit : limit = [int(item) for item in limit]
#         else : limit = [0,0]
#         tpqs = TestPaperQuestion.objects.filter(testpaper_id=testpaper).order_by('-id')[limit[0]:limit[1]]
#
#     if testpaper.get_submit(user) : is_solved = 1
#     else : is_solved = 0
#
#     for tpq in tpqs :
#         if tpq.question :
#             arr.append({
#                 "id":tpq.question.id,"type":tpq.question.type,"unit":tpq.question.unit.id,"unit_title":tpq.question.unit.title,
#                 "src":tpq.question.src.url,"explain":tpq.question.explain.url,"keyword":tpq.question.keyword,
#                 "video":tpq.question.video,"answer":tpq.question.answer,"is_active":tpq.question.is_active,
#                 "items":tpq.question.items,"answer_mobile":tpq.question.answer_mobile,"is_solved":is_solved,
#                 "purpose":testpaper.purpose,"date_created":"%s"%set_date(tpq.question.date_created),
#             })
#
#     return HttpResponse(json.dumps(arr), content_type="application/json")
#
# def set_invenroty(request):
#     user = get_or_none(User,id=request.GET.get('uid',0))
#     question = get_or_none(Question,id=request.GET.get('qid',0))
#
#     inventory = get_or_none(QuestionInventory, user=user,question=question)
#
#     if inventory :
#         inventory.delete()
#         return HttpResponse(json.dumps([{}], default=date_handler), content_type="application/json")
#     else :
#         inventory, created = QuestionInventory.objects.get_or_create(user=user,question=question)
#         return HttpResponse(json.dumps([{'question':inventory.question.id}], default=date_handler), content_type="application/json")
#
# def get_invenroty(request):
#     user = get_or_none(User,id=request.GET.get('uid',0))
#     question = get_or_none(Question,id=request.GET.get('qid',0))
#
#     inventory = get_or_none(QuestionInventory, user=user,question=question)
#
#     if inventory : return HttpResponse(json.dumps([{'question':inventory.question.id}], default=date_handler), content_type="application/json")
#     else : return HttpResponse(json.dumps([{}], default=date_handler), content_type="application/json")
#
#
# def get_inventory_list(request):
#     user = get_or_none(User,id=request.GET.get('uid',0))
#     units = QuestionInventory.objects.filter(user=user).values('question__unit__unit__unit__unit').annotate(count=Count('question__unit__unit__unit__unit'))
#
#     arr = []
#
#     for unit in units:
#         unit2 = get_or_none(QuestionUnit2,id=unit["question__unit__unit__unit__unit"], is_active=True)
#         if unit2 :
#             arr.append({"id":unit2.id,"title":unit2.title,'count':unit['count']})
#
#     return HttpResponse(json.dumps(arr), content_type="application/json")
#
# def get_inventory_question_list(request):
#     user = get_or_none(User,id=request.GET.get('uid',0))
#     unit_id = request.GET.get('unit_id',0)
#     limit = request.GET.get('limit','')
#
#     arr = []
#
#     if limit == '':
#         qis = QuestionInventory.objects.filter(user=user,question__unit__unit__unit__unit__id=unit_id).order_by('-id')
#     else :
#         limit = limit.split(':')
#         if limit : limit = [int(item) for item in limit]
#         else : limit = [0,0]
#         qis = QuestionInventory.objects.filter(user=user,question__unit__unit__unit__unit__id=unit_id).order_by('-id')[limit[0]:limit[1]]
#
#     for qi in qis :
#         if qi.question :
#             arr.append({
#                 "id":qi.question.id,"type":qi.question.type,"unit_id":qi.question.unit.id,"unit":qi.question.unit.title,"unit_title":qi.question.unit.title,"src":qi.question.src.url,"explain":qi.question.explain.url,"keyword":qi.question.keyword,
#                 "video":qi.question.video,"answer":qi.question.answer,"is_active":qi.question.is_active,"date_created":"%s"%set_date(qi.question.date_created)
#             })
#
#     return HttpResponse(json.dumps(arr), content_type="application/json")
#
# def get_testpaper_submit(request):
#     user = get_or_none(User,id=request.GET.get("uid",0))
#     testpaper = get_or_none(TestPaper,id=request.GET.get("tpid",0))
#     testpaper_user = TestPaperSubmit.objects.filter(testpaper=testpaper,user__profile__Group=user.profile.group).values('user').annotate(Count('user'))
#
#     myrank = 0
#
#     if testpaper_user :
#         arr_rank = []
#         for tp_user in testpaper_user :
#             tu = get_or_none(User,id=tp_user['user'])
#             arr_rank.append({"uid":tu.id,"username":tu.first_name,"src":tu.profile.src.url,"score":testpaper.get_score_user(tu),"rank":0})
#
#         arr_rank.sort(key=sort_score, reverse=True)
#         for i in range(0,len(arr_rank)):
#             arr_rank[i]['rank'] = i+1
#             if arr_rank[i]['uid'] == user.id : myrank = arr_rank[i]['rank']
#
#         arr_submit = []
#
#         for tq in testpaper.get_questions() :
#             tps = get_or_none(TestPaperSubmit,user=user,testpaper=testpaper,question=tq)
#             if tps:
#                 arr_submit.append({
#                     "tps_id":tps.id, "user_id":tps.user.id, "testpaper_id":tps.testpaper.id,
#                     "answer_user":tps.answer, "answer_correct":tps.question.answer_mobile,
#                     "id":tps.question.id,"type":tps.question.type,"unit_id":tps.question.unit.id,"unit":tps.question.unit.title,"unit_title":tps.question.unit.title,"src":tps.question.src.url,"explain":tps.question.explain.url,"keyword":tps.question.keyword,
#                     "video":tps.question.video,"answer":tps.question.answer,"is_active":tps.question.is_active,"date_created":"%s"%set_date(tps.question.date_created)
#                 })
#
#         return HttpResponse(json.dumps([{"submits":arr_submit,"ranks":[{
#             "username":user.first_name,
#             "src":user.profile.src.url,
#             "uid":user.id,
#             "score":testpaper.get_score_user(user),
#             "rank":myrank,
#             "scores":arr_rank}]}], default=date_handler), content_type="application/json")
#     return HttpResponse(json.dumps([{}]), content_type="application/json")
#
# def set_testpaper_submit(request):
#     user = get_or_none(User,id=request.GET.get("uid",0))
#     testpaper = get_or_none(TestPaper,id=request.GET.get("tpid",0))
#     answer = request.POST.get("answer","")
#
#     jo = json.loads(answer)
#
#     for tq in testpaper.get_questions() :
#         TestPaperSubmit.objects.get_or_create(user=user,testpaper=testpaper,question=tq,answer=jo[str(tq.id)])
#
#     ts = list(TestPaperSubmit.objects.filter(user=user,testpaper=testpaper).values())
#
#     if ts : return HttpResponse(json.dumps({"state":1}), content_type="application/json")
#     return HttpResponse(json.dumps({"state":0}), content_type="application/json")
#
# def redirect_market(request):
#     response = HttpResponse("", status=302)
#     response['Location'] = "market://details?id=net.sevenoclock.mobile"
#     return response

@csrf_exempt
def mobile(request):
    if request.GET.get("mode") == "get_user" :
        return get_user(request)
    elif request.GET.get("mode") == "get_user_info" :
        return get_user_info(request)
    elif request.GET.get("mode") == "get_school_name" :
        return get_school_name(request)
    elif request.GET.get("mode") == "set_user" :
        return set_user(request)
    # elif request.GET.get("mode") == "set_user_profilepic" :
    #     return set_user_profilepic(request)
    # elif request.GET.get("mode") == "set_user_passwd" :
    #     return set_user_passwd(request)
    elif request.GET.get("mode") == "set_user_info" :
        return set_user_info(request)
    elif request.GET.get("mode") == "set_school_info" :
        return set_school_info(request)
    # elif request.GET.get("mode") == "get_question_unit" :
    #     return get_question_unit(request)
    # elif request.GET.get("mode") == "get_question_list" :
    #     return get_question_list(request)
    # elif request.GET.get("mode") == "get_question_search" :
    #     return get_question_search(request)
    # elif request.GET.get("mode") == "get_question_feedback" :
    #     return get_question_feedback(request)
    # elif request.GET.get("mode") == "set_question_feedback" :
    #     return set_question_feedback(request)
    # elif request.GET.get("mode") == "get_testpaper_list" :
    #     return get_testpaper_list(request)
    # elif request.GET.get("mode") == "get_testpaper_question_list" :
    #     return get_testpaper_question_list(request)
    # elif request.GET.get("mode") == "get_invenroty":
    #     return get_invenroty(request)
    # elif request.GET.get("mode") == "set_invenroty":
    #     return set_invenroty(request)
    # elif request.GET.get("mode") == "get_inventory_list":
    #     return get_inventory_list(request)
    # elif request.GET.get("mode") == "get_inventory_question_list":
    #     return get_inventory_question_list(request)
    # elif request.GET.get("mode") == "get_testpaper_submit":
    #     return get_testpaper_submit(request)
    # elif request.GET.get("mode") == "set_testpaper_submit":
    #     return set_testpaper_submit(request)
    # elif request.GET.get("mode") == "redirect_market":
    #     return redirect_market(request)
    return HttpResponse('0')

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def set_date(obj):
    return obj.strftime('%Y.%m.%d')

def sort_score(json):
    try:
        return int(json['score'])
    except KeyError:
        return 0