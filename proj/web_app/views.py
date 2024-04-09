from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .models import Quiz


class MainPage(View):

    def get(self, request):
        return render(request, 'index.html', {})


class QuizView(View):

    def post(self, request):
        try:
            dct = {key: request.POST.get(key) for key in request.POST}

            if 'csrfmiddlewaretoken' in dct:
                del dct['csrfmiddlewaretoken']


            Quiz.objects.create(**dct)
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})