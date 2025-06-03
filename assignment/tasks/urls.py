from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register_api, name='api_register'),
    path('api/login/', views.login_api, name='api_login'),
    path('api/logout/', views.logout_api, name='api_logout'),
    path('api/protected/', views.protected_api, name='api_protected'),
    path("api/tasks/",views.get_all_tasks, name="task_list"),
    path("api/add/", views.add_task, name="task_add"),
    path('api/<int:task_id>/complete/', views.mark_task_completed, name="completed"),
    path('api/name/',  views.get_user_name, name='get_user_name')
]
