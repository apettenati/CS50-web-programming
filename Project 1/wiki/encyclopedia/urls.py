from django.urls import path

from . import views

# app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("newpage", views.new_page, name="newpage"),
    path("randompage", views.random_page, name="randompage"),
    path("editpage/<str:title>", views.edit_page, name="editpage"),
    path("search/<str:title>", views.wiki, name="search"),
]
