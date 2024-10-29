from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


class CustomLoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')  # Redirect after successful login

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        # Only Admin login allowed
        if user is not None:
            #limit to admin only
            login(self.request, user)
            if user.is_staff or user.is_superuser:
                return redirect(self.get_success_url())
            else:
                return redirect(reverse_lazy('st_home'))
        else:
            messages.error(self.request, 'Invalid username or password.')
            return self.form_invalid(form)


def root_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect(reverse_lazy('home'))
        else:
            return redirect(reverse_lazy('st_home'))
    else:
        return redirect('login') 