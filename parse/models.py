from django.db import models

# Create your models here.


class Candidate(models.Model):
    user_uid=models.CharField(max_length=255, unique=True)
    name=models.CharField(max_length=255)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    skills=models.TextField()
    experience=models.TextField()
    education=models.TextField()
    resume=models.FileField(upload_to='resumes/')


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.user_uid:
            import uuid
            self.user_uid = str(uuid.uuid4())
        super().save(*args, **kwargs)
        