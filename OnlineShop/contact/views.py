from django.core.mail import send_mail
from django.http import HttpResponse, BadHeaderError
from django.shortcuts import render, redirect

from categories.models import Category
from contact.forms import ContactForm
from goods.models import Good


def email_view(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = "{0}: {1}".format(name, form.cleaned_data['subject'])
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['dth.razak@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    goods = Good.objects.filter(featured=True)[:3]
    categories = Category.objects.all()[::1]
    return render(request, "contact.html", {'form': form, 'goods': goods, 'categories': categories})


def success_view(request):
    goods = Good.objects.filter(featured=True)[:3]
    categories = Category.objects.all()[::1]
    return render(request, "success.html", {'goods': goods, 'categories': categories})
