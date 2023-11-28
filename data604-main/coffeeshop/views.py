import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Max
from django.forms import modelformset_factory
from django.forms.widgets import Select   
from django.http import JsonResponse
from django.shortcuts import render, redirect
import plotly.express as px
from plotly.offline import plot
from .models import Datawarehouse, Orders, Products, Profile, Rawdata, Customers, Archive
from .pandas import df_format
from .forms import CoffeeShopOrderForm
from .plotly_app import plotly_treemap
from .dash_test import dash_test
from users.decorators import allowed_users
from itertools import groupby
from operator import attrgetter
from collections import OrderedDict
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404



# @admin_only
def Home(request):
    template = 'coffeeshop/home.html'
    context = {}

    return render(request, template, context)


@login_required(login_url='login')
def OrdersDBView(request):
    '''Renders Order table as DataFrame'''

    template = 'coffeeshop/orders_db.html'
    database_title = 'Transactional Database'

    # Database info card
    records = Orders.objects.count()

    # Aggregate and find largest transaction by total amount
    transactions_total = Orders.objects.values('order').annotate(total_amount=Sum('line_item_amount'))
    largest_transaction = transactions_total.aggregate(largest_amount=Max('total_amount'))

    if largest_transaction['largest_amount'] is not None:
        # Format the largest amount as a currency string
        largest_amount = "${:,.2f}".format(largest_transaction['largest_amount'])
    else:
        largest_amount = "N/A"


    # Calculate the most popular item
    popular_items = Orders.objects.values('product__product').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')
    most_popular_item = popular_items.first()

    if most_popular_item:
        most_popular_item = most_popular_item['product__product']
    else:
        most_popular_item = "N/A"


    # Aggregate the total spent by each customer
    customer_spending = Orders.objects.values('customer__user__username').annotate(total_spent=Sum('line_item_amount')).order_by('-total_spent')
    best_customer = customer_spending.first()

    if best_customer:
        best_customer_name = best_customer['customer__user__username']
        best_customer_spent = best_customer['total_spent']
    else:
        best_customer_name = "N/A"
        best_customer_spent = 0


    context = {
        'title': 'Orders Database',
        'records': records,
        'largest':largest_amount,
        'most_popular_item': most_popular_item,
        'best_customer_name': best_customer_name,
        'best_customer_spent': best_customer_spent}
    

    if request.method == 'GET' and 'render_data' in request.GET:
        # This is for rendering the data
        orders_query = Orders.objects.all()[:20]

        if orders_query.exists():
            # Convert the QuerySet to a DataFrame
            df = pd.DataFrame(orders_query.values())
        else:
            # Get column names from the model's fields
            model_fields = Orders._meta.get_fields()
            column_names = [field.name for field in model_fields if field.concrete]
            df = pd.DataFrame(columns=column_names)

        df = df_format(df, database_title)
        df = df.to_html()
        context['df_render'] = df

        return render(request, template, context)

    else:
        return render(request, template, context)


@login_required(login_url='login')
def RawDataDBView(request):
    '''Import CSV to database and render as DataFrame'''

    template = 'coffeeshop/rawdata_db.html'
    database_title = 'Raw Transactional Database'

    # Database info card
    records = Rawdata.objects.count()
    columns = len(Rawdata._meta.get_fields())

    context = {'records': records, 'columns':columns, 'title': 'Raw Data Database'}

    if request.method == 'GET' and 'render_data' in request.GET:
        # This is for rendering the data
        orders_query = Rawdata.objects.all()[:20]

        if orders_query.exists():
            # Convert the QuerySet to a DataFrame
            df = pd.DataFrame(orders_query.values())
            df.drop(df.columns[0], axis=1, inplace=True)
        else:
            # Get column names from the model's fields
            model_fields = Rawdata._meta.get_fields()
            column_names = [field.name for field in model_fields if field.concrete]
            df = pd.DataFrame(columns=column_names)

        df = df_format(df, database_title)
        df = df.to_html()
        context['df_render'] = df

        return render(request, template, context)

    else:
        return render(request, template, context)


