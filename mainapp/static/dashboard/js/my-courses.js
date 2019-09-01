$(document).ready(function () {
    $("#add-tutorial-session").submit(function(e) {
        e.preventDefault();
    }).validate({
        submitHandler: function(form) {
            $.ajax({
                url: "/tutor/add-tutorial-session/", 
                type: "POST",             
                data: $(form).serialize(),     
                success: function(data) {
                    $("#existing-tutorial-sessions").append(data);
                    $("#addTutorialSession").modal('toggle');
                    console.log('sucess is ', data);
                },
                error: function(error) {
                    console.log('error is ', error);
                }
            });
        }
    });
})