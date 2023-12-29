from django.urls import path
from .views import (PostsList,
                    PostDetail,
                    PostsSearchList,
                    PostCreate,
                    PostUpdate,
                    PostDelete,
                    ReactionCreate,
                    ReactionDelete,
                    user_posts,
                    user_reactions,
                    user_posts_reactions,
                    reaction_accept,
                    reaction_reject,)


urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('post<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('posts_search/', PostsSearchList.as_view(), name='posts_search'),
    path('post_create/', PostCreate.as_view(), name='post_create'),
    path('post<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('post<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('post<int:pk>/reactions/', ReactionCreate.as_view(), name='reaction_create'),
    path('user_posts/', user_posts, name='user_posts'),
    path('user_reactions/', user_reactions, name='user_reactions'),
    path('user_posts_reactions/', user_posts_reactions, name='user_posts_reactions'),
    path('reaction_delete/<int:pk>', ReactionDelete.as_view(), name='reaction_delete'),
    path('reaction_accept/<int:pk>/', reaction_accept, name='reaction_accept'),
    path('reaction_reject/<int:pk>/', reaction_reject, name='reaction_reject'),
]
