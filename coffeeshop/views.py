import csv
from datetime import datetime
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Receipts
from .pandas import df_format
from .forms import CoffeeShopOrderForm


def home(request):
    template = 'coffeeshop/base.html'
    context = {'receipts': Receipts.objects.all()}

    return render(request, template, context)


def TransactionalView(request):
    '''Import CSV to database and render as DataFrame'''

    template = 'coffeeshop/transactional_db.html'

    # Database info card
    records = Receipts.objects.count()
    context = {'records': records, 'title': 'Transactional Database'}

    if request.method == 'GET' and 'render_data' in request.GET:
        # This is for rendering the data
        receipts_query = Receipts.objects.all()[:20]

        if receipts_query.exists():
            # Convert the QuerySet to a DataFrame
            df = pd.DataFrame(receipts_query.values())
        else:
            # Get column names from the model's fields
            model_fields = Receipts._meta.get_fields()
            column_names = [field.name for field in model_fields if field.concrete]
            df = pd.DataFrame(columns=column_names)

        df = df_format(df)
        df = df.to_html()
        context['df_render'] = df

        return render(request, template, context)


    elif request.method == 'POST' and 'csv_file' in request.FILES:
        # This is for importing the CSV file
        try:
            csv_file = request.FILES['csv_file']

            if not csv_file.name.lower().endswith('.csv'):
                messages.warning(request, 'Error - Not a csv file')
                return render(request, template, context)

            data = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(data)

            # Skips header row
            headers = next(csv_reader)

            receipt_list = []
            
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

                # Use bulk_create to insert the list of Receipts objects into the database
                receipt = Receipts(
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
                receipt_list.append(receipt)
            Receipts.objects.bulk_create(receipt_list)

            messages.info(request, 'CSV file imported successfully')
            return redirect('/transactional-db/')

        except:
            messages.warning(request, 'No file selected')

        return render(request, template, context)
    
    elif request.method == 'POST' and 'delete' in request.POST:
        # This is for erasing all rows in the database
        Receipts.objects.all().delete()
        messages.warning(request, 'Records deleted')
        return redirect('/transactional-db')

    else:
        return render(request, template, context)

# Simple order form
def OrderFormView(request):
    if request.method == 'POST':
        form = CoffeeShopOrderForm(request.POST)
        if form.is_valid():
            instance = form.save()
            transaction_id = instance.transaction_id
            messages.info(request,  f'Your order with transaction ID {transaction_id} has been successfully placed!')
            # Redirect to a success page or show a success message
    else:
        form = CoffeeShopOrderForm()

    return render(request, 'coffeeshop/order_form.html', {'form': form})
