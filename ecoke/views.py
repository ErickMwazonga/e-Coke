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
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.core.mail import mail_admins
from django.views.generic import TemplateView, ListView, DetailView
# App imports
from .models import Brand
from .forms import BrandForm, BrandSearchForm, ProfileForm, ChangePasswordForm, FeedbackForm


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'ecoke/profile.html'
    slug_field = "username"


# index view
class IndexView(TemplateView):
    template_name = 'ecoke/index.html'


class LoginView(BaseLoginView):
    template_name = 'ecoke/login.html'
    authentication_form = AuthenticationForm


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
        data['html_form'] = render_to_string('ecoke/brand_delete.html',
            context,
            request=request)
    return JsonResponse(data)


# creating a view for exporting csv
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ecoke.csv"'

    brands = Brand.objects.all()
    headings = ['Collector', 'Respondent', 'City', 'Favourite Drink', 'Date of Collection']
    writer = csv.writer(headings)

    for brand in brands:
        writer.writerow([brand.collector_name, brand.respondent_name, brand.respondent_city, brand.favourite_drink, brand.date_of_collection])

    return response


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
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile was successfully edited.')
            return redirect(reverse('ecoke:profile', kwargs={'slug':user.username}))
    else:
        form = ProfileForm(instance=user, initial={
            'job_title': user.profile.job_title,
            'bio': user.profile.bio,
            'location': user.profile.location,
            'avatar': user.profile.avatar,
        })

    return render(request, 'ecoke/change_profile.html', {'form': form})


def feedback(request, username=None):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            email_prefix = settings.EMAIL_SUBJECT_PREFIX

            subject = " {}- A New Feedback".format(email_prefix)
            ctx = {
                'name': name,
                'email': email,
                'message': message
            }
            message = render_to_string('ecoke/includes/email_feedback.txt', ctx)

            mail_admins(subject, message)
            form.save()

            messages.add_message(request, messages.SUCCESS,
                                 'Thank you for your Feedback.')
            return redirect(reverse('ecoke:index'))

    else:
        if request.user.is_authenticated():
            user = get_object_or_404(User, username=username)
            form = FeedbackForm(instance=user, initial={
                'name': user.profile.get_screen_name,
                'email': user.email,
            })
        else:
            form = FeedbackForm(initial={
                'name': '',
                'email': '',
            })

    return render(request, 'ecoke/feedback.html', {'form': form})


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
            messages.add_message(request, messages.SUCCESS,
                                 'Your password was successfully changed.')
            return redirect(reverse('ecoke:change_password'))

    else:
        form = ChangePasswordForm(instance=user)

    return render(request, 'ecoke/password.html', {'form': form})
