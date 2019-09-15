$(document).ready(function(){
    /*
        add event listener to load the faculties based on the selected institution when
        the user clicks the faculties dropdown
    */
    document.getElementById("faculty").addEventListener('click', getFacultyOptions);
   
   /*
        add event listener to load faculties based on when the user reselects another 
        institution
   */
    document.getElementById("institution").addEventListener('change', function(){
        getFacultyOptions();
    });

    /*
        add event listener to load departments based on when the user reselects another
        faculty
    */
    document.getElementById("faculty").addEventListener('change', getDepartmentOptions);

    /* 
        add event listener to select and add courses to list of tutor courses
    */
   
});

// get the current selected university and send it to the server to get all the faculties
function getFacultyOptions(){
    let e = document.getElementById("institution");
    let institution = e.options[e.selectedIndex].value;
    $.ajax({
         type : "GET",
         url : "/faculty-options/",
         data : {
             "institution" : institution
         },
         dataType : 'text',
         success : function(data, textStatus, jqXHR){
             document.getElementById("faculty").innerHTML = data;
             getDepartmentOptions();
         },
         error: function(xhr, status, error){

             
         },               
     //Your code for AJAX Ends
     }); 
}

function getDepartmentOptions(){
    let e = document.getElementById("faculty");
    if (!e.innerHTML.length){
        // empty the department options if there is no faculty option
        document.getElementById("department").innerHTML = "";
        return;
    }
    let faculty = e.options[e.selectedIndex].value;
    $.ajax({
        type : "GET",
        url : "/department-options/",
        data : {
            "faculty" : faculty
        },
        dataType : "text",
        success : function(data, textStatus, jqXHR){
            document.getElementById("department").innerHTML = data;
        },
        error : function(xhr, status, error){

        }
    });
}