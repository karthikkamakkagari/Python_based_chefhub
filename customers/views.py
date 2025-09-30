from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import token_required
from .models import Customer, CustomerIngredientList
from .forms import CustomerForm, CustomerIngredientForm
from ingredients.models import Ingredient
from dishes.models import Dish
from cooking_items.models import CookingItem
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.contrib.auth import logout
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('home')   # 'home' is the name of your home page URL

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            form.save_m2m()
            messages.success(request, "Customer added successfully!")
            return redirect('dashboard')
    else:
        form = CustomerForm()
    return render(request, 'customers/add_customer.html', {'form': form})

@login_required
def generate_ingredient_list(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)
    CustomerIngredientList.objects.filter(customer=customer).delete()  # Clear old list

    for dish in customer.dishes.all():
        for ing in dish.ingredients.all():
            total_qty = ing.quantity * customer.num_persons
            CustomerIngredientList.objects.create(
                customer=customer,
                ingredient=ing,
                total_quantity=total_qty,
                unit=ing.unit
            )

    for ci in customer.cooking_items.all():
        # If needed, we can also add cooking items to ingredient list
        pass

    messages.success(request, "Ingredient list generated successfully!")
    return redirect('dashboard')


@login_required
def download_pdf(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{customer.name}_ingredients.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)
    p.drawString(50, 750, f"Customer: {customer.name}")
    p.drawString(50, 735, f"Phone: {customer.phone}")
    p.drawString(50, 720, f"Address: {customer.address}")
    p.drawString(50, 700, f"Number of Persons: {customer.num_persons}")
    p.drawString(50, 680, "Ingredient List:")

    y = 660
    ingredient_list = CustomerIngredientList.objects.filter(customer=customer)
    for ing in ingredient_list:
        p.drawString(60, y, f"{ing.ingredient.name_en} - {ing.total_quantity} {ing.unit}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 750

    p.showPage()
    p.save()
    return response

@login_required
@token_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            form.save_m2m()
            if request.user.account_type != 'SUPREM':
                request.user.token -= 1
                request.user.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/add_customer.html', {'form': form})

@login_required
@token_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/add_customer.html', {'form': form})




def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})
