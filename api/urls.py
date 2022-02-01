from django.urls import path
from api import views

urlpatterns = [
    # path('', views.usersAPI, name='index'),
    # path('article/', views.articleApi, name='article'),
    # path('createArticle/', views.createArticleApi, name='createArticle'),

    # Uisng inbuilt views
    path('article/', views.ArticleListView.as_view()),   
    path('article/<int:pk>', views.ArticleDetailView.as_view()),
]