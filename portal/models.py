from django.db import models

# Create your models here.
class Days(models.Model):
    days = models.CharField(max_length=12)
    def __str__(self):
        return f"{self.days}"


class Venue(models.Model):
    address = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.address}"

class Lecturer(models.Model):

    full_name = models.CharField(max_length=64)
    code = models.CharField(max_length=12) 

    def __str__(self):
        return f"{self.full_name}" 

class Course(models.Model):
    course_name = models.CharField(max_length=64)
    course_code = models.CharField(max_length=12)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="courses", blank=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name="courses", blank=True)
    day = models.ForeignKey(Days, related_name="courses", blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.course_name}"

class Student(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    user_name = models.CharField(max_length=12)
    courses= models.ManyToManyField(Course, blank=True, related_name="students")
    
    def __str__(self):
        return f"Student: {self.first_name} {self.last_name}"



