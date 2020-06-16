from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token


from authe.views import RegisterUserAPIView, UserViewSet

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', RegisterUserAPIView.as_view())
]


router = DefaultRouter()
router.register('authe', UserViewSet, base_name='authe')


urlpatterns += router.urls