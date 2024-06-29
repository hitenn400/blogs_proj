

from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import ParentInfoViewSet, ChildInfoViewSet, BlogsViewSet, HomeFeedViewSet,TestEndpoint
router = DefaultRouter()
router.register(r'parents', ParentInfoViewSet)
router.register(r'children', ChildInfoViewSet)
router.register(r'blogs', BlogsViewSet)
router.register(r'home-feed', HomeFeedViewSet, basename='home-feed')

urlpatterns = [
    path("ping", TestEndpoint.as_view(), name="test_endpoint"),
    path('', include(router.urls)),
]
