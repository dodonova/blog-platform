from django.shortcuts import render
from django.views.generic import TemplateView


def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html', status=403)


class HomePage(TemplateView):
    template_name = 'pages/about.html'


class Rules(TemplateView):
    template_name = 'pages/rules.html'