@login_required(login_url='login')
def OrderFormSetView(request):
    '''Self-ordering kiosk with multiple order lines'''

    template = 'coffeeshop/order_form.html'
    context = {'title': 'Order Form'}

    if request.method == 'POST':
        MyModelFormSet = modelformset_factory(Orders, form=CoffeeShopOrderForm, extra=0)
        formset = MyModelFormSet(request.POST, queryset=Orders.objects.none())

        # Get the profile of the currently logged-in user
        user_profile = Profile.objects.get(user=request.user)

        if formset.is_valid():
            # Get the highest current order number and increment by 1
            max_order = Orders.objects.aggregate(Max('order'))['order__max'] or 0
            max_order += 1

            instances = formset.save(commit=False)  # Create instances but don't save to the database yet

            for instance in instances:
                instance.order = max_order
                instance.customer = user_profile  # Set the customer field to the current user's profile
                instance.save()

            messages.info(request,  f'Your order with transaction ID {max_order} has been successfully placed!')
            return redirect('order_form')

        else:
            context['formset'] = formset

    else:
        MyModelFormSet = modelformset_factory(Orders, form=CoffeeShopOrderForm, extra=1)
        formset = MyModelFormSet(queryset=Orders.objects.none())
        context['formset'] = formset
        context['customer'] = request.user.first_name

    products = Products.objects.all().order_by('product_category', 'product')
    grouped_products = {k: list(g) for k, g in groupby(products, key=attrgetter('product_category'))}
    # Desired order of categories
    category_order = ['Coffee', 'Tea', 'Chocolate', 'Bakery']

    # Create an ordered dictionary based on the desired category order
    ordered_grouped_products = OrderedDict((cat, grouped_products[cat]) for cat in category_order if cat in grouped_products)

    context['grouped_products'] = ordered_grouped_products

    return render(request, template, context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def ETLView(request):
    '''Clean and concatenates Orders and Rawdata'''

    template = 'coffeeshop/etl_process.html'
    database_title = 'Data Warehouse'

    def info_card():
        # Database info card
        records_orders = Orders.objects.count()
        records_rawdata = Rawdata.objects.count()
        records_datawarehouse = Datawarehouse.objects.count()

        context = {'records_orders': records_orders, 'records_rawdata':records_rawdata,
                'records_datawarehouse': records_datawarehouse,'title': 'ETL Process'}
        
        return context

    if request.method == 'GET' and 'etl_process' in request.GET:

        data_warehouse_entries = []

        # Stack data from Orders
        for order in Orders.objects.all():
            data_warehouse_entries.append(
                Datawarehouse(
                    transaction_id=order.transaction_id,
                    transaction_date=order.transaction_date,
                    transaction_time=order.transaction_time,
                    customer_id=order.customer_id,
                    order=order.order,
                    product=order.product,
                    quantity=order.quantity,
                    unit_price=order.unit_price,
                    line_item_amount=order.line_item_amount
                )
            )

        # Stack data from Rawdata
        for rawdata in Rawdata.objects.all():
            data_warehouse_entries.append(
                Datawarehouse(
                    transaction_id=rawdata.transaction_id,
                    transaction_date=rawdata.transaction_date,
                    transaction_time=rawdata.transaction_time,
                    customer_id=rawdata.customer_id,
                    order=rawdata.order,
                    product=rawdata.product,
                    quantity=rawdata.quantity,
                    unit_price=rawdata.unit_price,
                    line_item_amount=rawdata.line_item_amount
                )
            )

        # Bulk create Datawarehouse entries
        Datawarehouse.objects.bulk_create(data_warehouse_entries)
        context = info_card()
        return render(request, template, context)

    elif request.method == 'GET' and 'render_data' in request.GET:
        # This is for rendering the data
        orders_query = Datawarehouse.objects.all()[:20]

        if orders_query.exists():
            # Convert the QuerySet to a DataFrame
            df = pd.DataFrame(orders_query.values())
            df.drop(df.columns[0], axis=1, inplace=True)
        else:
            # Get column names from the model's fields
            model_fields = Datawarehouse._meta.get_fields()
            column_names = [field.name for field in model_fields if field.concrete]
            df = pd.DataFrame(columns=column_names)

        df = df_format(df, database_title)
        df = df.to_html()
        context = info_card()
        context['df_render'] = df

        return render(request, template, context)

    else:
        context = info_card()
        return render(request, template, context)
    

@login_required(login_url='login')
def TreemapView(request):
    '''Checks for data in Datawarehouse and renders a Plotly chart'''
    if Datawarehouse.objects.all().exists():
        orders_query = Datawarehouse.objects.all()
        df = pd.DataFrame(orders_query.values())
        
        # Apply Treemap function 
        fig = plotly_treemap(df)

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        context = {'treemap': plot_div}
        return render(request, 'coffeeshop/treemap.html', context)  
    
    else:
        messages.info(request, 'No data available')
        return render(request, 'coffeeshop/treemap.html')
    

@login_required(login_url='login')
def DashView(request):
    '''Checks for data in Datawarehouse and renders a Plotly Dash application'''
    if Datawarehouse.objects.all().exists():
        context = {'data_exists': 'data_exists'}
        return render(request, 'coffeeshop/dash.html', context)
    else:
        messages.info(request, 'No data available')
        context = {'data_exists': None}
        return render(request, 'coffeeshop/dash.html', context)
    

def get_product_price(request):
    '''Function to dynamically fetch product prices for order forms using AJAX'''
    product_id = request.GET.get('product_id')
    if product_id:
        try:
            product = Products.objects.get(pk=product_id)
            return JsonResponse({'price': product.current_retail_price})
        except Products.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'No product ID provided'}, status=400)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def archival_process(request):
    template = 'coffeeshop/archival_process.html'
    
      # Function to provide counts for context
    def info_card():
        records_datawarehouse = Datawarehouse.objects.count()
        records_archive = Archive.objects.count()
        return {'records_datawarehouse': records_datawarehouse,
                'records_archive': records_archive,
                'title': 'Archival Process'}

    
    if request.method == 'POST':
        # Get all Datawarehouse records
        data_warehouse_records = Datawarehouse.objects.all()
        
        # Create Archive instances for each Datawarehouse record
        archive_entries = [
            Archive(
                transaction_id=record.transaction_id,
                transaction_date=record.transaction_date,
                transaction_time=record.transaction_time,
                customer_id=record.customer_id,
                order=record.order,
                product=record.product,
                quantity=record.quantity,
                unit_price=record.unit_price,
                line_item_amount=record.line_item_amount
            )
            for record in data_warehouse_records
        ]
        
        # Save all entries to the Archive model
        Archive.objects.bulk_create(archive_entries)
        
        # Optionally, delete the records from Datawarehouse if you want to clear them after archiving
        # data_warehouse_records.delete()
        
        context = info_card()
        messages.success(request, "Datawarehouse records have been successfully archived.")
        # No redirect needed here since we're updating the context below
        # and rendering the same template with new information

    if request.method == 'GET' and 'render_archive_data' in request.GET:
    # Fetch records from the Archive model
        archive_records = Archive.objects.all()

        # Convert the QuerySet to a DataFrame
        df = pd.DataFrame(list(archive_records.values()))

        # You might want to process the DataFrame to customize its appearance,
        # for example by renaming columns or formatting data.

        # Convert the DataFrame to an HTML table
        df_render = df.to_html(classes='table table-bordered', index=False)
        
        # Create or update the context with the HTML table
        context = info_card()
        context['df_render'] = df_render
    else:
        # If 'render_archive_data' isn't in the request, just provide the counts
        context = info_card()

    # Render the template with context
    return render(request, template, context)

