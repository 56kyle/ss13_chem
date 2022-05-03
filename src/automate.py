

import keyboard
import time


basic_recipes = [
    ['Acetone (27u) *welding fuel(12)', 'carbon=3;hydrogen=3;oxygen=9;'],
    ['Ammonia (30u)', 'hydrogen=30;nitrogen=10;'],
    ['Diethylamine (30u) *374c', 'hydrogen=15;nitrogen=5;ethanol=15;'],
    ['Oil* (30u)', 'hydrogen=10;carbon=10;'],
    ['Phenol *oil(9) (30u)', 'chlorine=10;water=10;'],
    ['Formaldehyde* (20u)', 'ethanol=10;oxygen=10;silver=10;'],
    ['Salt (20u)', 'chlorine=10;sodium=10;water=10;'],
    ['Soda Water (10u)', 'carbon=5;oxygen=5;water=5;'],
    ['Cola (20u)', 'carbon=5;oxygen=5;water=5;sugar=10;'],
    ['Acetaldehyde (30u) *heat', 'chromium=10;oxygen=10;copper=10;ethanol=10;']
]

utility = [
    ['Fluorosurfacant (90u) *Welding Fuel (10u)', 'hydrogen=25;sulfur=15;oxygen=15;fluorine=30;carbon=10;'],
]

acids = [
    ['Sulfuric Acid (10u)', 'hydrogen=5;sulfur=5;oxygen=5;'],
    ['Acetic Acid (27u) *Acetaldehyde (9)', 'oxygen=9;nitrogen=36'],
    ['Fluorosulfuric Acid (30u)', 'sulfur=5;hydrogen=15;oxygen=5;fluorine=10;potassium=10;'],
]

stabilized = [
    ['Stabilizing Agent (10u)', 'iron=5;oxygen=5;hydrogen=5;'],
    ['Phlogiston* (40u)', 'phosphorus=10;plasma=10;hydrogen=5;sulfur=5;oxygen=5;'],
    ['Smoke Powder* (30u)', 'potassium=10;sugar=10;phosphorus=10;'],
    ['Flash Powder *sa(10) (50u)', 'aluminium=10;potassium=10;chlorine=10;sulfur=10;'],
    ['Hootingium *sa(10) (20u)', 'carbon=3;oxygen=13;water=3;sugar=5;phosphorus=10;'],
    ['Dark Matter* (40u)', 'carbon=10;plasma=10;radium=10;'],
    ['Sorium* (40u)', 'mercury=10;carbon=10;nitrogen=10;oxygen=10;'],
]

custom = [
    ['Meat Cube Mix *sa(10) (100u)', 'carbon=10;plasma=30;radium=10;nitrogen=20;water=20;'],
    ['Quick Flamethrower Fuel *sa(20) *wf(10) (100u)', 'phosphorus=20;plasma=10;hydrogen=5;sulfur=5;oxygen=5;potassium=10;sugar=20;ethanol=10;']
]

stimulants = [
    ['Meth Precursor (54u)', 'hydrogen=29;nitrogen=1;ethanol=3;carbon=2;sugar=6;phosphorus=18;iodine=18']
]

medical_recipes = [
    ['Atrazine (30u)', 'chlorine=10;nitrogen=10;hydrogen=10;'],
    ['Stypic Powder (9u)', 'hydrogen=3;oxygen=3;aluminium=2;sulfur=1;'],
    ['Synth Flesh* (24u)', 'carbon=8;hydrogen=3;oxygen=3;aluminium=2;sulfur=1;'],
    ['Silver Sulfadiazine (45u)', 'nitrogen=3;hydrogen=9;silver=9;oxygen=9;sulfur=9;chlorine=9;'],
    ['Ether (27u)', 'chlorine=3;hydrogen=3;water=3;ethanol=9;oxygen=9;'],
    ['Unstable Mutagen (30u)', 'plasma=10;radium=10;chlorine=10;'],
    ['Haloperidol (24u) *Welding Fuel (2)', 'chlorine=6;fluorine=6;aluminium=6;potassium=3;iodine=3;hydrogen=2;carbon=2;'],
    ['Simethicone (30u)', 'oxygen=10;chlorine=10;hydrogen=10;silicon=10;'],
    ['Diphenhydramine (72u) *Welding Fuel (10) *heat', 'carbon=24;hydrogen=15;nitrogen=3;ethanol=27;bromine=18;'],
    ['Crank (u) *Diphenhydramine (10) *Welding Fuel (10) *heat', 'sulfur=5;hydrogen=17;oxygen=5;lithium=10;nitrogen=4;'],
    ['Cryoxadone (90u) *Acetone (30)', 'plasma=50;radium=10;chlorine=10;nitrogen=10;water=10;'],
]

all_recipes = [
    *basic_recipes,
    *utility,
    *acids,
    *stabilized,
    ['Cryostylane (30u)', 'nitrogen=10;plasma=10;water=10;'],
    ['Pyrosium (30u)', 'plasma=10;radium=10;phosphorus=10;'],
    ['Space Glue *phenol(10)formaldehyde(10) (50u)', 'oxygen=10;plasma=10;hydrogen=10;'],
    ['Napalm Goo *wf(10) (30u)', 'sugar=10;ethanol=10;'],
    *custom,
    *stimulants,
    *medical_recipes,
    ['thing', 'chlorine=16;oxygen=10;phosphorus=10;fluorine=10;hydrogen=16;nitrogen=6;'],
    ['thing therm *wf', 'carbon=1;hydrogen=13;chlorine=12;phosphorus=9;fluorine=9;nitrogen=3;'],
    ['thing therm2', 'copper=6;nitrogen=6;oxygen=18;'],
    ['boom', 'nitrogen=2;hydrogen=3;oxygen=1;sodium=1;silver=1;'],
    ['lots of boom', 'nitrogen=28;hydrogen=42;oxygen=14;sodium=14;silver=14;'],
    ['booma', 'nitrogen=2;hydrogen=3;silver=1;sodium=1;chlorine=1;'],
    ['boomb', 'nitrogen=1;copper=1;oxygen=3;']
]


def enter_recipes():
    for recipe in all_recipes:
        keyboard.write(recipe[0])
        time.sleep(0.1)
        keyboard.press_and_release('tab')
        time.sleep(0.1)
        keyboard.write(recipe[1])
        time.sleep(0.1)
        keyboard.press_and_release('tab')
        time.sleep(0.1)
        keyboard.press_and_release('enter')
        time.sleep(0.1)
        keyboard.press_and_release('shift+tab')
        time.sleep(0.1)
        keyboard.press_and_release('shift+tab')
        time.sleep(0.1)


if __name__ == '__main__':
    while not keyboard.is_pressed('space'):
        pass
    enter_recipes()

