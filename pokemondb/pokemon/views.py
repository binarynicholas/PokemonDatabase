from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from .models import Species, Ability, Move, LearnableMove, LevelMove, Location

from simple_rest_client.api import API
import requests
import json
import time

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

class MoveView(DetailView):
    model = Move
    context_object_name = 'move'

    def get_context_data(self, **kwargs):
        context = super(MoveView, self).get_context_data(**kwargs)
        context['title'] = self.object.move_name + " (Move)"
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

class ScrapeMoves(TemplateView):

    def get(self, request, *args, **kwargs):
        print("Getting moves...")
        api_request = "https://pokeapi.co/api/v2/move/"
        for _ in range (1, 728):
            api = API(
                api_root_url=api_request + _.__str__(),
                append_slash=True,
                json_encode_body=True,
            )
            response = requests.get(api.api_root_url)
            json_obj = json.loads(response.text)
            d = {}
            d["name"] = titlefy_name(json_obj["name"])
            d["type"] = Move.typeID(titlefy_name(json_obj["type"]["name"]))
            d["desc"] = cleanse_text(json_obj["flavor_text_entries"][2]["flavor_text"])
            d["acc"] = json_obj["accuracy"]
            d["power"] = json_obj["power"]
            d["category"] = Move.categoryID(titlefy_name(json_obj["damage_class"]["name"]))

            try:
                m = Move.objects.get(move_name=d["name"])
                print("Move already existed - updating type and stuff")
                if (m.move_type != Move.typeID("Cyber")):
                    print("Move not Cyber!")
                    m.move_type = d["type"]
                    m.move_category = d["category"]
                    m.save()
                    
            except:
                m = Move(
                    move_name=d["name"],
                    move_type=d["type"],
                    move_desc=d["desc"],
                    base_power=d["power"],
                    base_accuracy=d["acc"],
                    move_category=d["category"]
                )
                m.save()
                print(m)
            time.sleep(0.5)

        return HttpResponseRedirect('/')
    
def titlefy_name(input):
    output = input.replace("-", " ").title()
    return output

def cleanse_text(input):
    output = input.replace("\n", " ")
    return output