from django.shortcuts import render, redirect
from django.http import HttpResponse
from uloginapp.forms import UserRegisterForm
from django.views.generic import TemplateView
from django.contrib.auth.models import User

def register(response):
    if response.method == "POST":
        form = UserRegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserRegisterForm()

    return render(response, "register.html", { "form" : form })


class IndexView(TemplateView):
    template_name = "users.html"

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super().get_context_data(*args, **kwargs)

        if user and user.is_authenticated:
            context['auth_user'] = User.objects.all()


        return context