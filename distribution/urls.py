from django.urls import path
from .views import *

urlpatterns = [
        path('client/', ClientListView.as_view(), name='client'),
        path('client/<int:pk>/', ClientDetailView.as_view())
]