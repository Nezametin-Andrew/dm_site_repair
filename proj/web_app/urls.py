from django.urls import path
from .views import MainPage, QuizView


urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('quiz/', QuizView.as_view(), name='quiz'),
]