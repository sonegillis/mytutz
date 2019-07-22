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
            alert("hi");
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function appendCourseToList(){
    let course = document.getElementById("course");
    let courses = document.getElementById("courses");
    const oldValue = courses.innerHTML;
    let newValue = oldValue;
    console.log(course.value);
    createCourseBadge(course.value);
    course.value = "";
}

function createCourseBadge(courseCode){
    let template = `${courseCode} <i class="fas fa-close"></i>`
    let course = document.createElement("span");
    course.innerHTML = template;
    course.setAttribute("id", courseCode);
    course.setAttribute("class", "badge badge-pill badge-primary");
    course.style.marginRight = "8px";
    course.style.marginBottom = "4px";
    document.getElementById("courses").scrollTop = 80;
    document.getElementById("courses").appendChild(course);
    course.addEventListener("dblclick", removeCourseFromList(course));
    console.log(typeof course);
    return course;
}

function removeCourseFromList(course) {
    console.log("hello world");
    let parentNode = document.getElementById("courses");
    console.log(parentNode);
    parentNode.removeChild(course);
}