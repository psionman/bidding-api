from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("version/", views.Version.as_view(), name="version"),
    path(
        "package-versions/",
        views.PackageVersions.as_view(),
        name="package-versions",
    ),
    path("ensure-csrf/", views.ensure_csrf),
    path("static-data/", views.StaticData.as_view()),
    path("get-conventions/", views.GetConventions.as_view()),
    path("conventions-selected/", views.ConventionsSelected.as_view()),
]
