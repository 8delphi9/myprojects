from rest_framework import serializers
from .models import *


class RecordSummarySerializer(serializers.ModelSerializer):
    """
    author : 전재완
    explanation : 가계부의 요약 정보 serializer
    """

    class Meta:
        model = Record
        fields = ["id", "date", "amount", "in_ex"]


class LedgerDetailSerializer(serializers.ModelSerializer):
    """
    author : 임혁
    explanation : 가계부의 상세 정보 Serializer
    """

    class Meta:
        model = Record
        fields = ("id", "date", "in_ex", "amount", "method", "memo")


class RecordModifySerializer(serializers.ModelSerializer):
    """
    author : 전재완
    explanation : 가계부 수정 serializer
    """

    class Meta:
        model = Record
        fields = ("amount", "memo")
