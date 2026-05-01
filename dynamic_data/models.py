from django.db import models

# Create your models here.

class SkillModel(models.Model):
    name=models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}-{self.id}"


class EducationModel(models.Model):
    name=models.CharField(max_length=255)
    short_form = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.name}-{self.id}"