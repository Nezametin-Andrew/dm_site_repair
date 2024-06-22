from django.views.generic.detail import SingleObjectMixin
from .models import Category, Tag, Article
from django.core.paginator import Paginator


class CategoryTagMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        print(kwargs['object'].pk)
        prev = False
        next_ = False
        try:
            next_ = Article.objects.filter(pk__gt=kwargs['object'].pk).order_by('pk').first()
        except Exception as e:
            print(e)

        try:
            prev = Article.objects.filter(pk__lt=kwargs['object'].pk).order_by('-pk').first()
        except Exception as e:
            print(e)
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['hide_cat'] = ['Последнее', 'Лента', 'Новости']
        context['cat_count'] = {cat.title: cat.category.count() for cat in Category.objects.all()}
        context['tags'] = Tag.objects.all()
        context['next'] = next_
        context['prev'] = prev
        return context