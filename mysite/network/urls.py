from django.urls import path
from . import naivebayes

urlpatterns = [
    path('', naivebayes.index),
    path('responseLoad', naivebayes.responseLoad)
]