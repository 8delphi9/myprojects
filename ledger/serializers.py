from rest_framework import serializers
from .models import *


class RecordSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'date', 'amount', 'in_ex']


class LedgerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('id', 'date', 'in_ex', 'amount', 'method', 'memo')
        
class RecordModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('amount', 'memo')