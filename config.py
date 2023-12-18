CATIDX_2_CATNAME = {0: 'Aluminium foil',
                    1: 'Battery',
                    2: 'Aluminium blister pack',
                    3: 'Carded blister pack',
                    4: 'Other plastic bottle',
                    5: 'Clear plastic bottle',
                    6: 'Glass bottle',
                    7: 'Plastic bottle cap',
                    8: 'Metal bottle cap',
                    9: 'Broken glass',
                    10: 'Food Can',
                    11: 'Aerosol',
                    12: 'Drink can',
                    13: 'Toilet tube',
                    14: 'Other carton',
                    15: 'Egg carton',
                    16: 'Drink carton',
                    17: 'Corrugated carton',
                    18: 'Meal carton',
                    19: 'Pizza box',
                    20: 'Paper cup',
                    21: 'Disposable plastic cup',
                    22: 'Foam cup',
                    23: 'Glass cup',
                    24: 'Other plastic cup',
                    25: 'Food waste',
                    26: 'Glass jar',
                    27: 'Plastic lid',
                    28: 'Metal lid',
                    29: 'Other plastic',
                    30: 'Magazine paper',
                    31: 'Tissues',
                    32: 'Wrapping paper',
                    33: 'Normal paper',
                    34: 'Paper bag',
                    35: 'Plastified paper bag',
                    36: 'Plastic film',
                    37: 'Six pack rings',
                    38: 'Garbage bag',
                    39: 'Other plastic wrapper',
                    40: 'Single-use carrier bag',
                    41: 'Polypropylene bag',
                    42: 'Crisp packet',
                    43: 'Spread tub',
                    44: 'Tupperware',
                    45: 'Disposable food container',
                    46: 'Foam food container',
                    47: 'Other plastic container',
                    48: 'Plastic glooves',
                    49: 'Plastic utensils',
                    50: 'Pop tab',
                    51: 'Rope & strings',
                    52: 'Scrap metal',
                    53: 'Shoe',
                    54: 'Squeezable tube',
                    55: 'Plastic straw',
                    56: 'Paper straw',
                    57: 'Styrofoam piece',
                    58: 'Unlabeled litter',
                    59: 'Cigarette'}

CATNAME_2_CATIDX = {v: k for k, v in CATIDX_2_CATNAME.items()}

CATNAME_2_EMOJI = {
    'Aluminium foil': '🔩',  # Since there's no specific emoji for aluminum foil, I used a metal-related emoji.
    'Battery': '🔋',
    'Aluminium blister pack': '💊',  # Represents medication, often packaged in blister packs.
    'Carded blister pack': '💊🃏',  # Combination of medication and card for the carded aspect.
    'Other plastic bottle': '🧴',
    'Clear plastic bottle': '🧴',
    'Glass bottle': '🍾',
    'Plastic bottle cap': '🔘',
    'Metal bottle cap': '🔘',
    'Broken glass': '🔨',  # A hammer to represent the breaking of glass.
    'Food Can': '🥫',
    'Aerosol': '🎨',  # Spray paint to represent aerosol.
    'Drink can': '🥤',
    'Toilet tube': '🧻',
    'Other carton': '📦',
    'Egg carton': '🥚📦',  # Eggs and a box to represent an egg carton.
    'Drink carton': '🧃',
    'Corrugated carton': '📦',
    'Meal carton': '🍱',
    'Pizza box': '🍕📦',
    'Paper cup': '🥤',
    'Disposable plastic cup': '🥤',
    'Foam cup': '☕',  # A hot beverage cup to represent a foam cup.
    'Glass cup': '🥃',
    'Other plastic cup': '🥤',
    'Food waste': '🍽️🗑️',  # A plate and a trash can to represent food waste.
    'Glass jar': '🍯',
    'Plastic lid': '🔘',
    'Metal lid': '🔘',
    'Other plastic': '♻️',  # Recycling symbol for general plastic.
    'Magazine paper': '📰',
    'Tissues': '🤧',
    'Wrapping paper': '🎁',
    'Normal paper': '📄',
    'Paper bag': '🛍️',
    'Plastified paper bag': '🛍️',
    'Plastic film': '♻️',
    'Six pack rings': '🍺',  # Beer emoji to represent six-pack rings.
    'Garbage bag': '🗑️',
    'Other plastic wrapper': '♻️',
    'Single-use carrier bag': '🛍️',
    'Polypropylene bag': '♻️',
    'Crisp packet': '🍿',  # Popcorn to represent snacks.
    'Spread tub': '🧈',  # Butter to represent spread.
    'Tupperware': '🥡',  # Takeout box to represent food storage.
    'Disposable food container': '🥡',
    'Foam food container': '🥡',
    'Other plastic container': '♻️',
    'Plastic glooves': '🧤',
    'Plastic utensils': '🍴',
    'Pop tab': '🥤',
    'Rope & strings': '🧵',  # A spool of thread to represent rope and strings.
    'Scrap metal': '🔩',
    'Shoe': '👟',
    'Squeezable tube': '🧴',  # A bottle to represent a squeezable tube.
    'Plastic straw': '🥤',
    'Paper straw': '🥤',
    'Styrofoam piece': '☕',
    'Unlabeled litter': '❓🗑️',  # A question mark and a trash can for unknown litter.
    'Cigarette': '🚬'
}

