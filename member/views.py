from django.shortcuts import render
from .models import *
from .serializers import *
from board.models import *
from board.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

#확인 못함
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_info(request):
    user = request.user
    serializer = CustomInfoSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_list(request, user_id):
    user = request.user
    posts = Post.objects.filter(user=user_id)
    serializer = PostResponseSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)