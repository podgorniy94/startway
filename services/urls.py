from django.urls import path

from .views import ContactFormView, EmailView, GetPost, Home, Search, ShowPage

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("search/", Search.as_view(), name="search"),
    path("rezervace/", ContactFormView.as_view(), name="contact"),
    path("email/", EmailView.as_view(), name="email"),
    path("blog/<str:slug>/", GetPost.as_view(), name="post"),
    path("<str:slug>/", ShowPage.as_view(), name="page"),
]
