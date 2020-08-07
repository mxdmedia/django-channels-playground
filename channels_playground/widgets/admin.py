from django.contrib import admin
from .models import Widget
# Register your models here.


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    pass
