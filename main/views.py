# from django.http import Http404
from wsgiref.util import request_uri
from django.shortcuts import render, get_object_or_404
from main import models

# Create your views here.

#It is to list all the articles on the webpage
def index(request):

    # latest_articles = models.Article.objects.all()[:10]

    # To get the articles in the order of which is created first
    # See we had added - in fron of our field publish_date
    # To order the data in decresing order by deault it is ascendng order

    # latest_articles = models.Article.objects.all().order_by('-publish_date')[:10]

    #To represent it more readable form we can create above variable as:
    latest_articles = models.Article.objects \
    .all() \
    .order_by('-publish_date')[:10]

    context = {
        "latest_articles": latest_articles
    }
    return render(request, 'main/index.html', context)


# It will list the content of the particle article
def article(request, pk):
    ## Similar to that we do in shell to get article
    # try:
    #     article = models.Article.objects.get(pk = pk)
    # except:
    #     # Now it will raises the error for article which doesn't added in the database
    #     raise Http404()

    article = get_object_or_404(models.Article, pk = pk)
    context = {
        "article": article
    }
    return render(request, 'main/article.html', context)


## This function is to list all the articles written by particular author
def author_articles(request, pk):
    author = get_object_or_404(models.Author, pk = pk)

    context = {
        "author": author
    }
    return render(request, 'main/author_articles.html', context)


## It will allow the author to publish there article from the frontend
def create_article(request):
    authors = models.Author.objects.all()
    context = {
        "authors":authors
    }

    if request.method == "POST":
        # Now we are storing the received data at form submission from create_article in dictionary
        # request.POST gives us the dictionary from the form submission 
        article_data = {
            "title": request.POST['title'],
            "context": request.POST['context']
        }
        article = models.Article.objects.create(**article_data)
        # author = models.Author.objects.filter(pk = request.POST['author'])
        # article.authors.set(author)
        author = models.Author.objects.get(pk = request.POST['author'])
        article.authors.set([author])
        context['submission_status'] = True

    return render(request, 'main/create_article.html', context)