from django.shortcuts import render

from django.views.generic.base import View
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = self.request.POST.get('old_password', None)
        new_password = self.request.POST.get('new_password', None)
        request.user.set_password('new password')
        request.user.save()
        messages.success(request, 'Your password has been successfully changed.')

    return render(request, 'body.html', {'form': form})



class LoginPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        kwargs = super(LoginPage, self).get_context_data(**kwargs)
        # Your code here
        kwargs['foo'] = "bar"
        return kwargs

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        username = self.request.POST.get('username', None)
        password = self.request.POST.get('password', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            messages.warning(request, "Incorrect username or password.")




        previous_foo = context['foo']
        context['new_variable'] = 'new_variable' + ' updated'

        return self.render_to_response(context)


class ProfilePage(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    login_url = "/"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        old_password = self.request.POST.get('old_password', None)
        new_password = self.request.POST.get('new_password', None)
        if request.user.check_password(old_password):
            request.user.set_password(new_password)
            request.user.save()

            messages.success(request, 'Your password has been successfully changed.')
        else:
            messages.warning(request, 'Your old password is incorrect.')
        return self.render_to_response(context)
    def get_context_data(self, **kwargs):
        kwargs = super(ProfilePage, self).get_context_data(**kwargs)
        kwargs["form"] = PasswordChangeForm(user=self.request.user)
        return kwargs



class DashboardPage(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = "/"

    def get_context_data(self, **kwargs):
        kwargs = super(DashboardPage, self).get_context_data(**kwargs)

        kwargs['foo'] = "bar"
        return kwargs


def logout_view(request):
    logout(request)
    return redirect('/')