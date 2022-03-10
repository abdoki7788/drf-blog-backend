from django.urls import path, include, re_path
from .views import UserActivationView

urlpatterns = [
	path('', include('djoser.urls')),
	path('', include('djoser.urls.authtoken')),
	re_path(r'^users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view())
]