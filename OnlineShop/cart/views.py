from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from cart.models import Cart, CartItem
from goods.models import Good
from profiles.models import Profile


def checkout(request):
    if request.method == 'GET':
        profile = Profile.objects.filter(user=request.user)[0]
        cart = Cart.objects.filter(profile=profile)
        if len(cart) > 0:
            cart_items = CartItem.objects.filter(cart=cart[0])[::1]
        else:
            cart_items = []
    else:
        cart_items = []
    return render(request, 'checkout.html', {'cart_items': cart_items})


@csrf_protect
def remove(request):
    if request.method == "POST" and request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)[0]
        cart = Cart.objects.filter(profile=profile)
        if len(cart) > 0:
            item = CartItem.objects.get(id=request.POST.get('id'))
            if item is not None:
                item.delete()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@csrf_protect
def remove_all(request):
    if request.method == "GET" and request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)[0]
        cart = Cart.objects.filter(profile=profile)
        if len(cart) > 0:
            for item in CartItem.objects.filter(cart=cart[0]):
                item.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseBadRequest()


def add(request):
    if request.method == "POST" and request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)[0]
        cart = Cart.objects.filter(profile=profile)
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
