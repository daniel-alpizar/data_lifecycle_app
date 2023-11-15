import csv
import io
from datetime import datetime
from django import forms
from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import path
from .models import Customers, Datawarehouse, Orders, Products, Rawdata


class CsvCustomersForm(forms.Form):
    csv_customers = forms.FileField

class CustomersAdmin(admin.ModelAdmin):
    list_display = ('customer_id','home_store','customer_name','customer_email','customer_since')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls  = [path('csv-customers/', self.csv_customers)]
        return custom_urls + urls

    def csv_customers(self, request):
        if request.method == 'POST' and 'csv_file' in request.FILES:
            Customers.objects.all().delete()

            csv_file = request.FILES['csv_file']

            if not csv_file.name.lower().endswith('.csv'):
                messages.error(request, 'Error - Not a csv file')

            else:
                data_set = csv_file.read().decode('utf-8').splitlines()
                csv_reader = csv.reader(data_set)
            
                headers = next(csv_reader)

                customers_list = []
                
                for column in csv_reader:
                    customer_id = column[0]
                    home_store = column[1]
                    customer_name = column[2]
                    customer_email = column[3]
                    customer_since = datetime.strptime(str(column[4]), '%m/%d/%Y').strftime('%Y-%m-%d')

                    # Use bulk_create to insert the list of Customers objects into the database
                    customers = Customers(
                        customer_id = customer_id,
                        home_store = home_store,
                        customer_name = customer_name,
                        customer_email = customer_email,
                        customer_since = customer_since,
                    )
                    customers_list.append(customers)
                Customers.objects.bulk_create(customers_list)

                messages.info(request, 'CSV file imported successfully')
                return redirect('admin:index')                

        elif request.method == 'POST' and 'delete_data' in request.POST:
            # This is for erasing all rows in the database
            Customers.objects.all().delete()
            messages.warning(request, 'Records deleted')
            return redirect('admin:index')

        form = CsvCustomersForm()
        context = {'form': form}
        return render(request, 'admin/csv_customers.html', context)


class CsvProductForm(forms.Form):
    csv_products = forms.FileField

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_id','product_group','product_category','product_type',
                    'product','unit_of_measure','current_retail_price')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('csv-products/', self.csv_products)]
        return new_urls + urls

    def csv_products(self, request):
        if request.method == 'POST':
            Products.objects.all().delete()

            csv_file = request.FILES['csv_file']

            if not csv_file.name.lower().endswith('.csv'):
                messages.error(request, 'Error - Not a csv file')

            else:
                data_set = csv_file.read().decode('utf-8')
                io_string = io.StringIO(data_set)
                next(io_string)

                for column in csv.reader(io_string):
                    Products.objects.update_or_create(
                        product_id=column[0],
                        product_group=column[1],
                        product_category=column[2],
                        product_type=column[3],
                        product=column[4],
                        unit_of_measure=column[6],
                        current_retail_price=column[8].replace('$', ''),
                        )
                    
                messages.info(request, 'CSV file imported successfully')
                return redirect('admin:index')

        form = CsvProductForm()
        context = {'form': form}
        return render(request, 'admin/csv_products.html', context)


class CsvRawdataForm(forms.Form):
    csv_rawdata = forms.FileField

class RawdataAdmin(admin.ModelAdmin):
    list_display = ('transaction_id','transaction_date','transaction_time','customer_id',
                    'order','product','quantity','unit_price','line_item_amount')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls  = [path('csv-rawdata/', self.csv_rawdata)]
        return custom_urls + urls

    def csv_rawdata(self, request):
        if request.method == 'POST' and 'csv_file' in request.FILES:
            Rawdata.objects.all().delete()

            csv_file = request.FILES['csv_file']

            if not csv_file.name.lower().endswith('.csv'):
                messages.error(request, 'Error - Not a csv file')

            else:
                data_set = csv_file.read().decode('utf-8').splitlines()
                csv_reader = csv.reader(data_set)
            
                headers = next(csv_reader)

                rawdata_list = []
                
                for column in csv_reader:
                    transaction_id = column[0]
                    transaction_date = datetime.strptime(str(column[1]), '%m/%d/%Y').strftime('%Y-%m-%d')
                    transaction_time = column[2]
                    customer_id = column[5]
                    order = column[7]
                    product_id = column[9]
                    quantity = column[10]
                    line_item_amount = column[11]
                    unit_price = column[12]

                    # Use bulk_create to insert the list of Rawdb objects into the database
                    rawdata = Rawdata(
                        transaction_id = transaction_id,
                        transaction_date = transaction_date,
                        transaction_time = transaction_time,
                        customer_id = customer_id,
                        order = order,
                        product_id = product_id,
                        quantity = quantity,
                        line_item_amount = line_item_amount,
                        unit_price = unit_price
                    )
                    rawdata_list.append(rawdata)
                Rawdata.objects.bulk_create(rawdata_list)

                messages.info(request, 'CSV file imported successfully')
                return redirect('admin:index')                

        elif request.method == 'POST' and 'delete_data' in request.POST:
            # This is for erasing all rows in the database
            Rawdata.objects.all().delete()
            messages.warning(request, 'Records deleted')
            return redirect('admin:index')

        form = CsvRawdataForm()
        context = {'form': form}
        return render(request, 'admin/csv_rawdata.html', context)


admin.site.register(Customers, CustomersAdmin)
admin.site.register(Datawarehouse)
admin.site.register(Orders)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Rawdata, RawdataAdmin)
