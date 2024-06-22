from django.urls import path
from .views import MainPage, QuizView, DesignView, RepairView


urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('quiz/', QuizView.as_view(), name='quiz'),
    path('design/<str:city>/', DesignView.as_view(), name='design'),
    path('repair/<str:city>/', RepairView.as_view(), name='repair'),
]