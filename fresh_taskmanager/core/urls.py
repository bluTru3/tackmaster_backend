from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import views

def home(request):
    return JsonResponse({
        'message': 'Task Manager API is running',
        'endpoints': {
            'register': '/api/register/',
            'login': '/api/login/',
            'tasks': '/api/',
            'admin': '/admin/',
        }
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/register/', views.register, name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api/me/', views.me, name='me'),
    path('api/', include('api.urls')),
]
