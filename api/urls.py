from django.urls import (path, include)
from .views import *

app_name = 'api'

urlpatterns = [
    path('ledgers/', RecordListView.as_view()),
    path('ledgers/<int:pk>/', DetailAPIView.as_view()),
    path('bin/', DeletedRecordListView.as_view())
]