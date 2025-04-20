from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from tasks.views import obtain_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    path('api/token/', obtain_token, name='token_obtain'),
]