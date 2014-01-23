from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView


class ConsoleView(TemplateView):

    template_name = "temujin_console/console.html"

    