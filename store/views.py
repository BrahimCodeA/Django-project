from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from store.models import Cart, Order, Product, Goodie

def home(request):
    products = Product.objects.all()
    goodies = Goodie.objects.all()
    return render(request, 'store/home.html', context={'products': products, 'goodies': goodies})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', context={'product': product})

def goodie_detail(request, slug):
    goodie = get_object_or_404(Goodie, slug=slug)
    return render(request, 'store/goodies_detail.html', context={'goodie': goodie})

def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, ordered=False, product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    return redirect('cart')

def add_to_cart_goodies(request, slug):
    user = request.user
    goodie = get_object_or_404(Goodie, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, ordered=False, goodie=goodie)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    return redirect('cart')


def cart(request):
    if request.user.is_authenticated:
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        cart_orders = user_cart.orders.filter(ordered=False)

        total_price = user_cart.calculate_total()

        return render(request, 'store/cart.html', {'orders': cart_orders, 'total_price': total_price})
    else:
        return render(request, 'store/cart.html', {'orders': []})
    
def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()
        
    return redirect('cart')

def delete_orders(request, order_id):
    # Récupérez la commande spécifique de l'utilisateur connecté
    order = get_object_or_404(Order, id=order_id, user=request.user, ordered=False)

    # Supprimez la commande spécifique
    order.delete()

    return redirect('cart')

def remove_from_cart(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.quantity > 1:
        order.quantity -= 1
        order.save()
    else:
        order.delete()

    return redirect('cart')

    

