from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import (get_user_model, login, logout,
                                 authenticate, update_session_auth_hash)
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import UserSignupForm, LoginForm
from .tokens import account_activation_token

User = get_user_model()


class Signup(CreateView):
    form_class = UserSignupForm
    success_url = reverse_lazy('accounts:notice')
    template_name = 'accounts/sign-up.html'

    def form_valid(self, form, commit=True):
        # Save the provided password in hashed format
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        if commit:
            user.save()
            # Prepare email activation content
            current_site = get_current_site(self.request)
            subject = 'Activate your account'
            message = render_to_string('accounts/activation-email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
        return super().form_valid(form)

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            # Redirect to home page since this user is already authenticated
            return redirect('accounts:detail')
        return super().dispatch(*args, **kwargs)


class SignIn(View):

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('accounts:detail'))
        else:
            form = LoginForm()
            return render(request, 'accounts/sign-in.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                email=data.get('email'),
                password=data.get('password'))
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('accounts:detail'))
        return render(request, 'accounts/sign-in.html', {'form': form})


class SignOut(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('accounts:sign-in'))


class UserDetail(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('accounts:sign-in')
    template_name = 'accounts/my-account.html'


class EmailVerificationNotice(TemplateView):
    template_name = 'accounts/email-verification-notice.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            # Redirect to home page since this user is already authenticated
            return redirect('accounts:detail')
        return super().dispatch(*args, **kwargs)


class Activate(View):
    def get(self, request, uid, token):
        try:
            _uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=_uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None \
                and account_activation_token.check_token(user, token):
            # Activate user and login:
            user.is_active = True
            user.save()
            login(request, user)
            PasswordChangeForm(request.user)
            return HttpResponseRedirect(reverse('accounts:detail'))
        else:
            return HttpResponse('Activation link is invalid!')

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return HttpResponse('Password changed successfully')
