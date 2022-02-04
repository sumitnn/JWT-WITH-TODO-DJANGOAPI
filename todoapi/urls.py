
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from main.views import *
from authentication.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('api/', include('main.urls')),
    path('',HomeApiView.as_view(),name="HomeApiView"),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
