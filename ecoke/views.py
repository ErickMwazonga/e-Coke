# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
# Django importd
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum, Q
from django.views.generic.edit import CreateView
from django.views.generic import View, TemplateView, ListView, CreateView
# App imports
from .models import Brand
from .forms import BrandForm, BrandSearchForm

# Create your views here.
# index view
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'ecoke/index.html'


class LoginView(BaseLoginView):
    template_name = 'ecoke/login.html'
    authentication_form = AuthenticationForm


# Create CBV for listing the brands
class BrandListView(LoginRequiredMixin, ListView):
    context_object_name = 'brands'
    model               = Brand
    template_name       = 'ecoke/brand_list.html'

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
            request=request,
        )
    return JsonResponse(data)


#creating a view for exporting csv
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ecoke.csv"'

    brands      = Brand.objects.all()
    headings    = ['Collector', 'Respondent', 'City', 'Favourite Drink', 'Date of Collection']
    writer      = csv.writer(response)

    for brand in brands:
        writer.writerow([brand.collector_name, brand.respondent_name, brand.respondent_city, brand.favourite_drink, brand.date_of_collection])

    return response