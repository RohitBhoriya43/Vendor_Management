from django.db import models


class PurchaseOrderStatus(models.TextChoices):
    pending = 'pending'
    completed = 'completed'
    canceled = 'canceled'