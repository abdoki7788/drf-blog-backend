from rest_framework import viewsets
from .models import Article, Category, Tag
from .serializers import ArticleSerialize, CategorySerialize, TagSerializer

# Create your views here.


class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = ArticleSerialize
	filterset_fields = ['status', 'author__username', 'published']

class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerialize

class TagViewSets(viewsets.ModelViewSet):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer