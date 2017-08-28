$("#lambertadd").click(function(){
    var a_servername = $("#a_servername").val();
    var a_ip = $("#a_ip").val();
    var a_port = $("#a_port").val();
    var a_username = $("#a_username").val();
    var a_password = $("#a_password").val();
    var a_comment = $("#a_comment").val();
    var a_servergroup = $("#a_servergroup").val();

    $.ajax({
        url: "/add",
        type: "post",
        dataType: "json",
        data: {
            "a_servername": a_servername,
            "a_ip": a_ip,
            "a_port": a_port,
            "a_username": a_username,
            "a_password": a_password,
            "a_comment" : a_comment,
            "a_servergroup": a_servergroup
        },
        success: function() {
            location.reload();
        },
        complete: function(mesg){
             alert(mesg["responseJSON"]);
        }
    })
})

$(".reveal").mousedown(function() {
     $(".pwd").replaceWith($('.pwd').clone().attr('type', 'text'));
 })
 .mouseup(function() {
   $(".pwd").replaceWith($('.pwd').clone().attr('type', 'password'));
 })
 .mouseout(function() {
   $(".pwd").replaceWith($('.pwd').clone().attr('type', 'password'));
 });


$("#a_ip").focusout(function() {
     var ip = $("#a_ip").val();
     var exp=/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
     var reg = ip.match(exp);
     if(reg==null) {
         alert("IP Address is unlegal");
         return true;
     };
 })


$("#a_port").focusout(function() {
     var port = $("#a_port").val();
     var reg = port.match(/^\d+$/);
     if (reg==null){
         alert("Not a number!");
         return true;
     };
 })
