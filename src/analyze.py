
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

def simplify_reagents(reagents: Dict[str, int | float], result_amount: int = 1) -> Dict[str, float]:
    new_reagents = {}
    for name, ratio in reagents.items():
        if is_reaction(name):
            for k, v in simplify_reaction(name).items():
                if k not in new_reagents:
                    new_reagents[k] = 0
                new_reagents[k] += float(v) / float(result_amount)
        elif is_reagent(name):
            if name not in new_reagents:
                new_reagents[name] = 0
            new_reagents[name] += float(ratio) / float(result_amount)
        else:
            raise ValueError('Unknown reagent/recipe: ', name)
    return new_reagents

def simplify_reaction(reaction_name: str) -> Dict[str, float]:
    reaction = all_reactions[reaction_name]
    return simplify_reagents(reaction['required_reagents'], reaction['result_amount'])


def convert_to_units(reagents: Dict[str, float]) -> Dict[str, int]:
    lowest_amount = sorted(reagents.values())[0]
    as_units = {k: int(v / lowest_amount) for k, v in reagents.items()}
    for k, v in as_units.items():
        if reagents[k] % lowest_amount > .000000001:
            log.warning(f'Warning: {k} has a remainder of {reagents[k] % lowest_amount}')
    return as_units

def as_reagent_group(reagents: Dict[str, int]) -> str:
    log.info('Converting reagents to group')
    return ''.join([f'{k}={v};' for k, v in reagents.items()])

def reaction_as_reagent_group_dict(reaction_name: str) -> Dict[str, int]:
    log.info(f'Converting {reaction_name} to reagent group dict')
    return convert_to_units(simplify_reaction(reaction_name))

def reaction_as_dispensable_group_dict(reaction_name: str) -> Dict[str, int]:
    log.info(f'Converting {reaction_name} to dispensable group dict')
    reagent_group_contents = reaction_as_reagent_group_dict(reaction_name)
    to_remove = []
    for k, v in reagent_group_contents.items():
        if not is_dispensable(k):
            to_remove.append(k)
    for k in to_remove:
        del reagent_group_contents[k]
    return reagent_group_contents

def reaction_as_reagent_group(reaction_name: str) -> str:
    return as_reagent_group(reaction_as_reagent_group_dict(reaction_name))

def reaction_as_dispensable_group(reaction_name: str) -> str:
    return as_reagent_group(reaction_as_dispensable_group_dict(reaction_name))


def reagents_as_reagent_group_dict(reagents: Dict[str, int], result_amount: int = 1) -> Dict[str, int]:
    log.info(f'Converting reagents to reagent group dict')
    log.info(f'\tReagents: {reagents}')
    return convert_to_units(simplify_reagents(reagents, result_amount))

def reagents_as_dispensable_group_dict(reagents: Dict[str, int], result_amount: int = 1) -> Dict[str, int]:
    log.info(f'Converting reagents to dispensable reagent group dict')
    log.info(f'\tReagents: {reagents}')
    reagent_group_contents = reagents_as_reagent_group_dict(reagents, result_amount)
    to_remove = []
    for k, v in reagent_group_contents.items():
        if not is_dispensable(k):
            to_remove.append(k)
    for k in to_remove:
        del reagent_group_contents[k]
    return reagent_group_contents

def reagents_as_reagent_group(reagents: Dict[str, int], result_amount: int = 1) -> str:
    return as_reagent_group(reagents_as_reagent_group_dict(reagents, result_amount))

def reagents_as_dispensable_group(reagents: Dict[str, int], result_amount: int = 1) -> str:
    return as_reagent_group(reagents_as_dispensable_group_dict(reagents, result_amount))


def get_reagent_group_dict(reaction_or_reagents: str | Dict[str, int]) -> Dict[str, int]:
    if isinstance(reaction_or_reagents, str):
        return reaction_as_reagent_group_dict(reaction_or_reagents)
    return reagents_as_reagent_group_dict(reaction_or_reagents)

def get_dispensable_group_dict(reaction_or_reagents: str | Dict[str, int]) -> Dict[str, int]:
    if isinstance(reaction_or_reagents, str):
        return reaction_as_dispensable_group_dict(reaction_or_reagents)
    return reagents_as_dispensable_group_dict(reaction_or_reagents)

def get_reagent_group(reaction_or_reagents: str | Dict[str, int]) -> str:
    if isinstance(reaction_or_reagents, str):
        return reaction_as_reagent_group(reaction_or_reagents)
    return reagents_as_reagent_group(reaction_or_reagents)

def get_dispensable_group(reaction_or_reagents: str | Dict[str, int]) -> str:
    if isinstance(reaction_or_reagents, str):
        return reaction_as_dispensable_group(reaction_or_reagents)
    return reagents_as_dispensable_group(reaction_or_reagents)


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
            dispensable_group = get_dispensable_group(name)
        except ValueError:
            log.warning(f'{name} is not a valid reaction')
            continue
        log.info(f'\t{[name, dispensable_group]}')


if __name__ == '__main__':
    analyze()


