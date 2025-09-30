from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from .models import Dish, DishIngredient, UNITS
from .forms import DishForm, DishIngredientForm
from ingredients.models import Ingredient
from django.contrib import messages
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image as OpenpyxlImage
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
import requests
from .models import Dish, DishIngredient, Ingredient
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from openpyxl import load_workbook
import requests
from .models import Dish, Ingredient, DishIngredient

@login_required
def dish_list(request):
    user_lang = getattr(request.user, "preferred_language", "en")
    dishes = Dish.objects.all().order_by('dish_id')
    all_ingredients = Ingredient.objects.all()  # ✅ Pass all ingredients to template

    for dish in dishes:
        dish.display_name = getattr(dish, f"name_{user_lang}", None) or dish.name_en
        dish.display_preparation = getattr(dish, f"preparation_{user_lang}", None) or dish.preparation_en
        dish.display_ingredients = []
        for ing in dish.dishingredient_set.all():
            ing_name = getattr(ing.ingredient, f"name_{user_lang}", None) or ing.ingredient.name_en
            dish.display_ingredients.append({
                'ingredient': ing.ingredient,
                'name': ing_name,
                'quantity': ing.quantity,
                'unit': ing.unit,
                'price': ing.price
            })

    return render(request, 'dishes/dish_list.html', {
        'dishes': dishes,
        'user_lang': user_lang,
        'all_ingredients': all_ingredients  # ✅ Send to template
    })


@login_required
def add_dish(request):
    DishIngredientFormSet = inlineformset_factory(Dish, DishIngredient, form=DishIngredientForm, extra=1, can_delete=True)
    ingredient_list = Ingredient.objects.all()

    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            dish = form.save(commit=False)
            dish.save()
            formset = DishIngredientFormSet(request.POST, instance=dish)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Dish saved successfully.")
                return redirect('dish_list')
    else:
        form = DishForm()
        formset = DishIngredientFormSet(instance=Dish())
        for f in formset.forms:
            if not f.instance.pk:
                f.initial['quantity'] = 1
                f.initial['unit'] = 'N/A'
                f.initial['price'] = 0

    last_dish = Dish.objects.order_by("-id").first()
    next_id = f"D{int(last_dish.dish_id[1:])+1:03d}" if last_dish and last_dish.dish_id.startswith("D") else "D001"

    return render(request, 'dishes/add_dish.html', {
        'form': form,
        'formset': formset,
        'ingredient_list': ingredient_list,
        'units': UNITS,
        'next_id': next_id,
        'title': 'Add Dish'
    })

@login_required
def edit_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    DishIngredientFormSet = inlineformset_factory(Dish, DishIngredient, form=DishIngredientForm, extra=1, can_delete=True)
    ingredient_list = Ingredient.objects.all()

    if request.method == "POST":
        form = DishForm(request.POST, request.FILES, instance=dish)
        formset = DishIngredientFormSet(request.POST, request.FILES, instance=dish)
        if form.is_valid() and formset.is_valid():
            form.save()
            instances = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
            for obj in instances:
                if obj.ingredient:
                    obj.price = obj.ingredient.price
                obj.save()
            messages.success(request, "Dish updated successfully.")
            return redirect('dish_list')
    else:
        form = DishForm(instance=dish)
        formset = DishIngredientFormSet(instance=dish)
        for f in formset.forms:
            if not f.instance.pk:
                f.initial['quantity'] = 1
                f.initial['unit'] = 'N/A'
                f.initial['price'] = 0

    return render(request, 'dishes/add_dish.html', {
        'form': form,
        'formset': formset,
        'ingredient_list': ingredient_list,
        'units': UNITS,
        'next_id': dish.dish_id,
        'title': f'Edit Dish: {dish.name_en}'
    })

@login_required
def delete_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    dish.delete()
    messages.success(request, "Dish deleted successfully.")
    return redirect('dish_list')

@login_required
def ingredient_details(request, pk):
    try:
        ing = Ingredient.objects.get(pk=pk)
        return JsonResponse({"quantity": ing.quantity, "unit": ing.unit, "price": ing.price})
    except Ingredient.DoesNotExist:
        return JsonResponse({}, status=404)

@login_required
def export_dishes(request):
    dishes = Dish.objects.all().prefetch_related("dishingredient_set__ingredient")
    wb = Workbook()
    ws = wb.active
    ws.title = "Dishes"

    headers = [
        'dish_id', 'name_en','name_te','name_ta','name_hi','name_ka',
        'preparation_en','preparation_te','preparation_ta','preparation_hi','preparation_ka',
        'image_url','image','ingredient_name','quantity','unit','price'
    ]
    ws.append(headers)

    for dish in dishes:
        base_data = [
            dish.dish_id,
            dish.name_en, dish.name_te, dish.name_ta, dish.name_hi, dish.name_ka,
            dish.preparation_en, dish.preparation_te, dish.preparation_ta, dish.preparation_hi, dish.preparation_ka,
            dish.image.url if dish.image else "",
            ""
        ]

        if dish.dishingredient_set.exists():
            for di in dish.dishingredient_set.all():
                ing = di.ingredient
                ws.append(base_data + [
                    ing.name_en if ing else "",
                    di.quantity,
                    di.unit,
                    di.price
                ])
        else:
            ws.append(base_data + ["", "", "", ""])

        if dish.image:
            try:
                img = OpenpyxlImage(dish.image.path)
                img.width, img.height = 80, 80
                ws.add_image(img, f'M{ws.max_row}')
            except Exception as e:
                print(f"Error adding image for dish {dish.dish_id}: {e}")

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=dishes_with_images.xlsx'
    return response


