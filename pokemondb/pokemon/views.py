from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from .models import Species, Ability

# root page: shows latest added Pokemon.

def index(request):
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
    return render(request, 'pokemon/index.html', context)

def speciesDetails(request, pokemon_id):
    species = get_list_or_404(Species, pk=pokemon_id)
    return render(request, 'pokemon/speciesDetail.html', {'species': species})

def abilityDetails(request, ability_id):
    ability = get_object_or_404(Ability, pk=ability_id)
    return render(request, 'pokemon/abilityDetail.html', {'ability': ability})


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
            returnvalue = returnvalue.filter(species_name=s[0])

    print(searches)
    return returnvalue

def filterType(dataset, args):
    proper_args = args.capitalize()
    searched_type = Species.typeID(proper_args)
    print(dataset.filter(Q(type_primary=searched_type) | Q(type_secondary=searched_type)))
    return dataset.filter(Q(type_primary=searched_type) | Q(type_secondary=searched_type))


def filterAbility(dataset):
    print("Filtering on ability...")