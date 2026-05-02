from django.urls import path
from .views import CvUploadView

urlpatterns = [
    path('parse/', CvUploadView.as_view(), name='cv-parse'),
]