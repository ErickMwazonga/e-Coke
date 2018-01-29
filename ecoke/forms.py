# Django imports
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Crispy form imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, MultiWidgetField, Submit
# App imports
from .models import Brand, Feedback
from .validators import validate_email_unique, validate_username_unique


class UserCreateForm(UserCreationForm):
    username = forms.CharField(max_length=30,
                               validators=[validate_username_unique])
    email = forms.EmailField(required=True,
                             validators=[validate_email_unique])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False)
    job_title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=75,
        required=False)
    bio = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'job_title',
                  'email', 'bio', 'location', 'avatar', ]


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Old password",
        required=True)

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New password",
        required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm new password",
        required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        id = self.cleaned_data.get('id')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class([
                'Old password don\'t match'])
        if new_password and new_password != confirm_password:
            self._errors['new_password'] = self.error_class([
                'Passwords don\'t match'])
        return self.cleaned_data


class BrandForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

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
        model = Brand
        fields = ['collector_name', 'respondent_name', 'respondent_city',
                  'favourite_drink', 'date_of_collection']

        widgets = {
            'date_of_collection': forms.SelectDateWidget(years=[str(val) for val in range(2005, 2020)]),
        }


class BrandSearchForm(forms.Form):
    collector_name = forms.ModelChoiceField(
        queryset=Brand.objects.values_list('collector_name', flat=True),
        empty_label="Choose a Collector"
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


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
