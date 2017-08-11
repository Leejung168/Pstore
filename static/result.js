function deleteinfo(obj){
    var passwd_id = $(obj).attr("id");
    $('#passwd_id').val(passwd_id);
}

$(".")


function editinfo(obj){
    var u_hostid = $(obj).attr("id");
    var u_servername = $(obj).closest('tr').find('td:eq(1)').text();
    var u_ip = $(obj).closest('tr').find('td:eq(2)').text();
    var u_port = $(obj).closest('tr').find('td:eq(3)').text();
    var u_username = $(obj).closest('tr').find('td:eq(4)').text();
    var u_password = $(obj).closest('tr').find('td:eq(5)').text();
    var u_comment = $(obj).closest('tr').find('td:eq(6)').text();
    $('#u_hostid').val(u_hostid)
    $('#u_servername').val(u_servername)
    $('#u_ip').val(u_ip)
    $('#u_port').val(u_port)
    $('#u_username').val(u_username)
    $('#u_password').val(u_password)
    $('#u_comment').val(u_comment)
    }

$(document).ready(function(){
$("#mytable #checkall").click(function () {
        if ($("#mytable #checkall").is(':checked')) {
            $("#mytable input[type=checkbox]").each(function () {
                $(this).prop("checked", true);
            });

        } else {
            $("#mytable input[type=checkbox]").each(function () {
                $(this).prop("checked", false);
            });
        }
    });
    
    $("[data-toggle=tooltip]").tooltip();

//Delete the entry
$("#lambertyes").click(function(){  
    // Get the delete username/password id.
    var result = $("#passwd_id").val();
    $.ajax({
        url: "/delete",
        type: "post",
        dataType: "json",
        data: {
            "password_id": result,
        },
        success: function() {   
            location.reload();  
        }
    })  
  });

//Edit the entry
$("#lambertupdate").click(function(){
    var u_hostid = $("#u_hostid").val();
    var u_servername = $("#u_servername").val();
    var u_ip = $("#u_ip").val();
    var u_port = $("#u_port").val();
    var u_username = $("#u_username").val();
    var u_password = $("#u_password").val();
    var u_servername = $("#u_servername").val();
    var u_comment = $("#u_comment").val();
    $.ajax({
        url: "/edit",
        type: "post",
        dataType: "json",
        data: {
            "u_hostid": u_hostid,
            "u_servername": u_servername,
            "u_ip": u_ip,
            "u_port": u_port,
            "u_username": u_username,
            "u_password": u_password,
            "u_servername": u_servername,
            "u_comment" : u_comment,
        },
        success: function() {
            location.reload();
        }
    })
  });


});
