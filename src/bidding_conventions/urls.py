from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("ensure-csrf/", views.ensure_csrf),
    path("get-conventions/", views.GetConventions.as_view()),
    path("conventions-selected/", views.ConventionsSelected.as_view()),
]
