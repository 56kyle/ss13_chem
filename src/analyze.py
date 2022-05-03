
import json
import math
from logger import log
from typing import List, Dict


def parse_compounds(reagents: Dict[str, any]) -> Dict[str, any]:
    to_remove = []
    for k, v in reagents.items():
        if not isinstance(v, dict):
            to_remove.append(k)
    for k in to_remove:
        del reagents[k]
    return reagents


base_reagents = parse_compounds(json.load(open('data/chemistry/Reagents-Base.json', 'r'))['datum']['reagent'])
disease_reagents = parse_compounds(json.load(open('data/chemistry/Reagents-Diseases.json', 'r'))['datum']['reagent']['disease'])
drug_reagents = parse_compounds(json.load(open('data/chemistry/Reagents-Drugs.json', 'r'))['datum']['reagent']['drug'])
explosive_reagents = parse_compounds(json.load(open('data/chemistry/Reagents-ExplosiveFire.json', 'r'))['datum']['reagent']['combustible'])
food_reagents = parse_compounds(json.load(open('data/chemistry/Reagents-FoodDrink.json', 'r'))['datum']['reagent']['fooddrink'])
medical_reagents = parse_compounds(json.load(open('data/chemistry/Reagents-Medical.json', 'r'))['datum']['reagent']['medical'])
misc_reagents = parse_compounds(json.load(open('data/chemistry/Reagents-Misc.json', 'r'))['datum']['reagent'])
poison_reagents = parse_compounds(json.load(open('data/chemistry/Reagents-PoisonEtc.json', 'r'))['datum']['reagent']['harmful'])
all_reagents = {**base_reagents, **disease_reagents, **drug_reagents, **explosive_reagents, **food_reagents, **medical_reagents, **misc_reagents, **poison_reagents}

dispensable_reagents = json.load(open('data/chemistry/Chemistry-Machinery.json', 'r'))['obj']['machinery']['chem_dispenser']['var']['list']['dispensable_reagents']

all_reactions = parse_compounds(json.load(open('data/chemistry/Chemistry-Recipes.json', 'r'))['datum']['chemical_reaction'])

def recurse_print(data, tabs=0):
    if isinstance(data, dict):
        for key, value in data.items():
            print('\t' * tabs, key)
            recurse_print(value, tabs + 1)
    elif isinstance(data, list):
        for item in data:
            recurse_print(item, tabs)
    else:
        print('\t' * tabs, data)


def get_all_reactions():
    reactions = json.load(open('data/chemistry/Chemistry-Recipes.json', 'r'))['datum']['chemical_reaction']
    to_remove = []
    for k, v in reactions.items():
        if not isinstance(v, dict):
            print('removing ', k, ' from reactions')
            print('\t', v)
            to_remove.append(k)
    for k in to_remove:
        del reactions[k]
    return reactions


def is_reaction(name: str) -> bool:
    return name in all_reactions.keys()

def is_reagent(name: str) -> bool:
    return name in all_reagents.keys()

def is_dispensable(name: str) -> bool:
    return name in dispensable_reagents

#def simplify_reaction(reaction: Dict[str, int]) -> Dict[str, int]:

def simplify(reaction_name: str) -> Dict[str, float]:
    reagents = {}
    if not is_reaction(reaction_name):
        raise ValueError(f'{reaction_name} is not a valid reaction')
    reaction = all_reactions[reaction_name]
    for key, value in reaction['required_reagents'].items():
        if is_reaction(key):
            parts = simplify(key)
            for k, v in parts.items():
                if k in reagents:
                    reagents[k] += float(v) / float(reaction['result_amount'])
                else:
                    reagents[k] = float(v) / float(reaction['result_amount'])
        elif is_reagent(key):
            if key in reagents:
                reagents[key] += float(value) / float(reaction['result_amount'])
            else:
                reagents[key] = float(value) / float(reaction['result_amount'])
        else:
            raise ValueError('Unknown key: ', key)
    return reagents

def convert_to_units(reagents: Dict[str, float]) -> Dict[str, int]:
    lowest_amount = sorted(reagents.values())[0]
    as_units = {k: int(v / lowest_amount) for k, v in reagents.items()}
    for k, v in as_units.items():
        if reagents[k] % lowest_amount > .000000001:
            log.warning(f'Warning: {k} has a remainder of {reagents[k] % lowest_amount}')
    return as_units

def as_reagent_group(reagents: Dict[str, int]) -> str:
    return ''.join([f'{k}={v};' for k, v in reagents.items()])

def reaction_as_reagent_group_dict(reaction_name: str) -> Dict[str, int]:
    return convert_to_units(simplify(reaction_name))

def reaction_as_dispensable_group_dict(reaction_name: str) -> Dict[str, int]:
    reagent_group_contents = reaction_as_reagent_group_dict(reaction_name)
    to_remove = []
    for k, v in reagent_group_contents.items():
        if not is_dispensable(k):
            to_remove.append(k)
    for k in to_remove:
        del reagent_group_contents[k]
    return reagent_group_contents

def reaction_as_reagent_group(reaction_name: str) -> str:
    log.info(f'Converting {reaction_name} to reagent group')
    return as_reagent_group(reaction_as_reagent_group_dict(reaction_name))

def reaction_as_dispensable_group(reaction_name: str) -> str:
    log.info(f'Converting {reaction_name} to dispensable reagent group')
    return as_reagent_group(reaction_as_dispensable_group_dict(reaction_name))


def analyze():
    reactions = [
        'oil',
        'acetone',
        'sarin',
        'salt',
        'acid',
        'ammonia',
        'weedkiller',
    ]
    for name in reactions:
        try:
            reagent_group = reaction_as_dispensable_group(name)
        except ValueError:
            log.warning(f'{name} is not a valid reaction')
            continue
        log.info(f'\t{[name, reagent_group]}')


if __name__ == '__main__':
    analyze()


