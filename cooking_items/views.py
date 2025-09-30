from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CookingItem
from .forms import CookingItemForm

@login_required
def cooking_item_list(request):
    items = CookingItem.objects.all()
    return render(request, 'cooking_items/cooking_item_list.html', {'items': items})

@login_required
def add_cooking_item(request):
    if request.method == 'POST':
        form = CookingItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cooking_item_list')
    else:
        form = CookingItemForm()
    return render(request, 'cooking_items/add_cooking_item.html', {'form': form})

@login_required
def edit_cooking_item(request, pk):
    item = get_object_or_404(CookingItem, pk=pk)
    if request.method == 'POST':
        form = CookingItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('cooking_item_list')
    else:
        form = CookingItemForm(instance=item)
    return render(request, 'cooking_items/add_cooking_item.html', {'form': form})

@login_required
def delete_cooking_item(request, pk):
    item = get_object_or_404(CookingItem, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect('cooking_item_list')
    return render(request, 'cooking_items/cooking_iteam_delete.html', {'item': item})

