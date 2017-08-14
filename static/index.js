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
//        data: {
//            "a_servername": "srv-hs-db2",
//            "a_ip": "1.1.1.1",
//            "a_port": "40022",
//            "a_username": "xueqing",
//            "a_password": "happylemon",
//            "a_comment" : "this is my ",
//            "a_servergroup": "hs",
//        },
        success: function() {
            location.reload();
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