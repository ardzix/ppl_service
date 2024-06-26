from django.db import models
from django.utils.translation import gettext_lazy as _
import random
import string

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    
class Activity(models.Model):
    TYPE_CHOICES = [
        ('single', _('Single Occurrence')),
        ('multiple', _('Multiple Occurrences')),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    point_impact = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    code = models.CharField(max_length=5, unique=True, default=generate_code)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

class UserPoint(models.Model):
    user_hash = models.CharField(max_length=255, unique=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user_hash

    class Meta:
        verbose_name = _("User Point")
        verbose_name_plural = _("User Points")

class ActivityLog(models.Model):
    user = models.ForeignKey(UserPoint, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    nonce = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.user} - {self.activity}"

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activity Logs")
