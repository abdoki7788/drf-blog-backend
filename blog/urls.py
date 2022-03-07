from django.urls import path
from rest_framework import routers
from .views import ArticleViewSet, TagViewSets

urlpatterns = [
	
]


router = routers.SimpleRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'tags', TagViewSets)
urlpatterns += router.urls