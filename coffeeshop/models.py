import numpy as np
from django.db import models
from django.utils import timezone

class Receipts(models.Model):
    transaction_id = models.IntegerField(blank=False, null=False, editable=False)
    transaction_date = models.DateField(auto_now_add=True, editable=False)
    transaction_time = models.TimeField(default=timezone.now, editable=False)
    customer_id = models.IntegerField(blank=False, null=False, default=np.random.randint(100), editable=False)
    order = models.IntegerField(blank=False, null=False, default=1, editable=False)
    product_id = models.IntegerField(blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False)
    unit_price = models.FloatField()
    line_item_amount = models.FloatField(editable=False) 

    def __str__(self):
        return f'{self.transaction_id} - {self.quantity} - {self.line_item_amount}'
    
    class Meta:
        verbose_name_plural = 'Receipts'

    # Overrides save method
    def save(self, *args, **kwargs):
        # Assigns an incremental value to 'transaction_id' if not provided
        if self.transaction_id is None:
            last_instance = Receipts.objects.aggregate(models.Max('transaction_id'))
            last_value = last_instance['transaction_id__max']

            if last_value is not None:
                self.transaction_id = last_value + 1
            else:
                self.transaction_id = 1

        # Calculates 'line_item_amount'
        self.line_item_amount = float(self.quantity) * self.unit_price
        super().save(*args, **kwargs)


class Products(models.Model):
    product_id = models.IntegerField(blank=False, null=False)
    product_group = models.CharField(max_length=20, blank=False)
    product_category = models.CharField(max_length=20, blank=False)
    product_type = models.CharField(max_length=40, blank=False)
    product = models.CharField(max_length=40, blank=False)
    product_description = models.CharField(max_length=100, blank=False)
    unit_of_measure = models.CharField(max_length=10, blank=False)
    current_retail_price = models.FloatField()

    def __str__(self):
        return self.product


