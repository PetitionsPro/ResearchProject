from django.urls import path
from .views import CvUploadView

urlpatterns = [
    path('upload/', CvUploadView.as_view(), name='cv-upload'),
]