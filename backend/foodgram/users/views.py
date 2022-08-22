from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.paginations import LimitPageNumberPagination
from api.serializers import FollowListSerializer
from .models import Follow
from .serializers import (
    FollowSerializer, EmailLoginUserCreateSerializer, EmailLoginUserSerializer
)

User = get_user_model()


class EmailLoginUserViewSet(UserViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'subscribe':
            return FollowSerializer
        elif self.request.method == 'POST':
            return EmailLoginUserCreateSerializer
        return EmailLoginUserSerializer

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, following=author)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            subscription = get_object_or_404(
                Follow,
                user=user,
                following=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
