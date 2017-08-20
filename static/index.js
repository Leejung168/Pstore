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
