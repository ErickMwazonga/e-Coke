# Django imports
from django import forms
# Crispy form imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, MultiWidgetField, Submit
# App imports
from .models import Brand

class BrandForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        self.helper             = FormHelper()
        self.helper.form_tag    = False

        self.helper.layout = Layout(
            'collector_name',
            'respondent_name',
            'respondent_city',
            'favourite_drink',
            MultiWidgetField(
                'date_of_collection',
                attrs=(
                    {'style': 'width: 32.7%; display: inline-block;'}
                )
            ),
        )

    class Meta:
        model   = Brand
        fields  = ['collector_name', 'respondent_name', 'respondent_city', 'favourite_drink', 'date_of_collection']

        widgets = {
            'date_of_collection': forms.SelectDateWidget(years=[str(val) for val in range(2005, 2020)]),
        }


class BrandSearchForm(forms.Form):
    collector_name = forms.ModelChoiceField(
        queryset = Brand.objects.values_list('collector_name', flat=True),
        empty_label  = "Choose a Collector"
    )

    def __init__(self, *args, **kwargs):
        super(BrandSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            'collector_name',
            Submit('Search', 'search', css_class='btn-default'),
        )
        self.helper.form_method = 'get'