EN_CATNAME_2_FR_CATNAME = {
    'Aluminium foil': "Papier d'aluminium",
    'Battery': 'Batterie',
    'Aluminium blister pack': 'Plaquette thermoformée en aluminium',
    'Carded blister pack': 'Plaquette thermoformée à carte',
    'Other plastic bottle': 'Autre bouteille en plastique',
    'Clear plastic bottle': 'Bouteille en plastique transparente',
    'Glass bottle': 'Bouteille en verre',
    'Plastic bottle cap': 'Bouchon de bouteille en plastique',
    'Metal bottle cap': 'Bouchon de bouteille en métal',
    'Broken glass': 'Verre brisé',
    'Food Can': 'Boîte de conserve',
    'Aerosol': 'Aérosol',
    'Drink can': 'Canette de boisson',
    'Toilet tube': 'Tube de papier toilette',
    'Other carton': 'Autre carton',
    'Egg carton': 'Boîte à œufs',
    'Drink carton': 'Brique de boisson',
    'Corrugated carton': 'Carton ondulé',
    'Meal carton': 'Boîte alimentaire en carton',
    'Pizza box': 'Boîte à pizza',
    'Paper cup': 'Gobelet en papier',
    'Disposable plastic cup': 'Gobelet en plastique jetable',
    'Foam cup': 'Gobelet en mousse',
    'Glass cup': 'Tasse en verre',
    'Other plastic cup': 'Autre gobelet en plastique',
    'Food waste': 'Déchets alimentaires',
    'Glass jar': 'Pot en verre',
    'Plastic lid': 'Couvercle en plastique',
    'Metal lid': 'Couvercle en métal',
    'Other plastic': 'Autre plastique',
    'Magazine paper': 'Papier de magazine',
    'Tissues': 'Mouchoirs',
    'Wrapping paper': 'Papier cadeau',
    'Normal paper': 'Papier ordinaire',
    'Paper bag': 'Sac en papier',
    'Plastified paper bag': 'Sac en papier plastifié',
    'Plastic film': 'Film plastique',
    'Six pack rings': 'Anneaux de canette',
    'Garbage bag': 'Sac poubelle',
    'Other plastic wrapper': 'Autre emballage en plastique',
    'Single-use carrier bag': 'Sac à usage unique',
    'Polypropylene bag': 'Sac en polypropylène',
    'Crisp packet': 'Paquet de chips',
    'Spread tub': 'Pot de tartinade',
    'Tupperware': 'Tupperware',
    'Disposable food container': 'Contenant alimentaire jetable',
    'Foam food container': 'Contenant alimentaire en mousse',
    'Other plastic container': 'Autre contenant en plastique',
    'Plastic glooves': 'Gants en plastique',
    'Plastic utensils': 'Ustensiles en plastique',
    'Pop tab': 'Onglet de canette',
    'Rope & strings': 'Corde et ficelles',
    'Scrap metal': 'Métal usagé',
    'Shoe': 'Chaussure',
    'Squeezable tube': 'Tube compressible',
    'Plastic straw': 'Paille en plastique',
    'Paper straw': 'Paille en papier',
    'Styrofoam piece': 'Morceau de polystyrène',
    'Unlabeled litter': 'Déchets non étiquetés',
    'Cigarette': 'Cigarette'
}

