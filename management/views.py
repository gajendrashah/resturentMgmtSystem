from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Sum, F
from .forms import CustomerAdvanceForm, PurchaseForm
from .models import Cart, CartItem, MenuItem, Sale, Category, SubCategory, Table, Purchase, Customer, customerAdvance

def print_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'admin/sales/print_sale.html', {'sale': sale})

def dashboard(request):
    return render(request, 'management/dashboard.html')


def orderManagement(request):
    tables = Table.objects.all()
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    orders = Cart.objects.filter(table__isnull=False)
    cart_items = CartItem.objects.filter(cart__table__isnull=False)
    sub_catagory = SubCategory.objects.all()
    
    context = {'tables': tables, 
               'categories': categories, 
               'menu_items': menu_items, 
               'orders': orders, 
               'sub_catagory': sub_catagory,
               'cart_items': cart_items}
    return render(request, 'management/pages/OrderManagement.html', context )




@csrf_exempt
def create_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_id = data.get('table')
            items = data.get('items', [])

            if not table_id or not items:
                return JsonResponse({'error': 'Table and items are required'}, status=400)

            # Ensure table exists
            table = get_object_or_404(Table, id=table_id)

            cart = Cart.objects.create(table=table)

            for item in items:
                menu_item = get_object_or_404(MenuItem, id=item.get('menu_item'))
                quantity = item.get('quantity', 1)
                CartItem.objects.create(cart=cart, menu_item=menu_item, quantity=quantity)

            return JsonResponse({'message': 'Order created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def PurchaseItems(request):
    purchases = Purchase.objects.all()
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Purchase successful'}, status=200)
    else:
        form = PurchaseForm()
        
    return render(request, 'management/pages/PurchaseItems.html', {'form': form, 'purchases': purchases})

def edit_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Purchase updated successfully'}, status=200)
        return JsonResponse({'error': 'Invalid form data'}, status=400)
    else:
        form = PurchaseForm(instance=purchase)
        return JsonResponse({
            'id': purchase.id,
            'item_name': purchase.item_name,
            'quantity': purchase.quantity,
            'total_cost': str(purchase.total_cost),
            'bill_number': purchase.bill_number,
            'remarks': purchase.remarks
        })

def delete_purchase(request, purchase_id):
    if request.method == 'POST':
        purchase = get_object_or_404(Purchase, id=purchase_id)
        purchase.delete()
        return JsonResponse({'message': 'Purchase deleted successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def room_order(request):
    customers = Customer.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    menu_items = MenuItem.objects.all()
    orders = Cart.objects.filter(customer__isnull=False)
    cart_items = CartItem.objects.filter(cart__customer__isnull=False)

    context = {'customers': customers, 'categories': categories, 'menu_items': menu_items, 'orders': orders, 'cart_items': cart_items, 'subcategories': subcategories}
    return render(request, 'management/pages/roomOrder.html', context)
@csrf_exempt
def create_order_room(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            customer_id = data.get('customer')
            items = data.get('items', [])

            if not customer_id or not items:
                return JsonResponse({'error': 'Customer and items are required'}, status=400)

            # Ensure customer exists
            customer = get_object_or_404(Customer, id=customer_id)

            cart = Cart.objects.create(customer=customer)

            for item in items:
                menu_item = get_object_or_404(MenuItem, id=item.get('menu_item'))
                quantity = item.get('quantity', 1)
                CartItem.objects.create(cart=cart, menu_item=menu_item, quantity=quantity)

            return JsonResponse({'message': 'Order created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def roomDetail(request):
    customers = Customer.objects.all()
    advance = customerAdvance.objects.all()   

    customer_data = []
    for customer in customers:
        # Total Balance = Sum of (quantity * price) from CartItems
        total_balance = CartItem.objects.filter(cart__customer=customer).aggregate(
            total=Sum(F('quantity') * F('menu_item__price'))
        )['total'] or 0

        # Total Advance = Sum of all advances made by the customer
        total_advance = customerAdvance.objects.filter(customers=customer).aggregate(
            total=Sum('Advance')
        )['total'] or 0

        # Total Remaining = Balance - Advance
        total_remaining = total_balance - total_advance

        customer_data.append({
            'customer': customer,
            'total_balance': total_balance,
            'total_advance': total_advance,
            'total_remaining': total_remaining,
        })
    context = {'customers': customers, 'advance': advance, 'customer_data': customer_data  }
    return render(request, 'management/pages/roomCalculation.html', context)

def add_advance(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        form = CustomerAdvanceForm(request.POST)
        if not form.is_valid():
            return JsonResponse({'success': False, 'errors': form.errors})

        form.save()
        return JsonResponse({'success': True, 'message': 'Advance added successfully!'})
    else:
        form = CustomerAdvanceForm(initial={'customers': customer})

    return render(request, 'management/pages/advance_form.html', {'form': form, 'customer': customer})