from django.urls import path, include, re_path
from .views import UserActivationView, CustomUserViewSet, AuthorView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', CustomUserViewSet)



urlpatterns = [
	path('', include('djoser.urls')),
	path('', include('djoser.urls.authtoken')),
	path('author/<str:username>', AuthorView.as_view()),
	re_path(r'^users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view())
]

urlpatterns += router.urls