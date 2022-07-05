from django.urls import path 
from .views import DetailAPIView

urlpatterns = [
    path('ledgers/<int:pk>/', DetailAPIView.as_view()),
]
