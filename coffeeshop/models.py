from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from users.models import Profile


class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    home_store = models.IntegerField(blank=False, null=False, default=1, editable=False)
    customer_name = models.CharField(max_length=100, blank=False)
    customer_email = models.EmailField(max_length=100, blank=True)
    customer_since = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.customer_name}'

    class Meta:
        verbose_name_plural = 'Customers'
       

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_group = models.CharField(max_length=20, blank=False)
    product_category = models.CharField(max_length=20, blank=False)
    product_type = models.CharField(max_length=40, blank=False)
    product = models.CharField(max_length=40, blank=False)
    unit_of_measure = models.CharField(max_length=10, blank=False)
    current_retail_price = models.FloatField()

    def __str__(self):
        return f'{self.product}-{self.unit_of_measure}'
    
    class Meta:
        verbose_name_plural = 'Products'


class Orders(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_date = models.DateField(auto_now_add=True, editable=False)
    transaction_time = models.TimeField(default=timezone.now, editable=False)
    customer = models.ForeignKey(Profile, blank=False, null=False, on_delete=models.CASCADE)
    order = models.IntegerField(blank=False, null=False, editable=False)
    product = models.ForeignKey(Products, blank=False, null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(1)])
    unit_price = models.FloatField(validators=[MinValueValidator(0)])
    line_item_amount = models.FloatField() 

    def __str__(self):
        return f'{self.transaction_id} - {self.quantity}'
    
    class Meta:
        verbose_name_plural = 'Orders'

    # Overrides save method
    def save(self, *args, **kwargs):
        # # Assigns an incremental value to 'transaction_id' if not provided
        # if self.transaction_id is None:
        #     last_instance = Orders.objects.aggregate(models.Max('transaction_id'))
        #     last_value = last_instance['transaction_id__max']

        #     if last_value is not None:
        #         self.transaction_id = last_value + 1
        #     else:
        #         self.transaction_id = 1

        # Calculates 'line_item_amount'
        self.line_item_amount = float(self.quantity) * self.unit_price
        super().save(*args, **kwargs)


class Rawdata(models.Model):
    transaction_id = models.IntegerField(blank=False, null=False)
    transaction_date = models.DateField(auto_now_add=True, editable=False)
    transaction_time = models.TimeField(default=timezone.now, editable=False)
    customer_id = models.IntegerField(blank=False, null=False, default=99, editable=False)
    order = models.IntegerField(blank=False, null=False, default=1, editable=False)
    product = models.ForeignKey(Products, blank=False, null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False)
    unit_price = models.FloatField()
    line_item_amount = models.FloatField(editable=False) 

    def __str__(self):
        return f'{self.transaction_id} - {self.quantity}'
    
    class Meta:
        verbose_name_plural = 'Rawdata'


class Datawarehouse(models.Model):
    transaction_id = models.IntegerField(blank=False, null=False)
    transaction_date = models.DateField(auto_now_add=True, editable=False)
    transaction_time = models.TimeField(default=timezone.now, editable=False)
    customer_id = models.IntegerField(blank=False, null=False, default=99, editable=False)
    order = models.IntegerField(blank=False, null=False, default=1, editable=False)
    product = models.ForeignKey(Products, blank=False, null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False)
    unit_price = models.FloatField()
    line_item_amount = models.FloatField(editable=False) 

    def __str__(self):
        return f'{self.transaction_id} - {self.quantity}'
    
    class Meta:
        verbose_name_plural = 'Datawarehouse'