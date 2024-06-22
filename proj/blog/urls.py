from django.urls import path
from .views import *


urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category'),
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag'),
    path('update_like_article/', UpdateLikeArticle.as_view(), name='update_like_article'),
]