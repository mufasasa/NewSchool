from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout 
from .models import  Student, Course, Venue, Lecturer 
from django.urls import reverse 


# Index page. the view first checks whether the user is authenticated.
# if user is authenticated, then the student with the username is loaded 
#from the database. All the available courses are also loaded and passed to the index page

def index(request):
    if not request.user.is_authenticated: 
        return HttpResponseRedirect(reverse("login")) 

    student = Student.objects.get(user_name=request.user.username)
    courses = student.courses.all() 
    return render(request, "portal/index.html", {
        "courses": courses 
    })


# the login view gets the user name and password form the html page and authenticates
#the user. if no user matches that, the login page is loaded back and a message is 
# passed back to the user saying no user matches the login credentials.
# if a user was found, but not a student, the login page is again reloaded, telling 
# the user he is not a student.

def login_view(request):
    if request.method == "POST":
        message = "Not a Student"
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            student = Student.objects.filter(user_name=user.username)
            if not student:
                return render(request, "portal/login.html",{
                    "message":message
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "portal/login.html",{
                "message": message
            } )
    else:
        return render(request, "portal/login.html")

# this view loads the course information from the db and passes it on to the 
# course page. 
def course(request,code):
    course = Course.objects.get(course_code=code)
    return render(request, "portal/course.html", {
        "course":course
    })


# this view registers a student and redirects them to the index page
def register(request,code):
    course = Course.objects.get(course_code=code)
    student = Student.objects.get(user_name=request.user.username)
    existing = student.courses.filter(course_code=code) 
    if existing:
        return HttpResponseRedirect(reverse("index"))  
    student.courses.add(course)
    return HttpResponseRedirect(reverse("index")) 

# loads up all available courses from the db and passes them on the portal page
def all(request):
    courses = Course.objects.all()
    return render(request, "portal/all.html",{
        "courses":courses 
    }) 

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login")) 


# this view is for lectures. the user is first asked to provide their credentials.
# if a user matches the credentials, the view then checks wheter the user is a lecturer.
# if the user is not a lecturer, the login page is reloaded with the message "not a lecturer".
# if the user is a lecturer. the lecturer's course is loaded from the db, and the students
# that registered for the course as well. this is all then passed to the html page.
def lecturer(request): 
    message = "Not a lecturer"
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if not user:
            return render(request, "portal/lecturer_login.html",{
                "message":message
            })
        lecturers = Lecturer.objects.filter(code=user.username)
        if not lecturers:
            return render(request, "portal/lecturer_login.html",{
                "message":message
            })
        course = Course.objects.get(course_code=user.username)
        students = course.students.all()
        return render(request, "portal/lecturer.html",{
            "students":students
        })
    else:
        return render(request, "portal/lecturer_login.html")
