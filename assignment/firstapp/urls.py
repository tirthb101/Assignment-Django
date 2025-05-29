from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("students/", views.get_students),
    path("students/add/", views.add_student),
    path("students/edit/<int:student_id>/", views.edit_student),
    path("students/delete/<int:student_id>/", views.delete_student),
]