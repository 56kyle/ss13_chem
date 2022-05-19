
import json
import math
from logger import log
from typing import List, Dict


def is_reagent_dict(reagent: Dict[str, any]) -> bool:
    if not isinstance(reagent, dict):
        return False
    if not reagent.get('name') and not reagent.get('id'):
        return False
    return True

def parse_compounds(reagents: Dict[str, any]) -> Dict[str, any]:
    keywords = ['var']
    new_reagents = {}
    for k, v in reagents.items():
        if isinstance(v, dict):
            if is_reagent_dict(v):
                new_reagents[k] = v
            for nested_name, nested_value in parse_compounds(v).items():
                new_reagents[nested_name] = nested_value
    return new_reagents


def get_all_compounds_by_id(reactions: Dict[str, any]) -> Dict[str, any]:
    reactions_by_id = {}
    for k, v in reactions.items():
        if v.get('id', None) is not None:
            reactions_by_id[v['id']] = v
    return reactions_by_id


base_reagents = parse_compounds(json.load(open('data/current/chemistry/Reagents-Base.json', 'r'))['datum']['reagent'])
disease_reagents = parse_compounds(json.load(open('data/current/chemistry/Reagents-Diseases.json', 'r'))['datum']['reagent']['disease'])
drug_reagents = parse_compounds(json.load(open('data/current/chemistry/Reagents-Drugs.json', 'r'))['datum']['reagent']['drug'])
explosive_reagents = parse_compounds(json.load(open('data/current/chemistry/Reagents-ExplosiveFire.json', 'r'))['datum']['reagent']['combustible'])
food_reagents = parse_compounds(json.load(open('data/current/chemistry/Reagents-FoodDrink.json', 'r'))['datum']['reagent']['fooddrink'])
medical_reagents = parse_compounds(json.load(open('data/current/chemistry/Reagents-Medical.json', 'r'))['datum']['reagent']['medical'])
misc_reagents = parse_compounds(json.load(open('data/current/chemistry/Reagents-Misc.json', 'r'))['datum']['reagent'])
poison_reagents = parse_compounds(json.load(open('data/current/chemistry/Reagents-PoisonEtc.json', 'r'))['datum']['reagent']['harmful'])
all_reagents = {**base_reagents, **disease_reagents, **drug_reagents, **explosive_reagents, **food_reagents, **medical_reagents, **misc_reagents, **poison_reagents}
all_reagents_by_id = get_all_compounds_by_id(all_reagents)

dispensable_reagents = json.load(open('data/chemistry/Chemistry-Machinery.json', 'r'))['obj']['machinery']['chem_dispenser']['var']['list']['dispensable_reagents']

all_reactions = parse_compounds(json.load(open('data/current/chemistry/Chemistry-Recipes.json', 'r'))['datum']['chemical_reaction'])
all_reactions_by_id = get_all_compounds_by_id(all_reactions)


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

def get_reaction(reaction_name: str) -> Dict[str, any] | None:
    if reaction_name + 'stable' in all_reactions.keys() or reaction_name + 'stable' in all_reactions_by_id.keys():
        return get_reaction(reaction_name + 'stable')
    if reaction_name in all_reactions.keys():
        return all_reactions[reaction_name]
    elif reaction_name in all_reactions_by_id.keys():
        return all_reactions_by_id[reaction_name]
    return None

def get_reagent(reagent_name: str) -> Dict[str, any] | None:
    if reagent_name in all_reagents.keys():
        return all_reagents[reagent_name]
    elif reagent_name in all_reagents_by_id.keys():
        return all_reagents_by_id[reagent_name]
    return None

def is_reaction(name: str) -> bool:
    return name in all_reactions.keys() or name in all_reactions_by_id.keys()

def is_reagent(name: str) -> bool:
    return name in all_reagents.keys() or name in all_reagents_by_id.keys()

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
    reaction = get_reaction(reaction_name)
    if reaction.get('required_reagents', None) is None:
        log.warning('No required reagents for reaction: ', reaction_name)
        return {}
    if reaction.get('result_amount', None) is None:
        log.warning(f'No result amount for reaction: {reaction_name}')
    return simplify_reagents(reaction['required_reagents'], reaction.get('result_amount', 1))

def convert_to_units(reagents: Dict[str, float]) -> Dict[str, int]:
    if not reagents:
        return {}
    lowest_amount = sorted(reagents.values())[0]
    as_units = {k: int(v / lowest_amount) for k, v in reagents.items()}
    for k, v in as_units.items():
        if reagents[k] % lowest_amount > .000000001:
            log.warning(f'\tWarning: {k} has a remainder of {reagents[k] % lowest_amount}')
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


def generate_reagent_groups(reactions: List[str]) -> Dict[str, str]:
    for reaction in reactions:
        yield reaction, get_reagent_group(reaction)

def generate_dispensable_groups(reactions: List[str]) -> Dict[str, str]:
    for reaction in reactions:
        yield reaction, get_dispensable_group(reaction)


def generate_all():
    as_reagent_group_dict = {reaction: get_reagent_group_dict(reaction) for reaction in all_reactions}
    as_dispensable_dict = {reaction: get_dispensable_group_dict(reaction) for reaction in all_reactions}
    as_dispensable_changed = {}
    for name, disp_reaction in as_dispensable_dict.items():
        reag_reaction = as_reagent_group_dict.get(name, None)
        if not reag_reaction:
            raise ValueError(f'Reaction {name} not present in both groups')
        name_additions = []
        for reagent, amount in reag_reaction.items():
            if reagent not in disp_reaction.keys():
                name_additions.append(f'*{reagent}({amount})')
        new_name = ' '.join([name, *name_additions])
        as_dispensable_changed[new_name] = disp_reaction

    with open('reactions.py', 'w') as file:
        recipes_as_lists = [[k, as_reagent_group(v)] for k, v in as_dispensable_changed.items()]
        file.write(f'all_recipes = {recipes_as_lists}')


if __name__ == '__main__':
    print(get_reagent_group('cyanide'))


