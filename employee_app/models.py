from django.db import models

class Employee(models.Model):
     # Define fields for the Employee model
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True) 
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phoneNo = models.CharField(max_length=15)
    addressDetails = models.JSONField()
    workExperience = models.JSONField()
    qualifications = models.JSONField()
    projects = models.JSONField()
    photo = models.TextField()  

     # Method to return a string representation of the employee (their name)

    def __str__(self):
        return self.name
