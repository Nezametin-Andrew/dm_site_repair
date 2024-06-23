from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from .models import Quiz, CallMi
from .sent_contact import add_client


CITY = {
    'anapa': 'Анапе',
    'novorossiysk': 'Новороссийске',
    'rostov-na-donu': 'Ростове-на-Дону',
    'krasnodar': 'Краснодаре',
}


ADDRESS = {
    'anapa': [],
    'novorossiysk': ['Новороссийск,', 'пр. Дзержинского 229,', '2-й этаж, офис 7'],
    'rostov-na-donu': ['Ростов-на-Дону,', 'Таганрогская улица 117,', 'офис 305'],
    'krasnodar': ['Краснодар,', 'улица Митрофана Седина 150,', 'офис 306'],
}

TEMPLATE_MESSAGE = """
Новая заявка на свйте design-pro-remont.ru
{name} оставил заявку, просит вас перезвонить
По номеру: {phone}
"""


class MainPage(View):

    def get(self, request):
        return render(request, 'index.html', {})

    def post(self, request):
        dct = {key: request.POST.get(key) for key in request.POST}

        if 'csrfmiddlewaretoken' in dct:
            del dct['csrfmiddlewaretoken']

        try:
            add_client(dct)
            CallMi.objects.create(**dct)

            send_mail(
                subject=_("Новая заявка на сайте design-pro-remont"),
                message=TEMPLATE_MESSAGE.format(name=dct['name'], phone=dct['phone']),
                from_email="nezametin.a@yandex.ru",
                recipient_list=['nezametin.andrey@gmail.com' ]
            )

            return render(request, 'index.html', {"status": "success"})
        except Exception as e:
            print(e)
            return render(request, 'index.html', {"status": "error"})


class DesignView(View):

    def get(self, request, city):
        return render(request, 'design.html',
                      {
                          'city': CITY[city],
                          'design': True,
                          'title': f"Дизайн квартир в {CITY[city]}",
                          'address': ADDRESS[city]
                      })

    def post(self, request):
        dct = {key: request.POST.get(key) for key in request.POST}

        if 'csrfmiddlewaretoken' in dct:
            del dct['csrfmiddlewaretoken']

        try:
            add_client(dct)
            CallMi.objects.create(**dct)

            send_mail(
                subject=_("Новая заявка на сайте design-pro-remont"),
                message=TEMPLATE_MESSAGE.format(name=dct['name'], phone=dct['phone']),
                from_email="nezametin.a@yandex.ru",
                recipient_list=['nezametin.andrey@gmail.com']
            )

            return render(request, 'index.html', {"status": "success"})
        except Exception as e:
            print(e)
            return render(request, 'index.html', {"status": "error"})


class RepairView(View):

    def get(self, request, city):
        return render(request, 'repair.html',
                      {
                          'city': CITY[city],
                          'repair': True,
                          'title': f"Ремонт квартир в {CITY[city]}",
                          'address': ADDRESS[city]

                      })

    def post(self, request):
        dct = {key: request.POST.get(key) for key in request.POST}

        if 'csrfmiddlewaretoken' in dct:
            del dct['csrfmiddlewaretoken']

        try:
            add_client(dct)
            CallMi.objects.create(**dct)

            send_mail(
                subject=_("Новая заявка на сайте design-pro-remont"),
                message=TEMPLATE_MESSAGE.format(name=dct['name'], phone=dct['phone']),
                from_email="nezametin.a@yandex.ru",
                recipient_list=['nezametin.andrey@gmail.com']
            )

            return render(request, 'index.html', {"status": "success"})
        except Exception as e:
            print(e)
            return render(request, 'index.html', {"status": "error"})


class QuizView(View):

    def post(self, request):
        amo_dct = {'name': request.POST.get('user-name'), 'phone': request.POST.get('user-phone')}
        try:
            dct = {key: request.POST.get(key) for key in request.POST}

            if 'csrfmiddlewaretoken' in dct:
                del dct['csrfmiddlewaretoken']
            add_client(amo_dct)
            Quiz.objects.create(**dct)

            send_mail(
                subject=_("Новая заявка на сайте design-pro-remont"),
                message=TEMPLATE_MESSAGE.format(name=dct['name'], phone=dct['phone']),
                from_email="nezametin.a@yandex.ru",
                recipient_list=['nezametin.andrey@gmail.com']
            )
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'error': str(e)})
