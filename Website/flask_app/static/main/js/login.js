// Login screen functionality wating for user input
$(document).ready(function() {
    $("#loginForm").submit(function(event) {
        event.preventDefault();
        var data_d = {
            'email': $('#email').val(),
            'password': $('#password').val()
        };
        $.ajax({
            url: "/processlogin",
            data: data_d,
            type: "POST",
            success: function(returned_data) {
                returned_data = JSON.parse(returned_data);
                if(returned_data.success) {
                    window.location.href = "/home";
                } else {
                    var errorMessage = "Login failed. Please check your credentials.";
                    if(returned_data.attempts) {
                        errorMessage += " Attempts: " + returned_data.attempts;
                    }
                    $("#loginError").text(errorMessage).show();
                }
            }
        });
    });
});