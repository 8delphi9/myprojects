from .models import Record
from rest_framework import serializers



class LedgerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('id', 'date', 'amount', 'method', 'memo', 'is_deleted')
        
