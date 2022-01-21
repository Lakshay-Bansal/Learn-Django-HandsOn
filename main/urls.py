from django.urls import path

from main import views

urlpatterns = [
    path("", views.index, name = 'index'),
    path('article/<int:pk>', views.article, name='get_article'),
    path('author_articles/<int:pk>', views.author_articles, name='get_author_articles'),
    path('create_article', views.create_article, name = 'create_article')
]