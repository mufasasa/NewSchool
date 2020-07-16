from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout 
from .models import  Student, Course, Venue, Lecturer 
from django.urls import reverse 


# Create your views here.
def index(request):
    if not request.user.is_authenticated: 
        return HttpResponseRedirect(reverse("login")) 

    student = Student.objects.get(user_name=request.user.username)
    courses = student.courses.all() 
    return render(request, "portal/index.html", {
        "courses": courses 
    })


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

def course(request,code):
    course = Course.objects.get(course_code=code)
    return render(request, "portal/course.html", {
        "course":course
    })

def register(request,code):
    course = Course.objects.get(course_code=code)
    student = Student.objects.get(user_name=request.user.username)
    existing = student.courses.filter(course_code=code) 
    if existing:
        return HttpResponseRedirect(reverse("index"))  
    student.courses.add(course)
    return HttpResponseRedirect(reverse("index")) 

def all(request):
    courses = Course.objects.all()
    return render(request, "portal/all.html",{
        "courses":courses 
    }) 

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login")) 

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