@login_required
def customer_list_view(request):
    template = 'coffeeshop/customer_list.html'
    
    # Context to hold the data
    context = {'records': Customers.objects.count(), 'title': 'Customers Database'}
    
    if request.method == 'GET' and 'render_data' in request.GET:
        # Query the Customers model for data
        customer_data = Customers.objects.all()
        
        # Check if there is any customer data
        if customer_data.exists():
            # Convert the QuerySet to a DataFrame
            df = pd.DataFrame(customer_data.values())

            # Get CSRF token
            csrf_token = get_token(request)

            # Add a delete button column as a single line string
            df['delete'] = df.apply(lambda row: f"<form method='post' action='{reverse('delete_customer', args=[row['customer_id']])}'><input type='hidden' name='csrfmiddlewaretoken' value='{csrf_token}'><button type='submit' class='btn btn-danger delete-btn' onclick='return confirm(\"Are you sure you want to delete this customer?\");'>Delete</button></form>", axis=1)
            # Render the DataFrame to HTML
            df_render = df.to_html(classes='table table-bordered', index=False, escape=False)
            df_render = df_render.replace('\n', '')  # Remove newline characters
            context['df_render'] = df_render
        else:
            context['df_render'] = 'No customers found.'

    return render(request, template, context)

@login_required
@require_POST
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customers, customer_id=customer_id)
    customer.delete()
    messages.success(request, f'Customer with ID {customer_id} has been deleted.')
    return redirect('customer_list')