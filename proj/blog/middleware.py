from datetime import timedelta
import uuid

from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

from .models import AnonymousUser, IpAddress, Visit, ViewArticle, Article, NotAccessPath


def generate_unique_sesid():
    return str(uuid.uuid4())


class AnonymousUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        sesid = request.COOKIES.get('sesid')
        ip_address = request.META.get('REMOTE_ADDR', None)

        if ip_address is None or ip_address == '':
            ip_address = request.META.get('HTTP_X_REAL_IP', None)
        if ip_address is None or ip_address == '':
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if ip_address is None or ip_address == '':
            return request
        user = None

        end_date = timezone.now()
        start_date = end_date - timedelta(days=60)

        if sesid:
            try:
                user = AnonymousUser.objects.get(sesid=sesid)
            except AnonymousUser.DoesNotExist as e:
                user = AnonymousUser.objects.create(sesid=sesid)
                IpAddress.objects.create(ip=ip_address, user=user)
        else:
            # Находим записи, созданные в течение последних 60 дней
            ip_exists = IpAddress.objects.filter(ip=ip_address, created_at__range=(start_date, end_date)).exists()
            if ip_exists:
                user = IpAddress.objects.get(ip=ip_address).user
            else:
                user = AnonymousUser.objects.create(sesid=generate_unique_sesid())
                IpAddress.objects.create(ip=ip_address, user=user)
        request.anonymous_user = user

    def process_response(self, request, response):
        if not request.COOKIES.get('sesid'):
            response.set_cookie('sesid', request.anonymous_user.sesid, expires=None)
        return response


class VisitMiddleware(MiddlewareMixin):

    def process_request(self, request):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)

        list_page_exclude = ['admin']
        list_page_include = ['article']

        sesid = request.COOKIES.get('sesid')
        visit_path = request.path

        flag = True
        visit_flag = False

        user = None

        if sesid:
            try:
                user = AnonymousUser.objects.get(sesid=sesid)
            except AnonymousUser.DoesNotExist as e:
                print(e)
            if user is not None:

                for i in visit_path.split('/'):
                    if i in list_page_exclude:
                        flag = False
                    if i in list_page_include:
                        visit_flag = True

                if flag:
                    Visit.objects.create(user=user, page_visit=request.path)
                if visit_flag:
                    try:
                        article = Article.objects.get(slug=visit_path.split('/')[-2])
                        article_visit = ViewArticle.objects.filter(
                            user=user, article=article, created_at__range=(start_date, end_date)
                        )
                        if not article_visit:
                            ViewArticle.objects.create(user=user, article=article)
                            article.views = 1 + article.views
                            article.save()
                    except Exception as e:
                        print(e)

    def process_response(self, request, response):
        return response