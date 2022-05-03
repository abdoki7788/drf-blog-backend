from rest_framework import viewsets
from .models import Article, Tag, IPAddress, Comment
from .serializers import ArticleSerialize, TagSerializer, ArticleCreateSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import filters
from .permissions import IsAuthorOrSuperuserElseReadOnly, EveryOne
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
import datetime
# Create your views here.

class ArticlePagination(PageNumberPagination):
	page_size = 9
	page_size_query_param = 'page_size'
	def get_paginated_response(self, data):
		return Response({
			'next': self.get_next_link(),
			'previous': self.get_previous_link(),
			'total_pages': self.page.paginator.num_pages,
			'active_page': self.page.number,
			'results': data
		})

class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.filter(status=True)
	filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
	search_fields = ['content', 'title']
	lookup_field = 'slug'
	ordering_fields = ['published', 'hits', 'likes']
	filterset_fields = ['status', 'author__username', 'published', 'tags__slug', 'tags']
	pagination_class = ArticlePagination
	def get_serializer_class(self):
		if self.action in ['create', 'update']:
			serializer_class = ArticleCreateSerializer
		else:
			serializer_class = ArticleSerialize
		return serializer_class
	def get_permissions(self):
		if self.action in ['like', 'dislike', 'add_view']:
			permission_classes = [EveryOne]
		elif self.action == 'comments':
			permission_classes = [IsAuthenticatedOrReadOnly]
		else:
			permission_classes = [IsAuthorOrSuperuserElseReadOnly]
		return [permission() for permission in permission_classes]
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
	
	@action(methods=['post'], detail=True)
	def add_view(self, request, *args, **kwargs):
		obj = self.get_object()
		req_ip = request.META['REMOTE_ADDR']
		if not IPAddress.objects.filter(ip=req_ip):
			ip_obj = IPAddress(ip=req_ip)
			ip_obj.save()
		else:
			ip_obj = IPAddress.objects.filter(ip=req_ip)[0]
		if not obj.hits.filter(ip=req_ip):
			obj.hits.add(ip_obj)
		return Response({'hits':obj.hits.count()})
	@action(methods=['get', 'post'], detail=True)
	def comments(self, request, pk):
		obj = self.get_object()
		if request.method == 'GET':
			comments = obj.comments.all()
			serialized_comments = CommentSerializer(comments, many=True)
			return Response(serialized_comments.data)
		elif request.method == 'POST':
			data = request.data
			comment = CommentSerializer(data=data)
			if comment.is_valid():
				comment.save(author=request.user, article=obj)
				return Response(comment.data)
			else:
				return Response(comment.errors)
	@action(methods=['get'], detail=False)
	def week_trand(self, request):
		now = datetime.datetime.now()
		week_start = now - datetime.timedelta(days = 7)
		trand = Article.objects.filter(published__range=[week_start, now], status=True).order_by('-like', '-hits')
		if trand:
			return Response(ArticleSerialize(trand[0]).data)
		else:
			return Response({'detail': 'no articles made in the last week'}, status=404)


class TagViewSets(viewsets.ModelViewSet):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer
	@action(methods=['get'], detail=True)
	def articles(self, request, pk):
		base_link = reverse('article-list')+f'?tags={pk}'
		if request.query_params.get('page_size'):
			base_link += f'&page_size={request.query_params.get("page_size")}'
		if request.query_params.get('page'):
			base_link += f'&page={request.query_params.get("page")}'
		return HttpResponseRedirect(redirect_to=base_link)


class ArticleShortLink(APIView):
	def get(self, request, shortlink):
		try:
			obj = Article.objects.get(short_link=shortlink)
			return HttpResponseRedirect(reverse('article-detail', kwargs={'pk': obj.id}))
		except Article.DoesNotExist:
			return Response('article not found', status=404)


class CommentsViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	def get_permissions(self):
		if self.action == 'create':
			permission_classes = [IsAuthenticatedOrReadOnly]
		else:
			permission_classes = [IsAuthorOrSuperuserElseReadOnly]
		return [permission() for permission in permission_classes]
	def create(self, request, *args, **kwargs):
		data = request.data
		comment = CommentSerializer(data=data)
		if comment.is_valid():
			comment.save(author=request.user, article=data['article'])
			return Response(comment.data)
		else:
			return Response(comment.errors)