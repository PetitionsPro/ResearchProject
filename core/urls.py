
from django.contrib import admin
from django.urls import path,include
from .views import app_ui, stories_ui, admin_stories_ui, admin_skills_ui, admin_search_ui

from core import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', app_ui, name='app-ui'),
    path('stories/', stories_ui, name='stories-ui'),
    path('admin-stories/', admin_stories_ui, name='admin-stories-ui'),
    path('admin-skills/', admin_skills_ui, name='admin-skills-ui'),
    path('admin-search/', admin_search_ui, name='admin-search-ui'),
    path('admin/', admin.site.urls),
    path('cv/', include('parse.urls')),
    path('data/', include('dynamic_data.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
