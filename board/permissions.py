from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #읽기 권한 요청이면 인증여부 상관없이 GET
        if request.method in permissions.SAFE_METHODS:
            return True
        #request.user가 Blog의 user와 동일한지 확인 후 PUT, DELETE
        return obj.user == request.user