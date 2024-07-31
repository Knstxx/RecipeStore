from django.urls import include, path

from users.views import UserAvatarUpdateView, SubscriptionsView, SubscribeView


urlpatterns = [
    path('',
         include('djoser.urls')
         ),
    path('auth/',
         include('djoser.urls.jwt')
         ),
    path('users/me/avatar/',
         UserAvatarUpdateView.as_view(),
         name='user-avatar'
         ),
    path('users/subscriptions/',
         SubscriptionsView.as_view(),
         name='subscriptions'
         ),
    path('users/<int:user_id>/subscribe/',
         SubscribeView.as_view(),
         name='user-subscribe'
         ),
]
