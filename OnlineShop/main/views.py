from django.views.generic.base import TemplateView
from categories.models import Category
from goods.models import Good


class MainPageView(TemplateView):
    template_name = "mainpage.html"
    categories = Category.objects.all()
    goods = Good.objects.filter(featured=True)[:3]

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context["categories"] = self.categories
        context["goods"] = self.goods
        return context
