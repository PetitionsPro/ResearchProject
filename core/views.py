from django.shortcuts import render


def app_ui(request):
    return render(request, "ui/index.html")


def stories_ui(request):
    return render(request, "ui/stories.html")


def admin_stories_ui(request):
    return render(request, "ui/admin_stories.html")


def admin_skills_ui(request):
    return render(request, "ui/admin_skills.html")


def admin_search_ui(request):
    return render(request, "ui/admin_search.html")
