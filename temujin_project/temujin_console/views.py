from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView



class TestCaseView(TemplateView):


    def get_template_names(self):
        template = self.kwargs['template']
        return ["temujin_console/" + template + ".html"]


    def get_context_data(self, **kwargs):
        context = super(TestCaseView, self).get_context_data(**kwargs)
        return context