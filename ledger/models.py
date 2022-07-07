from django.db import models
from user.models import User

# Create your models here.

class SoftDeleteManager(models.Manager):
    use_for_related_fields = True
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class DeletedRecordManager(models.Manager):
    use_for_related_fields = True
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)

class  SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(null=False, default=False)
    
    class Meta:
        abstract = True
    
    objects = SoftDeleteManager()
    deleted_objects = DeletedRecordManager()
        
    def delete(self, using=None, keep_parents=False):
        self.is_deleted=True
        self.save(update_fields=['is_deleted'])
    
    def restore(self):
        self.is_deleted=False
        self.save(update_fields=['is_deleted'])


class Record(SoftDeleteModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
