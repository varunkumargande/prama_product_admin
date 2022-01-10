import pytz
from datetime import datetime

from django.db import models

from accounts.models import Owner

# Create your models here.
class AbstractProduct(models.Model):
    """docstring for AbstractProduct"""
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(blank=True, default='')

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE,default='')
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)


    def __str__(self):
        return '%d - %s' % (self.id, self.name, )

    def save(self, *args, **kwargs):
        timezone = pytz.timezone("UTC")
        self.updated_at = timezone.localize(datetime.now())
        super(AbstractProduct, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Product(AbstractProduct):

    class Meta:
        ordering = ('-id', )