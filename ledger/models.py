from django.db import models

# Create your models here.

class Record(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.IntegerField(null=False, default=0)
    IN_EX_CHOICES = [
        ('income', '수입'),
        ('expense', '지출'), 
        ]
    in_ex = models.CharField(choices=IN_EX_CHOICES, null=False, default=IN_EX_CHOICES[0][0], max_length=20)
    METHOD_CHOICES = [
        ('cash', '현금'),
        ('card', '카드'),
        ('transfer', '이체'),
    ]
    method = models.CharField(choices=METHOD_CHOICES, null=False, default=METHOD_CHOICES[0][0], max_length=20)
    memo = models.CharField(max_length=300, null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=False)