from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from . import forms
from .models import Product, Cart, CartItem
from django.views.generic import DetailView, ListView, View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# from .models import Article
               
def product_description(request):
    return render(request, "Polls/product_description.html")

class ProductListView(ListView):
    model = Product
    template_name = 'Polls/main.html'  
    context_object_name = 'products'
    # ordering = ['-date_posted']
    
class ProductListViewNew(ListView):
    model = Product
    template_name = 'Polls/main.html'
    context_object_name = 'products'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Проверка аутентификации пользователя и получение элементов корзины
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['cart_items'] = CartItem.objects.filter(cart=cart)  # здесь фильтруем по объекту cart
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name="Polls/product_description.html"
    context_object_name = 'object'
    fields = ['title', 'description', 'price','photo']
    
class CartDetailView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'main.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        # Получаем корзину текущего пользователя
        cart = Cart.objects.get_or_create(user=self.request.user)
        # Возвращаем все элементы корзины
        return CartItem.objects.filter(cart=cart)
    
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        return redirect("main")
    else:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('main') 

def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(cart=cart, product=product).delete()
    return redirect('main')

def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    return redirect('cart_detail')

def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'cart_detail.html', {'cart': cart})    

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return redirect("main")

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main")
        return redirect("main")

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return redirect("main")

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect("main")
        return redirect("main")   
                 


# def register_view(request):
#     # if request.user.is_authenticated:
#     #     # Если пользователь уже аутентифицирован, перенаправляем его на главную страницу
#     #     return redirect('main')  # Замените 'home' на имя вашего представления или URL

#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             # Сохраняем нового пользователя
#             print("valid2")
#             # Аутентифицируем нового пользователя и выполняем вход
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 print("valid3")
#                 login(request, user)
#                 # Перенаправляем пользователя на нужную страницу
#                 return redirect('main')  # Замените 'home' на имя вашего представления или URL
#     else:
#         # Если запрос не методом POST, просто отображаем пустую форму регистрации
#         form = UserCreationForm()
#     return render(request, 'Polls/register.html', {'form': form})