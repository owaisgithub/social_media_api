from django.urls import path

from main.views import (LoginView, 
                        UserView, 
                        FollowView, 
                        UnfollowView,
                        PostView,
                        AllPostView,
                        LikeView,
                        UnlikeView,
                        CommentView
                        )

urlpatterns = [
    path('authenticate', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('follow/<int:id>', FollowView.as_view()),
    path('unfollow/<int:id>', UnfollowView.as_view()),
    path('posts/', PostView.as_view()),
    path('posts/<int:id>', PostView.as_view()),
    path('all_posts', AllPostView.as_view()),
    path('like/<int:id>', LikeView.as_view()),
    path('unlike/<int:id>', UnlikeView.as_view()),
    path('comment/<int:id>', CommentView.as_view()),
]