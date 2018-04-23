from django.contrib import admin

from .models import Shi, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class ShiAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['input_text']}),
        ('text', {'fields': ['output_text']}),
        ('Date information', {'fields': ['created_date', 'published_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    search_fields = ['input_text', 'output_text']

admin.site.register(Shi, ShiAdmin)
admin.site.register(Choice)
