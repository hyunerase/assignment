from rest_framework import serializers
from .models import *
from django.utils import timezone

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'created_at']

class CommentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']

class CommentResponseSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'
        #fields = ['id', 'user','nickname','comment','created_at']
    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')

#
class PostResponseSerializer(serializers.ModelSerializer):
    #이미 존재하는 필드 데이터 변경해서 리턴
    created_at = serializers.SerializerMethodField()
    comments = CommentResponseSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'body', 'created_at', 'comments']
    def get_created_at(self, obj):
        #처리하는 객체에서 created_at 데이터 가져오기
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')

class PostDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    comments = CommentResponseSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'body', 'created_at', 'comments']
    def get_created_at(self, obj):
        time = timezone.localtime(obj.created_at)
        return time.strftime('%Y-%m-%d')