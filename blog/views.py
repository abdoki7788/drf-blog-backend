from rest_framework import viewsets
from .models import Article, Category
from .serializers import ArticleSerialize, CategorySerialize

# Create your views here.


class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = ArticleSerialize

class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerialize