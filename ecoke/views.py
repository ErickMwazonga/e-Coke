# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
# Django importd
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import render, get_object_or_404, redirect, \
                            reverse, Http404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.views.generic import TemplateView, ListView, DetailView, FormView

from sweetify.views import SweetifySuccessMixin
import sweetify

# App imports
from . import helpers
from .models import Brand, Profile
from .forms import BrandForm, BrandSearchForm, ProfileForm, \
                    ChangePasswordForm, FeedbackForm, UserCreateForm


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'ecoke/profile.html'
    slug_field = "username"


# index view
class IndexView(TemplateView):
    template_name = 'ecoke/index.html'


class LoginView(SweetifySuccessMixin, BaseLoginView):
    template_name = 'ecoke/login.html'
    authentication_form = AuthenticationForm
    success_message = 'Welcome!'


def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            # send email verification now
            activation_key = helpers.generate_activation_key(username)
            subject = "Account Verification"
            # Split to one line to avoid header injection issues
            subject = ''.join(subject.splitlines())

            # scheme = http/https, get_host = 127.0.0.1:8000
            activate_url = "{0}://{1}/activate/account/?key={2}".format(request.scheme, request.get_host(), activation_key)
            message = render_to_string(
                'ecoke/includes/acc_active_email.html',
                {
                    'user': user,
                    'activate_url': activate_url
                }
            )

            mail = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST, [email])
            mail.attach_alternative(message, "text/html")

            error = False
            try:
                mail.send()
                sweetify.success(request, 'Welcome', text='Account created! Click on the link sent to your email to activate the account', persistent='OK')
                # messages.add_message(request, messages.INFO, 'Account created! Click on the link sent to your email to activate the account')
            except:
                error = True
                sweetify.error(request, 'Oh! NO', text='Unable to send email verification. Please try again', persistent='OK')
                # messages.add_message(request, messages.INFO, 'Unable to send email verification. Please try again')

            if not error:
                user.username = username
                user.email = email
                user.password1 = password1
                user.is_active = 0
                user.save()
                user.profile.activation_key = activation_key
                user.save()

            return redirect(reverse('ecoke:login'))
    else:
        form = UserCreateForm()

    return render(request, 'ecoke/register.html', {'form': form})


def activate_account(request):
    key = request.GET['key']
    if not key:
        raise Http404

    # r = get_object_or_404(Profile, activation_key=key, email_validated=False)
    try:
        r = Profile.objects.get(activation_key=key, email_validated=False)
    except Profile.DoesNotExist:
        raise Http404('The activation link was already used!!!')
    r.user.is_active = True
    r.user.save()
    r.email_validated = True
    r.save()

    return redirect(reverse('ecoke:login'))


@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.profile.job_title = form.cleaned_data.get('job_title')
            user.profile.bio = form.cleaned_data.get('bio')
            user.profile.location = form.cleaned_data.get('location')
            user.profile.avatar = form.cleaned_data.get('avatar')
            user.save()
            # messages.add_message(request,
            #                      messages.SUCCESS,
            #                      'Your profile was successfully edited.')
            sweetify.success(request, 'PROFILE!',
                             text='Your profile was successfully edited.',
                             persistent='OK')
            return redirect(reverse('ecoke:profile', kwargs={'slug': user.username}))
    else:
        form = ProfileForm(instance=user, initial={
            'job_title': user.profile.job_title,
            'bio': user.profile.bio,
            'location': user.profile.location,
            'avatar': user.profile.avatar,
        })

    return render(request, 'ecoke/change_profile.html', {'form': form})


# Create CBV for listing the brands
class BrandListView(LoginRequiredMixin, ListView):
    context_object_name = 'brands'
    model = Brand
    template_name = 'ecoke/brand_list.html'

    def get_queryset(self):
        queryset = super(BrandListView, self).get_queryset().order_by('-collector_name')
        collector_name = self.request.GET.get('collector_name')

        if collector_name:
            return queryset.filter(collector_name=collector_name)
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super(BrandListView, self).get_context_data(**kwargs)
        ctx['search_form'] = BrandSearchForm
        return ctx


# saving brands
def save_brand_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            brands = Brand.objects.all()
            data['html_brand_list'] = render_to_string("ecoke/includes/partial_brand_list.html",
                {'brands': brands}
            )
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


# create brand
@login_required()
def brand_create(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
    else:
        form = BrandForm()
    return save_brand_form(request, form, 'ecoke/brand_form.html')


# update brand
@login_required()
def brand_update(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
    else:
        form = BrandForm(instance=brand)
    return save_brand_form(request, form, 'ecoke/brand_update.html')


# delete brand
@login_required()
def brand_delete(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    data = dict()
    if request.method == 'POST':
        brand.delete()
        data['form_is_valid'] = True
        brands = Brand.objects.all()
        data['html_brand_list'] = render_to_string('ecoke/includes/partial_brand_list.html',
            {'brands': brands}
        )
    else:
        context = {'brand': brand}
        data['html_form'] = render_to_string('ecoke/brand_delete.html', context, request=request)
    return JsonResponse(data)


# creating a view for exporting csv
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ecoke.csv"'

    writer = csv.writer(response)
    brands = Brand.objects.all()
    headings = ['Collector', 'Respondent', 'City', 'Favourite Drink', 'Date of Collection']
    writer.writerow(headings)

    for brand in brands:
        writer.writerow([brand.collector_name, brand.respondent_name, brand.respondent_city, brand.favourite_drink, brand.date_of_collection])

    return response


class FeedbackFormView(FormView):
    form_class = FeedbackForm
    template_name = 'ecoke/feedback.html'

    def get_initial(self):
        if self.request.user.is_authenticated():
            return {
                'name': self.request.user.profile.get_screen_name,
                'email': self.request.user.email,
            }

    # def form_valid(self, form):
    #     success_message = 'Thank you for your Feedback.'
    #     messages.add_message(self.request, messages.SUCCESS, success_message)

    #     return super(FeedbackFormView, self).form_valid(form)

    # def form_invalid(self, form):
    #     failure_message = 'Email not sent. Please try again.'
    #     messages.add_message(self.request, messages.WARNING, failure_message)

    #     return super(FeedbackFormView, self).form_invalid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            support_email = settings.CONTACTS['support_email']

            subject = "[e-Coke] A New Feedback"
            ctx = {
                'name': name,
                'email': email,
                'message': message
            }
            txt_message = render_to_string('ecoke/includes/_email_feedback.html', ctx)

            mail = EmailMultiAlternatives(subject, txt_message, email, [support_email])
            mail.attach_alternative(txt_message, "text/html")
            try:
                mail.send()
            except:
                return JsonResponse({'error': 'Email not sent. Please try again.'})
                # messages.add_message(request, messages.WARNING, 'Unable to send email verification. Please try again')

            # return self.form_valid(form)
            return JsonResponse({'success': 'Thank you for your Feedback.'})
        else:
            # return self.form_invalid(form)
            return JsonResponse({'error': 'Email not sent. Please try again.'})

    def get_success_url(self):
        return reverse('ecoke:index')


@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            sweetify.success(request, 'PASSWORD!',
                             text='Your password was successfully changed.',
                             persistent='OK')

            # messages.add_message(request, messages.SUCCESS,
            #                      'Your password was successfully changed.')
            return redirect(reverse('ecoke:change_password'))

    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'ecoke/password.html', {'form': form})
