from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from cart.models import Cart, CartItem
from categories.models import Category
from goods.models import Good
from profiles.models import Profile


def checkout(request):
    if request.method == 'GET':
        _cart = dict()
        profile = Profile.objects.filter(user=request.user)[0]
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))
        if len(cart) > 0:
            cart_items = CartItem.objects.filter(cart=cart[0])[::1]
            total = sum([cart_item.quantity * cart_item.good.price for cart_item in cart_items])
            discount = total - cart[0].total
            cart_total = cart[0].total + 50
            _cart['total'] = total
            _cart['discount'] = discount
            _cart['cart_total'] = cart_total
        else:
            cart_items = []
    else:
        cart_items = []
    goods = Good.objects.filter(featured=True)[:3]
    categories = Category.objects.all()[::1]
    return render(request, 'checkout.html', {'cart_items': cart_items, 'goods': goods, 'categories': categories, 'cart': _cart})


@csrf_protect
def remove(request):
    if request.method == "POST" and request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)[0]
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))
        if len(cart) > 0:
            item = CartItem.objects.get(id=request.POST.get('id'))
            item.cart.total -= item.quantity * item.good.price
            item.cart.save()
            if item is not None:
                item.delete()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@csrf_protect
def remove_all(request):
    if request.method == "GET" and request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)[0]
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))
        if len(cart) > 0:
            for item in CartItem.objects.filter(cart=cart[0]):
                item.delete()
            cart[0].total = 0
            cart.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseBadRequest()


def add(request):
    if request.method == "POST" and request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)[0]
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))
        cartItem = CartItem()
        if len(cart) > 0:
            cartItem.cart = cart[0]
        else:
            cart = Cart()
            cart.profile = profile
            cart.total = 0.0
            cart.save()
            cartItem.cart = cart
        cartItem.quantity = int(request.POST.get('id_quantity'))
        cartItem.material = request.POST.get('id_material')
        cartItem.good = Good.objects.get(id=request.POST.get('id_good_id'))
        cartItem.save()
        return redirect('/good/{0}'.format(request.POST.get('id_good_id')))
    else:
        return HttpResponseBadRequest()


def buy(request):
    if request.method == "POST" and request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)[0]
        cart = list(filter(lambda x: x.is_active, Cart.objects.filter(profile=profile)))[0]
        cart.is_active = False
        cart.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseBadRequest()
