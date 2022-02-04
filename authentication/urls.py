from django.urls import path
from .views import *
urlpatterns = [
    path('signup/',SignupView.as_view(),name='signup' ),
    path('login/',LoginView.as_view(),name='login' ),
    path('home/',HomeView.as_view(),name='home' ),
    path('confirm-email/<uuid:token>/',ConfirmEmailView.as_view(),name='confirm-email' ),
]