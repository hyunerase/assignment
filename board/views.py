from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

# Create your views here.
@api_view(['GET','POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = PostDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

"""
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwnerOrReadOnly])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if request.method == 'GET':
            serializer = PostDetailSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = PostResponseSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
"""
#Custom Permission 적용하기 위해 check_object_permissions로 검사하려면 CBV로 바꾸어야함
class PostDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    def get_object(self, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(self.request, post)
        return post

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def comments_list(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        if request.method == 'GET':
            comments = Comment.objects.filter(post=post)
            serializer = CommentResponseSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            serializer = CommentRequestSerializer(data=request.data)
            if serializer.is_valid():
                new_comment = serializer.save(post=post, user=request.user)
                response = PostDetailSerializer(post)
                return Response(response.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

"""
@api_view(['GET', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsOwnerOrReadOnly])
def comment_delete(request, post_id, comment_id):
    if request.method == 'DELETE':
        post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post=post)
        serializer = CommentResponseSerializer(comments, many=True)
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)
"""

#Custom Permission 적용하기 위해 check_object_permissions로 검사하려면 CBV로 바꾸어야함
class CommentDelete(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    def delete(self, request, post_id, comment_id):
        post = Post.objects.get(pk=post_id)
        comment = Comment.objects.get(pk=comment_id)
        self.check_object_permissions(self.request, post)
        serializer = PostDetailSerializer(post)
        comment.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)