from rest_framework import viewsets
from .models import Article, Tag
from .serializers import ArticleSerialize, TagSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import pagination
import requests
# Create your views here.

class ArticlePagination(pagination.PageNumberPagination):
	page_size = 9
	page_size_query_param = 'page_size'
	def get_paginated_response(self, data):
		return Response({
			'next': self.get_next_link(),
			'previous': self.get_previous_link(),
			'count': self.page.paginator.count,
			'total_pages': self.page.paginator.num_pages,
			'results': data
		})

class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = ArticleSerialize
	filterset_fields = ['status', 'author__username', 'published', 'tags__slug', 'tags']
	pagination_class = ArticlePagination
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
	
	def retrieve(self, request, *args, **kwargs):
		obj = self.get_object()
		obj.views += 1
		obj.save()
		return Response(ArticleSerialize(obj).data)


class TagViewSets(viewsets.ModelViewSet):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer



class UserActivationView(APIView):
	def get(self, request, uid, token):
		protocol = 'https://' if request.is_secure() else 'http://'
		web_url = protocol + request.get_host()
		post_url = web_url + "/api/auth/users/activation/"
		print(post_url)
		post_data = {'uid': uid, 'token': token}
		result = requests.post(post_url, data = post_data)
		return Response(data=result.content, status=result.status_code)
