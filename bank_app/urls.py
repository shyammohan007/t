from django.urls import path
from .views import *


urlpatterns = [
    path('transactions/<str:date>', TransactionListAPI.as_view()),
    path('balance/<str:date>', BalanceAPI.as_view()),
    path('details/<int:pk>', TransactionDetailAPI.as_view()),
    path('add/', TransactionListAPI.as_view()),
]