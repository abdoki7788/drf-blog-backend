from rest_framework import viewsets
from .models import Article, Category, Tag
from .serializers import ArticleSerialize, CategorySerialize, TagSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.


class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = ArticleSerialize
	filterset_fields = ['status', 'author__username', 'published', 'tags__slug', 'tags']
	@action(methods=['post'], detail=True)
	def like(self,request,pk):
		article = self.get_object()
		article.like += 1
		article.save()
		return Response(Article.objects.get(id=pk).like)
	
	@action(methods=['post'], detail=True)
	def dislike(self,request,pk):
		article = self.get_object()
		article.like -= 1
		article.save()
		return Response(Article.objects.get(id=pk).like)

class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerialize

class TagViewSets(viewsets.ModelViewSet):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer