from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()
# Create your models here.




class Candidate_parsed_data(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.TextField(null=True, blank=True)
    email=models.TextField(null=True, blank=True)
    phone=models.TextField(null=True, blank=True)
    address=models.TextField(null=True, blank=True)
    skills=models.TextField(null=True, blank=True)
    soft_skills=models.TextField(null=True, blank=True)
    story=models.TextField(null=True, blank=True)
    experience=models.TextField(null=True, blank=True)   
    education=models.TextField(null=True, blank=True)
    resume=models.FileField(upload_to='resumes/')
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)


    def __str__(self):
        return f"name: {self.name} - id: {self.id}"