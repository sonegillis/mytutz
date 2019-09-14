$(function(){
    // initialize tooltipster on text input elements
	$('input').tooltipster({
		trigger: 'custom',
		onlyOne: false,
		position: 'right',
		theme: ['tooltipster-noir', 'tooltipster-noir-customized']
    });
    
    $.validator.addMethod('strongPassword', function(value, element){
        return this.optional(element) 
        || value.length >= 8
        && /\d/.test(value)
        && /[a-z]/i.test(value)
    },
    'Your password must atleast 8 characters with atleast one number included'
    );
    $("#user-form").submit(function(e) {
        e.preventDefault();
    }).validate({
        rules: {
            email : {
                required : true,
                email : true
            },
            password1: {
                strongPassword : true,
            },
            password2: {
                required : true,
                equalTo : "#password1",
            }
        },
        messages: {
            
        },
        errorPlacement: function (error, element) {
			$(element).tooltipster('content', $(error).text());
			$(element).tooltipster('show');
		},
        submitHandler: function(form){
            var userForm = document.getElementById('user-form');
            var form_data = new FormData(userForm);
            $.ajax({
                type : "POST",
                url : window.location.href,
                data : form_data,
                cache:false,
                contentType: false,
                processData: false,
                dataType : 'text',
                success : function(response){
                    swal({
                        title: "Succesfully Changed Password",
                        text: "",
                        type: "success",
                        closeOnClickOutside: false,
                        closeOnEsc: false,
                        allowOutsideClick: false,
                        }).then(function() {
                        // Redirect the user
                        window.location.href = response;
                    });                   
                },
                error: function(xhr, status, error){
                    swal({
                        title: "An error occurred",
                        text: "Report this to developer",
                        type: "error",
                        closeOnClickOutside: false,
                        closeOnEsc: false,
                        allowOutsideClick: false,
                        }).then(function() {
                        // Redirect the user
                        // window.location = xhr.responseText;
                    });
                }             
            //Your code for AJAX Ends
            }); 
            return false;
        },
    });
});