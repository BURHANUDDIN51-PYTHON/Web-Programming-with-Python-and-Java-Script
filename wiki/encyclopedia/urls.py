from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name='title'),
    path("search", views.search, name='search'),
    path('newpage', views.new_page, name="new_page"),
    path('editpage', views.edit_page, name="edit_page"),
    path('save', views.save_changes, name="save_changes"),
    path('random',views.random_page, name='random_page')
]
