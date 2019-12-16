from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView

from categories.models import Category
from goods.models import Good


class GoodDetailView(TemplateView):
    template_name = "good_detail.html"

    def get_context_data(self, **kwargs):
        context = super(GoodDetailView, self).get_context_data(**kwargs)
        try:
            context["good"] = Good.objects.get(id=kwargs['pk'])
        except Good.DoesNotExist:
            raise Http404("Good does not exist")

        return context


def catalog(request):
    context = dict()
    goods = Good.objects.all()[::1]

    category = request.GET.get('category')
    if category is not None:
        goods = list(filter(lambda g: g.category.name == category, goods))

    price = request.GET.get('price')
    if price is not None:
        if price == 'lower':
            goods.sort(key=lambda g: g.price)
        else:
            goods.sort(key=lambda g: g.price, reverse=True)

    recommend = request.GET.get('recommend')
    if recommend is not None:
        if recommend == 'true':
            goods = list(filter(lambda g: g.featured, goods))

    in_stock = request.GET.get('in_stock')
    if in_stock is not None:
        if in_stock == 'true':
            goods = list(filter(lambda g: g.in_stock, goods))

    name = request.GET.get('search')
    if name is not None:
        goods = list(filter(lambda g: g.name.lower().startswith(name.lower()), goods))

    categories = Category.objects.all()
    paginator = Paginator(goods, 6)
    page = request.GET.get('page')
    good_list = paginator.get_page(page)

    context['goods'] = goods[:3]
    context['good_list'] = good_list
    context['categories'] = categories
    context['page_range'] = list(paginator.page_range)

    return render(request, 'catalog.html', context)
