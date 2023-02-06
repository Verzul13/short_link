from django.http import Http404
from django.shortcuts import redirect
from django.core.cache import cache
from django.views.generic import TemplateView
from django.shortcuts import render

from .models import ShortLink
from .tasks import update_visit_count
from .forms import LinkshortenerCreateForm


def redirect_subpart(request, subpart):
    '''
    Принимает subpart и редиректит на записынный в кэш или ShortLink url
    '''
    url = cache.get(f'subpart_{subpart}')
    if not url:
        short_link = ShortLink.objects.filter(subpart=subpart).first()
        if not short_link:
            raise Http404
        url = short_link.long_url

    update_visit_count.delay(subpart)

    return redirect(url)


class MainPageView(TemplateView):
    template_name = 'linkshortener/main_page.html'
    link_shortener_create_form = LinkshortenerCreateForm

    def get(self, request, *args, **kwargs):
        data = {
            "link_shortener_create_form": self.link_shortener_create_form,
        }

        return render(request, self.template_name, data)
