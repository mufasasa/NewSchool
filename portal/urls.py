from django.urls import path, reverse
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"), 
    path("<str:code>", views.course, name="course"),
    path("<str:code>/register", views.register, name="register"),
    path("all/", views.all, name="all"),
    path("logout/", views.logout_view, name="logout"), 
    path("lecturer/", views.lecturer, name="lecturer"),

]