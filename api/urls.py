from api.views import CommentViewSet
from django.conf.urls import url, patterns, include
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
