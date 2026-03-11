from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLogin, RegisterView, TaskToggle
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    path('', TaskList.as_view(), name='task_list'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task_detail'),
    path('create-task/', TaskCreate.as_view(), name='create_task'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task_update'),
    path('task-delete/<int:pk>', TaskDelete.as_view(), name='task_delete'),
    path('task-toggle/<int:pk>/', TaskToggle.as_view(), name='task_toggle'),
]
