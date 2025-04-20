from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, obtain_token

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', obtain_token, name='token_obtain'),
]