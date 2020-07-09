from django.shortcuts import render
from django.views import View


class WelcomePageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'welcome/index.html')
