from django.urls import path
from .Controllers import *

urlpatterns = [
    # All the urls and the functions to activate on the urls
    path('login/', UsersController.login),
    path('register/', UsersController.register),
    path('users/<str:pk>/games/', UsersController.user_games),
    path('users/<str:user_name>/games/<str:game_name>', UsersController.user_games),
    path('games/<str:game_name>/', GamesController.get_game),
    path('games/', GamesController.get_games),
    path('games/<str:game_name>/reviews', GamesController.get_game_reviews),
    path('genres/', GenresController.get_genres),
    path('genres/<str:genre>/', GenresController.get_genre_games),
    path('platforms/', PlatformController.get_platform),
    path('platforms/<str:platform>/', PlatformController.get_platform_games),
    path('posts/', PostsController.create_post),
    path('posts/popular/', PostsController.popular_posts),
    path('posts/popular/game/<str:game_name>/', PostsController.popular_game_posts),
    path('posts/popular/user/<str:user_name>/', PostsController.popular_user_posts),
    path('posts/<str:pk>/', PostsController.user_post),
    path('posts/user/<str:pk>', PostsController.get_user_posts),
    path('posts/<str:post_id>/likes/', LikeController.likes),
    path('posts/<str:post_id>/likes/<str:user_name>', LikeController.user_likes),
    path('posts/<str:post_id>/comment/', CommentController.comments),
    path('posts/<str:post_id>/comment/amount/', CommentController.comment_amounts),
    path('posts/<str:post_id>/comment/<str:comment_id>', CommentController.spec_comment),
    path('reviews/', ReviewsController.create_review),
    path('reviews/<str:rev_id>/', ReviewsController.specific_review),
]