@login_required
def import_dishes(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']

        try:
            wb = load_workbook(filename=excel_file)
            ws = wb.active
        except Exception as e:
            messages.error(request, f"Error reading Excel file: {e}")
            return redirect('dish_list')

        # Get headers and map to column indices
        headers = [cell.value for cell in ws[1]]
        col_index = {header: i for i, header in enumerate(headers)}

        for row in ws.iter_rows(min_row=2):
            # Convert row to dict with header keys
            data = {header: row[col_index[header]].value if header in col_index else None for header in headers}

            # Create or update dish
            dish, created = Dish.objects.update_or_create(
                dish_id=data.get('dish_id'),
                defaults={
                    'name_en': data.get('name_en', ''),
                    'name_te': data.get('name_te', ''),
                    'name_ta': data.get('name_ta', ''),
                    'name_hi': data.get('name_hi', ''),
                    'name_ka': data.get('name_ka', ''),
                    'preparation_en': data.get('preparation_en', ''),
                    'preparation_te': data.get('preparation_te', ''),
                    'preparation_ta': data.get('preparation_ta', ''),
                    'preparation_hi': data.get('preparation_hi', ''),
                    'preparation_ka': data.get('preparation_ka', ''),
                }
            )

            # Handle dish image
            image_url = data.get('image_url')
            if image_url and isinstance(image_url, str) and image_url.strip():
                try:
                    resp = requests.get(image_url)
                    if resp.status_code == 200:
                        dish.image.save(f"{dish.dish_id}.jpg", ContentFile(resp.content), save=True)
                except Exception as e:
                    messages.warning(request, f"Failed to import image for {dish.dish_id}: {e}")

            # Handle ingredients
            ingredient_name = data.get('ingredient_name')
            if ingredient_name:
                try:
                    ingredient = Ingredient.objects.get(name_en=ingredient_name)
                    DishIngredient.objects.update_or_create(
                        dish=dish,
                        ingredient=ingredient,
                        defaults={
                            'quantity': data.get('quantity', 0) or 0,
                            'unit': data.get('unit', 'N/A') or 'N/A',
                            'price': data.get('price', 0) or 0,
                        }
                    )
                except Ingredient.DoesNotExist:
                    messages.warning(request, f"Ingredient '{ingredient_name}' not found. Skipping.")

        messages.success(request, "Dishes imported successfully.")
        return redirect('dish_list')

    return render(request, 'dishes/import_dishes.html')

@login_required
def update_dish_ingredients(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    
    if request.method == "POST":
        # Update or delete each ingredient
        for key in request.POST:
            if key.startswith("ingredient_id_"):
                di_id = key.replace("ingredient_id_", "")
                if not di_id.isdigit():
                    continue

                di = get_object_or_404(DishIngredient, id=int(di_id))
                delete_flag = request.POST.get(f"delete_{di_id}")

                if delete_flag:
                    di.delete()
                    continue

                # Update ingredient
                ingredient_id = request.POST.get(f"ingredient_id_{di_id}")
                quantity = request.POST.get(f"quantity_{di_id}")
                unit = request.POST.get(f"unit_{di_id}")
                price = request.POST.get(f"price_{di_id}")

                try:
                    ingredient = Ingredient.objects.get(id=int(ingredient_id))
                    di.ingredient = ingredient
                    di.quantity = float(quantity) if quantity else 0
                    di.unit = unit or "N/A"
                    di.price = float(price) if price else 0
                    di.save()
                except Ingredient.DoesNotExist:
                    continue

        messages.success(request, f"Ingredients updated successfully for {dish.name_en}")
        return redirect("dish_list")  # Redirect ensures DB updated data is loaded fresh

    # If GET request (or redirect after POST), fetch fresh data
    user_lang = getattr(request.user, "preferred_language", "en")
    dish.display_name = getattr(dish, f"name_{user_lang}", None) or dish.name_en
    dish.display_preparation = getattr(dish, f"preparation_{user_lang}", None) or dish.preparation_en
    dish.display_ingredients = []
    for ing in dish.dishingredient_set.all():
        ing_name = getattr(ing.ingredient, f"name_{user_lang}", None) or ing.ingredient.name_en
        dish.display_ingredients.append({
            'id': ing.id,
            'ingredient': ing.ingredient,
            'name': ing_name,
            'quantity': ing.quantity,
            'unit': ing.unit,
            'price': ing.price
        })

    all_ingredients = Ingredient.objects.all().order_by("name_en")

    return render(request, "dishes/dish_list.html", {"dishes": [dish], "user_lang": user_lang, "all_ingredients": all_ingredients})


