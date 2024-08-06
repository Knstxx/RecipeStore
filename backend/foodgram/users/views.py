from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from users.models import User
from users.serializers import CustomUserSerializer


class CustomUserViewSet(DjoserUserViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        users = User.objects.all()
        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = CustomUserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get_serializer_class(self):
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



'''
    path('users/subscriptions/',
         SubscriptionsView.as_view(),
         name='subscriptions'
         ),
    path('users/<int:user_id>/subscribe/',
         SubscribeView.as_view(),
         name='user-subscribe'
         ),'''
