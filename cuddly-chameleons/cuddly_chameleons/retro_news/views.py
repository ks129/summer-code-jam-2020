from django.http import Http404
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from retro_news import serializers
from retro_news.models import BlogArticle


class IsJwtAuthOrReadOnly(permissions.BasePermission):
    """Permission class that allow read only access when user is not authenticated or is not superuser."""


class BlogArticleListView(APIView):
    """Handles BlogArticle object listing and creation."""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request: Request):
        """Get all articles."""
        return Response(serializers.BlogArticleGetSerializer(BlogArticle.objects.all(), many=True).data)

    def post(self, request: Request):
        """Create new article."""
        if not request.user.is_superuser:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = serializers.BlogArticleSerializer(data=request.data)
        if serializer.is_valid():
            article = serializer.save(author=request.user)
            if article:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogArticleActionView(APIView):
    """Handles specific article actions."""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self, pk: int):
        """Get object based on primary key."""
        try:
            return BlogArticle.objects.get(pk=pk)
        except BlogArticle.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk: int):
        """Get one blog post by primary key."""
        post = self.get_object(pk)
        return Response(serializers.BlogArticleGetSerializer(post).data)

    def put(self, request: Request, pk: int):
        """Update blog post by primary key."""
        post = self.get_object(pk)
        serializer = serializers.BlogArticleSerializer(post, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int):
        """Delete blog post by primary key."""
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomUserCreate(APIView):
    """Handles user creation."""

    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request: Request):
        """Create new user."""
        serializer = serializers.CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(APIView):
    """Handles JWT Token deactivating."""

    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request: Request):
        """Deactivate user JWT token."""
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Define custom token pair view to include superuser status inside response."""
    serializer_class = serializers.CustomTokenObtainPairSerializer
