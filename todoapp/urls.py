from django.urls import path
from . import views

# Define URL patterns for the todo app
urlpatterns = [
    # URL pattern for the home page
    path('', views.home, name='home-page'),
    # URL pattern for user registration
    path('register/', views.register, name='register'),
    # URL pattern for user login
    path('login/', views.loginpage, name='login'),
    # URL pattern for user logout
    path('logout/', views.LogoutView, name='logout'),
    # URL pattern for deleting a task
    path('delete-task/<str:name>/', views.DeleteTask, name='delete'),
    # URL pattern for updating the status of a task
    path('update/<str:name>/', views.Update, name='update'),
]
