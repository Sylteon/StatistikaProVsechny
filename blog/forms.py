from django import forms
from django.contrib import admin
from .models import ApiEndpoint

class ApiEndpointForm(forms.ModelForm):
    raw_api_key = forms.CharField(required=False, help_text="Enter the API key. It will be hashed before saving.")

    class Meta:
        model = ApiEndpoint
        fields = ['url', 'raw_api_key']

class ApiEndpointAdmin(admin.ModelAdmin):
    form = ApiEndpointForm
    list_display = ['url']

admin.site.register(ApiEndpoint, ApiEndpointAdmin)


