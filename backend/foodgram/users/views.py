from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from users.models import User, Subscribe
from users.serializers import (CustomUserSerializer, CreateUserSerializer,
                               SubSerializer)


class CustomUserViewSet(DjoserUserViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        users = User.objects.all()
        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = CustomUserSerializer(paginated_users,
                                          context={'request': request},
                                          many=True)
        return paginator.get_paginated_response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return CustomUserSerializer

    @action(detail=False, methods=['put', 'delete'], url_path='me/avatar')
    def set_avatar(self, request, *args, **kwargs):
        user = request.user

        if request.method == 'PUT':
            serializer = self.get_serializer(user, data=request.data,
                                             partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'avatar': serializer.data.get('avatar')})
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            user.avatar.delete()
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'], url_path='subscribe')
    def subscribe(self, request, id=None):
        author = self.get_object()
        user = request.user

        if request.method == 'POST':
            if user == author:
                return Response(
                    {'errors': 'Вы не можете подписаться на себя.'},
                    status=status.HTTP_400_BAD_REQUEST)
            if Subscribe.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на этого пользователя.'},
                    status=status.HTTP_400_BAD_REQUEST)
            Subscribe.objects.create(user=user, author=author)
            serializer = SubSerializer(author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            subscription = Subscribe.objects.filter(user=user, author=author)
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя.'},
                status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='subscriptions')
    def subscriptions(self, request):
        user = request.user
        subscriptions = Subscribe.objects.filter(user=user)
        authors = [subscription.author for subscription in subscriptions]
        paginator = self.pagination_class()
        paginated_authors = paginator.paginate_queryset(authors, request)
        serializer = SubSerializer(paginated_authors,
                                   context={'request': request},
                                   many=True)
        return paginator.get_paginated_response(serializer.data)
