from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import ParentInfo, ChildInfo, Blogs
from .serializers import ParentInfoSerializer, ChildInfoSerializer, BlogsSerializer
from .permissions import IsOwnerOrReadOnly

# Create your views here.
class TestEndpoint(APIView):

    def get(self, request):
        try:
            return Response({"Ping": "Pong!"})
        except Exception as e:
            return Response({"Exception": str(e)})


class ParentInfoViewSet(viewsets.ModelViewSet):
    queryset = ParentInfo.objects.all()
    serializer_class = ParentInfoSerializer
    permission_classes = [IsAuthenticated]


class ChildInfoViewSet(viewsets.ModelViewSet):
    queryset = ChildInfo.objects.all()
    serializer_class = ChildInfoSerializer
    permission_classes = [IsAuthenticated]


class BlogsViewSet(viewsets.ModelViewSet):
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return Blogs.objects.filter(created_by=self.request.user)



class HomeFeedViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='home-feed')
    def home_feed(self, request):
        parent_id = request.query_params.get('parent_id')
        cache_key = f'home_feed_{parent_id}'
        cached_feed = cache.get(cache_key)

        if cached_feed:
            return Response(cached_feed, status=status.HTTP_200_OK)

        try:
            parent = ParentInfo.objects.get(id=parent_id)
            preferences = parent.feed_preferences
            children = ChildInfo.objects.filter(parent_details=parent)
            feed = []

            for child in children:
                query = Blogs.objects.filter(suitable_for_age__contains=[child.age], suitable_for_gender__in=[child.gender, 'other'])

                if preferences:
                    # Apply preferences from parent
                    if 'topics' in preferences:
                        query = query.filter(content__icontains=preferences['topics'])

                feed.extend(query)

            serializer = BlogsSerializer(feed, many=True)
            cache.set(cache_key, serializer.data, timeout=60*15)  # Cache for 15 minutes
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ParentInfo.DoesNotExist:
            return Response({'error': 'Parent not found'}, status=status.HTTP_404_NOT_FOUND)
