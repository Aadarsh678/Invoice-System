from django.shortcuts import get_object_or_404, render,redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.forms import modelformset_factory
from django.http import FileResponse
from django.template.loader import render_to_string
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
import pandas as pd
from django.http import HttpResponse
from .models import Bill, BillItem
from .page import paginate_queryset


def home(request):
    return render(request,'home.html')


def manage_bill(request):
    pass


def bill_list(request):
    bills = Bill.objects.all()
    page_obj = paginate_queryset(request,bills)
    context = {'page_obj': page_obj}
    return render(request, 'list_bill.html', context)

def category_list(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    categories = Category.objects.all()
    page_obj = paginate_queryset(request,categories)
    return render(request, 'add_category.html', {'form': form,'page_obj': page_obj})
    

def category_delete(request, id):
    category_del = Category.objects.get(id=id)
    category_del.delete()
    return redirect('category_list')

def product_list(request):
    if request.method == 'POST':
        formp = ProductForm(request.POST)
        if formp.is_valid():
            formp.save()
            return redirect('product_list')
    else:
        formp = ProductForm()
    
    products = Product.objects.all()

    page_obj = paginate_queryset(request,products)
    return render(request, 'add_product.html', {'formp': formp, 'page_obj': page_obj})


def product_delete(request, id):
    product_del = Product.objects.get(id=id)
    product_del.delete()
    return redirect('product_list')

def product_update(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        formp = ProductForm(request.POST, instance=product)
        if formp.is_valid():
            formp.save()
            return redirect('product_list')
    else:
        formp = ProductForm(instance=product)
    return render(request, 'update_product.html', {'formp': formp})

def create_customer(request):
    if request.method == 'POST':
        formc = CustomerForm(request.POST)
        if formc.is_valid():
            formc.save()
            return redirect('create_customer')
    else:
        formc = CustomerForm()
    
    customers = Customer.objects.all()
    
    page_obj = paginate_queryset(request,customers)
    return render(request, 'add_customer.html', {'formc': formc, 'page_obj': page_obj})
    

def customer_delete(request, id):
    customer_del = Customer.objects.get(id=id)
    customer_del.delete()
    return redirect('create_customer')

def customer_update(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        formc = CustomerForm(request.POST, instance=customer)
        if formc.is_valid():
            formc.save()
            return redirect('create_customer')
    else:
        formc = CustomerForm(instance=customer)
    return render(request, 'update_customer.html', {'formc': formc})



def bill_delete(request, id):
    bill_del = Bill.objects.get(id=id)
    bill_del.delete()
    return redirect('bill_list')


def create_bill(request):
    BillItemFormSet = modelformset_factory(BillItem, form=BillItemForm, extra=1)
    
    if request.method == 'POST':
        formb = BillForm(request.POST)
        formset = BillItemFormSet(request.POST, queryset=BillItem.objects.none())
        
        if formb.is_valid() and formset.is_valid():
            bill = formb.save(commit=False)
            if 'delivery' not in request.POST:
                bill.shipping_cost = None
            bill.save()
            
            for form in formset:
                if form.cleaned_data:  
                    bill_item = form.save(commit=False)
                    bill_item.bill = bill
                    bill_item.save()
            
            bill.generate_pdf()
            
            return redirect('bill_list')  
    else:
        formb = BillForm()
        formset = BillItemFormSet(queryset=BillItem.objects.none())

    return render(request, 'create_bill.html', {'formb': formb, 'formset': formset})

def view_pdf(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if not bill.pdf:
        bill.generate_pdf()
    response = FileResponse(bill.pdf, as_attachment=False, filename=f"invoice_{bill.invoice_number}.pdf")
    return response

def send_bill_email(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    bill.send_email_with_pdf()
    messages.success(request, 'Mail sent successfully')
    return HttpResponseRedirect(reverse('bill_list'))


def bill_update(request, id):
    bill = get_object_or_404(Bill, id=id)
    products = BillItem.objects.filter(bill=bill)
    if request.method == 'POST':
        formb = BillForm(request.POST, instance=bill, update=True)
        if formb.is_valid():
            formb.save()
            return redirect('bill_list')
    else:
        formb = BillForm(instance=bill, update=True)
    return render(request, 'update_bill.html', {'formb': formb, 'products': products})
 
    
def details(request, id):
    mybill = Bill.objects.get(id=id)
    bill_items = BillItem.objects.filter(bill=mybill)
    template = loader.get_template('details.html')
    context = {
        'mybill': mybill,
        'bill_items': bill_items,
    }
    return HttpResponse(template.render(context, request))

def download_bill_pdf(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if not bill.pdf:
        bill.generate_pdf()
    response = FileResponse(bill.pdf, as_attachment=True, filename=f"invoice_{bill.invoice_number}.pdf")
    return response



def export_bills_csv(request):
    bills = Bill.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bills.csv"'

    writer = csv.writer(response)
    writer.writerow(['Invoice Number', 'Customer', 'Total Amount', 'Shipping Cost', 'Paid'])

    for bill in bills:
        total_amount = bill.total_price()
        writer.writerow([bill.invoice_number, bill.customer.name, total_amount, bill.shipping_cost, bill.paid])

    return response

def export_bills_excel(request):
    bills = Bill.objects.all()

    data = []
    for bill in bills:
        total_amount = bill.total_price()
        data.append({
            'Invoice Number': bill.invoice_number,
            'Customer': bill.customer.name,
            'Total Amount': total_amount,
            'Shipping Cost': bill.shipping_cost,
            'Paid': bill.paid
        })

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="bills.xlsx"'

    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Bills')

    return response














