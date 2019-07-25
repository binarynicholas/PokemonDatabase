from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from .models import Species, Ability, Move, LearnableMove, LevelMove, Location

# root page: shows latest added Pokemon.


class SpeciesList(ListView):
    model = Species
    context_object_name = 'current_species'

    def get_queryset(self):
        return Species.objects.order_by('id')
    
    def post(self, request, *args, **kwargs):
        try:
            if request.POST['searchterm'] is not "":
                try:
                    current_species = filterSearch(request.POST['searchterm'])
                except (IndexError):
                    current_species = []
            else:
                current_species = Species.objects.order_by('id')
        except (KeyError, Species.DoesNotExist):
            current_species = Species.objects.order_by('id')
        context = { 'current_species' : current_species }
        return render(request, 'pokemon/species_list.html', context)


class SpeciesView(DetailView):
    model = Species
    context_object_name = 'species'

    def get_context_data(self, **kwargs):
        context = super(SpeciesView, self).get_context_data(**kwargs)
        species = self.object
        context['title'] = species.species_name + " (Pokémon)"
        context['level_moves'] = LevelMove.objects.filter(species=species).order_by('level')
        context['tm_moves'] = LearnableMove.objects.filter(species=species, source='1').order_by('move__TM_number')
        context['egg_moves'] = LearnableMove.objects.filter(species=species, source='2')
        context['tutor_moves'] = LearnableMove.objects.filter(species=species, source='3')
        context['locations'] = Location.objects.filter(available_species=species)
        return context

class AbilityView(DetailView):
    model = Ability
    context_object_name = 'ability'

    def get_context_data(self, **kwargs):
        context = super(AbilityView, self).get_context_data(**kwargs)
        context['title'] = self.object.ability_name + " (Ability)"
        return context

def filterSearch(searchterm):
    terms = searchterm.split(" ")
    searches = [t.split(":") for t in terms]
    returnvalue = Species.objects.order_by('id')

    switcher = {
        "type" : filterType,
        "ability" : filterAbility,
    }

    for s in searches:
        if len(s) > 1:
            func = switcher.get(s[0])
            returnvalue = func(returnvalue, s[1])
        else:
            returnvalue = returnvalue.filter(species_name=s[0].lower().capitalize())

    print(searches)
    return returnvalue

def filterType(dataset, args):
    proper_args = args.capitalize()
    searched_type = Species.typeID(proper_args)
    print(dataset.filter(Q(type_primary=searched_type) | Q(type_secondary=searched_type)))
    return dataset.filter(Q(type_primary=searched_type) | Q(type_secondary=searched_type))


def filterAbility(dataset):
    print("Filtering on ability...")