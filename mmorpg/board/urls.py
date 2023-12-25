from django.urls import path
from .views import PostsList, PostDetail, PostsSearchList, PostCreate, PostUpdate, PostDelete


urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('post<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('posts_search/', PostsSearchList.as_view(), name='posts_search'),
    path('post_create/', PostCreate.as_view(), name='post_create'),
    path('post<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('post<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
