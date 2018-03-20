from django.contrib import admin

from .models import Animal, AnimalWeight

# Register your models here.

class AnimalAdmin(admin.ModelAdmin):
    list_display = ('__str__','id')
    list_filter = []
    search_fields = ['id']
    readonly_fields = ('created_at', 'last_modified',)


admin.site.register(Animal, AnimalAdmin)



admin.site.register(AnimalWeight)