from django.shortcuts import render
from django.views import View


# Create your views here.


class MainView(View):
    def get(self, request, *rages, **kwargs):
        return render(request, 'main/index.html')
