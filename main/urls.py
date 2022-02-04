from django.urls import path
from .views import *
urlpatterns = [
    
    path('create-todo/',CreateTodoView.as_view(),name='create-todo' ),

]