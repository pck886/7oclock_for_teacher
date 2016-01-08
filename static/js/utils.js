$(document).ready(function(){
    $(function(){
        var frm = $("#csv_form");
        frm.ajaxForm(FileUploadCallback);
        frm.submit(function(){return false;});
    });

    $(function(){
       jcrop_api.setOptions(this.checked? {
            minSize: [ 80, 80 ],
            maxSize: [ 350, 350 ]
        }: {
            minSize: [ 0, 0 ],
            maxSize: [ 0, 0 ]
        });
        jcrop_api.focus();
    });

    $("#img_union_upload").change(function(){
        readURL(this);
    });

    function readURL(input){
        if(input.files && input.files[0]){
            var reader = new FileReader();
            reader.onload = function(e){
                $("#img_union").attr("src", e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    function FileUploadCallback(data, err){
        if(data=="error"){
            alert("파일전송중 오류가 발생하였습니다.\n다시한번 시도해주세요.");
            return false;
        }
        alert("파일전송이 완료되었습니다.");
    }

    function FileUpload(){
        if(!$("#upload_file").val()){
            alert("파일을 선택하세요.");
            $("#upload_file").focus();
            return;
        }
        var frm = $("#csv_form");
        frm.attr("action", "/photo");
        frm.submit();
    }
});