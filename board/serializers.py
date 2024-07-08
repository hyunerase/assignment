from rest_framework import serializers
from .models import *
from django.utils import timezone

#1
class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user', 'nickname', 'title', 'created_at']
    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')

class CommentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']

#6
class CommentResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'user','nickname','comment','created_at']
    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')

#2
class PostDetailSerializer(serializers.ModelSerializer):
    #이미 존재하는 필드 데이터 변경해서 리턴
    created_at = serializers.SerializerMethodField()
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    comments = CommentResponseSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user', 'nickname', 'title', 'body', 'created_at', 'comments']
    def get_created_at(self, obj):
        #처리하는 객체에서 created_at 데이터 가져오기
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')

class PostListSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'created_at']
    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')