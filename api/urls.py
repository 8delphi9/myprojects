from django.urls import (path, include)
from .views import *

app_name = 'api'

record_summary_list = RecordListView.as_view({'get': 'list'})

urlpatterns = [
    path('ledgers/', record_summary_list, name='record-list'),
]