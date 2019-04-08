from django.contrib.admin import ModelAdmin, register
from django.contrib.admin.widgets import AdminTextInputWidget
from django.db.models import TextField

from .models import Ignorable404Url, Ignorable404Referer

@register(Ignorable404Url)
class Ignorable404UrlAdmin(ModelAdmin):
	formfield_overrides = {
		# Use a smaller text field:
		TextField: {'widget': AdminTextInputWidget},
	}

@register(Ignorable404Referer)
class Ignorable404RefererAdmin(ModelAdmin):
	formfield_overrides = {
		# Use a smaller text field:
		TextField: {'widget': AdminTextInputWidget},
	}