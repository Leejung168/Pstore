$("#lambertadd").click(function(){
    var username = $("#username").val();
    var password = $("#password").val();

    $.ajax({
        url: "/verify_pw",
        type: "post",
        dataType: "json",
        data: {
            "username": username,
            "password": password,
        },
        success: function() {
            alert("login successful")
        }
    })
  });


$(".reveal").mousedown(function() {
     $(".pwd").replaceWith($('.pwd').clone().attr('type', 'text'));
 })
 .mouseup(function() {
   $(".pwd").replaceWith($('.pwd').clone().attr('type', 'password'));
 })
 .mouseout(function() {
   $(".pwd").replaceWith($('.pwd').clone().attr('type', 'password'));
 });
