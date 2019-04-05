from django.contrib import admin

from .models import Species, Ability

# Register your models here.

admin.site.register(Ability)

class AbilityInLine(admin.TabularInline):
    model=Ability

class SpeciesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'species_name', 'type_primary', 'type_secondary',
            'ability_1', 'ability_2', 'hidden_ability',
            'egg_group_1', 'egg_group_2'
        ]}),
        ('Biometric information', {'fields': [
            'min_height', 'max_height',
            'min_weight', 'max_weight'
        ]}),
        ('Metadata', {'fields': ['date_added']}),
    ]
    list_display = ('species_name', 'type', 'ability_1', 'ability_2', 'hidden_ability')


admin.site.register(Species, SpeciesAdmin)