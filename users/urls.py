from django.urls import path, include, re_path
from .views import UserActivationView, CustomUserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', CustomUserViewSet)



urlpatterns = [
	path('', include('djoser.urls')),
	path('', include('djoser.urls.authtoken')),
	re_path(r'^users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view())
]

urlpatterns += router.urls