CATIDX_2_SUPERCATNAME = {0: 'Aluminium foil',
                         1: 'Battery',
                         2: 'Blister pack',
                         3: 'Blister pack',
                         4: 'Bottle',
                         5: 'Bottle',
                         6: 'Bottle',
                         7: 'Bottle cap',
                         8: 'Bottle cap',
                         9: 'Broken glass',
                         10: 'Can',
                         11: 'Can',
                         12: 'Can',
                         13: 'Carton',
                         14: 'Carton',
                         15: 'Carton',
                         16: 'Carton',
                         17: 'Carton',
                         18: 'Carton',
                         19: 'Carton',
                         20: 'Cup',
                         21: 'Cup',
                         22: 'Cup',
                         23: 'Cup',
                         24: 'Cup',
                         25: 'Food waste',
                         26: 'Glass jar',
                         27: 'Lid',
                         28: 'Lid',
                         29: 'Other plastic',
                         30: 'Paper',
                         31: 'Paper',
                         32: 'Paper',
                         33: 'Paper',
                         34: 'Paper bag',
                         35: 'Paper bag',
                         36: 'Plastic bag & wrapper',
                         37: 'Plastic bag & wrapper',
                         38: 'Plastic bag & wrapper',
                         39: 'Plastic bag & wrapper',
                         40: 'Plastic bag & wrapper',
                         41: 'Plastic bag & wrapper',
                         42: 'Plastic bag & wrapper',
                         43: 'Plastic container',
                         44: 'Plastic container',
                         45: 'Plastic container',
                         46: 'Plastic container',
                         47: 'Plastic container',
                         48: 'Plastic glooves',
                         49: 'Plastic utensils',
                         50: 'Pop tab',
                         51: 'Rope & strings',
                         52: 'Scrap metal',
                         53: 'Shoe',
                         54: 'Squeezable tube',
                         55: 'Straw',
                         56: 'Straw',
                         57: 'Styrofoam piece',
                         58: 'Unlabeled litter',
                         59: 'Cigarette'}

SUPERCATIDX_2_SUPERCATNAME = {0: 'Aluminium foil',
                              1: 'Battery',
                              2: 'Blister pack',
                              3: 'Bottle',
                              4: 'Bottle cap',
                              5: 'Broken glass',
                              6: 'Can',
                              7: 'Carton',
                              8: 'Cup',
                              9: 'Food waste',
                              10: 'Glass jar',
                              11: 'Lid',
                              12: 'Other plastic',
                              13: 'Paper',
                              14: 'Paper bag',
                              15: 'Plastic bag & wrapper',
                              16: 'Plastic container',
                              17: 'Plastic glooves',
                              18: 'Plastic utensils',
                              19: 'Pop tab',
                              20: 'Rope & strings',
                              21: 'Scrap metal',
                              22: 'Shoe',
                              23: 'Squeezable tube',
                              24: 'Straw',
                              25: 'Styrofoam piece',
                              26: 'Unlabeled litter',
                              27: 'Cigarette'}
