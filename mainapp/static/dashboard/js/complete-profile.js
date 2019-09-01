var coursesList = [];
var coursesListID = [];
(function(){
    /*
        add event listener to load the faculties based on the selected institution when
        the user clicks the faculties dropdown
    */
    // document.getElementById("faculty").addEventListener('click', getFacultyOptions);
   
   /*
        add event listener to load faculties based on when the user reselects another 
        institution
   */
    // document.getElementById("institution").addEventListener('change', function(){
    //     getFacultyOptions();
    // });

    /*
        add event listener to load departments based on when the user reselects another
        faculty
    */
    // document.getElementById("faculty").addEventListener('change', getDepartmentOptions);

    /* 
        add event listener to select and add courses to list of tutor courses
    */
    document.getElementById("course").addEventListener('change', appendCourseToList);

    $("#submitForm").validate({
        submitHandler: function(form) {
            form.submit();
        }
    });

})();

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

function readImageUploadURL(input){
    if (input.files && input.files[0]){
        let reader = new FileReader();
        reader.onload = function(e) {
            $("#upload-img").attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function appendCourseToList() {
    let course = document.getElementById("course");
    if (coursesList.includes(course.value.split('-')[1])) {
        course.value = "";
        return;
    }
    let courses = document.getElementById("courses");
    coursesListID.push(course.value.split('-')[0]);
    coursesList.push(course.value.split('-')[1]);
    courses.innerHTML = createCourseBadges();
    $("#txtAreaCourses").val(coursesListID.join(","));
    courses.scrollTop = 80;
    course.value = "";
}

function createCourseBadges() {
    let courseTemplate = '';
    console.log('in course badge it is ', coursesList);
    for (const course of coursesList) {
        courseTemplate += `
                            <span class="badge badge-pill badge-primary" ondblclick="removeCourseFromList('${course}')"
                                style="margin-right: 8px; margin-bottom: 4px; cursor: pointer">
                                ${course} <i class="fas fa-close"></i>
                            </span>
                        `
    }
    
    return courseTemplate;
}

function removeCourseFromList(courseId) {
    for (let i = 0; i < coursesList.length; i++) {
        if (coursesList[i] === courseId) {
            coursesList.splice(i, 1);
        }
    }
    document.getElementById("courses").innerHTML = createCourseBadges();
    $("#txtAreaCourses").val(coursesList.join(","));
}