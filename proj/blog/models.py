import os
import uuid
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('media/article', filename)


class Category(models.Model):

    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категоря'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Tag(models.Model):

    title = models.CharField(max_length=255, verbose_name="")
    slug = models.SlugField(unique=True, verbose_name="")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})


class Article(models.Model):

    title = models.CharField(max_length=255, unique=True, verbose_name="Заголовок")
    article = RichTextUploadingField(verbose_name="Содержание")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category',
        related_query_name='category', verbose_name='Категория'
    )
    tag = models.ManyToManyField(Tag, verbose_name='Тег', null=True, blank=True)
    views = models.BigIntegerField(verbose_name='Просмотров')
    likes = models.BigIntegerField(verbose_name='Понравилось')
    dis_likes = models.BigIntegerField(verbose_name='Не понравилось')
    image = models.ImageField(upload_to=get_file_path, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    lent = models.BooleanField(default=False)
    slug = models.SlugField('URL', max_length=255, unique=True, db_index=True)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return f"{str(self.pk)}: {self.title}"

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': self.slug})


class AnonymousUser(models.Model):

    sesid = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{str(self.pk)}: {self.sesid}"


class Visit(models.Model):

    user = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE)
    page_visit = models.CharField(max_length=255, verbose_name='')
    visit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.pk)}  {str(self.visit_date)} :   {self.page_visit}"


class IpAddress(models.Model):

    ip = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE)


class DataArticle(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ViewArticle(DataArticle):
    ...


class LikeArticle(DataArticle):
    ...


class DisLikeArticle(DataArticle):
    ...



class NotAccessPath(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255, verbose_name='Path')
    count = models.BigIntegerField(verbose_name='Count')
    ip = models.ForeignKey(IpAddress, on_delete=models.CASCADE, verbose_name='ip')



