from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, LoginForm

# Регистрация
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# Вход
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Неверные данные для входа")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, Category, Dish
from django.contrib import messages

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant_list.html', {'restaurants': restaurants})

def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    categories = restaurant.categories.prefetch_related('dishes').all()
    return render(request, 'restaurant_menu.html', {'restaurant': restaurant, 'categories': categories})

def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = request.session.get('cart', {})

    restaurant_id = str(dish.category.restaurant.id)
    item = {
        'dish_id': dish.id,
        'name': dish.name,
        'price': float(dish.price),
        'grams': dish.grams,
        'image': dish.image.url
    }

    if restaurant_id not in cart:
        cart[restaurant_id] = []

    cart[restaurant_id].append(item)
    request.session['cart'] = cart
    messages.success(request, f'{dish.name} добавлен в корзину!')
    return redirect('restaurant_menu', restaurant_id=restaurant_id)

def view_cart(request):
    cart_data = request.session.get('cart', {})
    cart = {}

    for rest_id, items in cart_data.items():
        restaurant = Restaurant.objects.get(id=rest_id)
        cart[restaurant] = [{'dish': Dish.objects.get(id=item['dish_id'])} for item in items]

    return render(request, 'cart.html', {'cart': cart})
