from django.urls import path
from rest_framework import routers
from .views import ArticleViewSet, TagViewSets, ArticleShortLink, CommentsViewSet

urlpatterns = [
	path('a/<str:shortlink>/', ArticleShortLink.as_view(), name='short-link')
]


router = routers.SimpleRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'tags', TagViewSets)
router.register(r'comments', CommentsViewSet)
urlpatterns += router.urls