from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Powder, Customer, Region, Purchase
from .forms import RegionForm, CustomerForm, PurchaseForm


def main_page(request):
    powders = Powder.objects.all()
    regions = Region.objects.all()
    customers = Customer.objects.select_related('region').all()

    return render(request, 'store/base.html', {
        'powders': powders,
        'regions': regions,
        'customers': customers,
    })


# Получение списка покупателей для региона
def customers_by_region(request, region_id):
    region = get_object_or_404(Region, id=region_id)
    customers = Customer.objects.filter(region=region)
    customers_data = [
        {'name': customer.name, 'region': region.name}
        for customer in customers
    ]
    return JsonResponse(customers_data, safe=False)


# ===== Region Views =====
def region_list(request):
    regions = Region.objects.all()
    return render(request, 'store/region_list.html', {'regions': regions})


def region_create(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:main_page')
    else:
        form = RegionForm()
    return render(request, 'store/region_form.html', {'form': form})


def region_edit(request, id):
    region = get_object_or_404(Region, id=id)
    if request.method == 'POST':
        form = RegionForm(request.POST, instance=region)
        if form.is_valid():
            form.save()
            return redirect('store:region_list')
    else:
        form = RegionForm(instance=region)
    return render(request, 'store/region_form.html', {'form': form})


def region_delete(request, id):
    region = get_object_or_404(Region, id=id)
    if request.method == 'POST':
        region.delete()
    return redirect('store:main_page')


# ===== Customer Views =====
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'store/customer_list.html', {'customers': customers})


def customer_list_view(request):
    customers = Customer.objects.all()  # Fetch all customers
    paginator = Paginator(customers, 10)  # Show 10 customers per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the corresponding page

    return render(request, 'store/customer_list.html', {'page_obj': page_obj})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:main_page')
    else:
        form = CustomerForm()
    return render(request, 'store/customer_form.html', {'form': form})


def customer_edit(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('store:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'store/customer_form.html', {'form': form})


def customer_delete(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        customer.delete()
    return redirect('store:main_page')


def fetch_customers(request, region_id):
    customers = Customer.objects.filter(region_id=region_id)
    customer_data = [
        {"name": customer.name, "region": customer.region.name}
        for customer in customers
    ]
    return JsonResponse(customer_data, safe=False)


# ===== Purchase Views =====
def purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:purchase_list')
    else:
        form = PurchaseForm()
    return render(request, 'store/purchase_create.html', {'form': form})


from django.shortcuts import render
from .models import Purchase


def purchase_list(request):
    purchases = Purchase.objects.select_related('customer', 'powder').all()

    customer_total_powder = {}

    for purchase in purchases:
        # Используем имя клиента как ключ словаря
        customer_name = purchase.customer.name
        if customer_name not in customer_total_powder:
            customer_total_powder[customer_name] = 0
        customer_total_powder[customer_name] += purchase.quantity

    return render(request, 'store/purchase_list.html', {
        'purchases': purchases,
        'customer_total_powder': customer_total_powder
    })



def purchase(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        powder_id = request.POST.get('powder_id')
        powder = get_object_or_404(Powder, id=powder_id)

        # Создаем заказ
        order = Order.objects.create(customer=customer, powder=powder)
        order.save()

        return HttpResponse("Order has been placed successfully!")

    powders = Powder.objects.all()
    return render(request, 'store/purchase.html', {
        'customer': customer,
        'powders': powders
    })
