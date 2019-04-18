from django.contrib import admin

from .models import Species, Ability, Move, LearnableMove, LevelMove, Location

# Register your models here.


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
            'min_weight', 'max_weight',
            'regional_variant',
            'form',
            'base_HP', 'base_Attack', 'base_Defense',
            'base_SpAttack', 'base_SpDefense', 'base_Speed'
        ]}),
        ('Metadata', {'fields': ['date_added']}),
    ]
    list_display = ('__str__', 'type_string', 'ability_1', 'ability_2', 'hidden_ability', 'BST')

class AbilityAdmin(admin.ModelAdmin):
    list_display = ('ability_name', 'ability_desc')

admin.site.register(Species, SpeciesAdmin)
admin.site.register(Ability, AbilityAdmin)
admin.site.register(Move)
admin.site.register(LevelMove)
admin.site.register(LearnableMove)
admin.site.register(Location)