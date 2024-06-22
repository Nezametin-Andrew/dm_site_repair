from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from .mixins import CategoryTagMixin
from .models import Article, Category, Tag, LikeArticle, DisLikeArticle, AnonymousUser


class MainView(View):

    def get(self, request):
        page_number = request.GET.get('page', 1)
        article = Paginator(Article.objects.filter(is_published=True), 5).get_page(page_number)
        data = {
            'category': Category.objects.all(),
            'article': article,
            'tags': Tag.objects.all(),
            'is_paginated': article.has_other_pages(),
            'cat_count': {cat.title: cat.category.count() for cat in Category.objects.filter()},
            'hide_cat': ['Последнее', 'Лента', 'Новости']
        }
        return render(request, 'blog/index.html', data)


class ArticleDetailView(CategoryTagMixin, DetailView):

    model = Article
    template_name = 'blog/article.html'


class CategoryListView(View):

    def get(self, request, slug):
        page_number = request.GET.get('page', 1)
        article = Paginator(Article.objects.filter(category=Category.objects.get(slug=slug), is_published=True), 5).get_page(page_number)
        data = {
            'category': Category.objects.all(),
            'tags': Tag.objects.all(),
            'article': article,
            'cat_count': {cat.title: cat.category.count() for cat in Category.objects.all()},
            'is_paginated': article.has_other_pages(),
            'hide_cat': ['Последнее', 'Лента', 'Новости']
        }
        return render(request, 'blog/category.html', data)


class TagListView(View):

    def get(self, request, slug):
        page_number = request.GET.get('page', 1)
        article = Paginator(Article.objects.filter(tag=Tag.objects.get(slug=slug), is_published=True), 5).get_page(page_number)
        data = {
            'category': Category.objects.all(),
            'tags': Tag.objects.all(),
            'article': article,
            'is_paginated': article.has_other_pages(),
            'cat_count': {cat.title: cat.category.count() for cat in Category.objects.all()},
            'hide_cat': ['Последнее', 'Лента', 'Новости']
        }
        return render(request, 'blog/tags.html', data)


class UpdateLikeArticle(View):

    def post(self, request):
        sesid = request.COOKIES.get('sesid')
        answer = int(request.POST.get('answer', None))
        user = None
        article = None

        if sesid:
            try:
                user = AnonymousUser.objects.get(sesid=sesid)
                article = Article.objects.get(pk=int(request.POST.get('pk')))
            except Exception as e:
                print(e)
        if user and article:
            dislike = DisLikeArticle.objects.filter(user=user, article=article)
            like = LikeArticle.objects.filter(user=user, article=article)

            if answer is not None and answer:
                if not like:
                    article.likes = 1 + article.likes
                    LikeArticle.objects.create(user=user, article=article)
                if dislike:
                    if article.dis_likes:
                        article.dis_likes = article.dis_likes - 1
                    DisLikeArticle.objects.filter(user=user, article=article).delete()
                article.save()
            if answer is not None and not answer:
                if not dislike:
                    article.dis_likes = 1 + article.dis_likes
                    DisLikeArticle.objects.create(user=user, article=article)
                if like:
                    if article.likes:
                        article.likes = article.likes - 1
                    LikeArticle.objects.filter(user=user, article=article).delete()
                article.save()

        data = {
                'like': article.likes,
                'dislike': article.dis_likes
            }
        return JsonResponse(data)
