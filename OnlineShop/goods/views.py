from django.http import Http404
from django.views.generic import TemplateView

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
