from django.urls import path
from .views import BulkSkillCreateView, BulkEducationCreateView

urlpatterns = [
    path("skills/bulk-create/", BulkSkillCreateView.as_view(), name="bulk-skill-create"),
    path("education/bulk-create/", BulkEducationCreateView.as_view(), name="bulk-education-create"),
]