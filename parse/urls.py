from django.urls import path
from .views import CvUploadView,StoryDataView,UserSearchAPIView

urlpatterns = [
    path('parse/', CvUploadView.as_view(), name='cv-parse'),
    path('story-data/',StoryDataView.as_view(),name='story-data'),
    path('story/user-data/',UserSearchAPIView.as_view(),name='user-data'),
    
]