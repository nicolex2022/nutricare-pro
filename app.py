import random
from flask import Flask, render_template, request

app = Flask(__name__)

# ==================================================
# 1. EXTENDED USDA-STYLE FOOD DATABASE (per 100g)
# ==================================================
# cal (kcal), pro (g), fat (g), carb (g),
# fiber (g), sugar (g), sodium (mg),
# eco, processed, tip


FOOD_DB = {
# ================= GRAINS & STARCH =================
"white rice": {"cal":130,"pro":2.7,"fat":0.3,"carb":28,"fiber":0.4,"sugar":0.1,"sodium":1,"eco":"Medium","processed":"no"},
"brown rice": {"cal":123,"pro":2.7,"fat":1,"carb":26,"fiber":1.8,"sugar":0.4,"sodium":2,"eco":"High","processed":"no"},
"pasta": {"cal":131,"pro":5,"fat":1.1,"carb":25,"fiber":1.8,"sugar":0.6,"sodium":6,"eco":"High","processed":"no"},
"whole wheat pasta": {"cal":124,"pro":5.3,"fat":1.5,"carb":25,"fiber":3.9,"sugar":0.8,"sodium":5,"eco":"Very High","processed":"no"},
"bread": {"cal":265,"pro":9,"fat":3.2,"carb":49,"fiber":2.7,"sugar":5,"sodium":490,"eco":"Medium","processed":"yes"},
"bagel": {"cal":250,"pro":10,"fat":1.5,"carb":48,"fiber":2,"sugar":6,"sodium":430,"eco":"Medium","processed":"yes"},
"oats": {"cal":389,"pro":16.9,"fat":6.9,"carb":66,"fiber":10.6,"sugar":1,"sodium":2,"eco":"Very High","processed":"no"},
"quinoa": {"cal":120,"pro":4.1,"fat":1.9,"carb":21,"fiber":2.8,"sugar":0.9,"sodium":7,"eco":"High","processed":"no"},
"couscous": {"cal":112,"pro":3.8,"fat":0.2,"carb":23,"fiber":1.4,"sugar":0.1,"sodium":5,"eco":"High","processed":"no"},
"potato": {"cal":77,"pro":2,"fat":0.1,"carb":17,"fiber":2.2,"sugar":0.8,"sodium":6,"eco":"High","processed":"no"},
"sweet potato": {"cal":86,"pro":1.6,"fat":0.1,"carb":20,"fiber":3,"sugar":4.2,"sodium":55,"eco":"Very High","processed":"no"},
"corn": {"cal":86,"pro":3.2,"fat":1.2,"carb":19,"fiber":2.7,"sugar":6,"sodium":15,"eco":"High","processed":"no"},
"barley": {"cal":354,"pro":12,"fat":2.3,"carb":73,"fiber":17,"sugar":0.8,"sodium":12,"eco":"High","processed":"no"},
"rye": {"cal":335,"pro":10,"fat":1.6,"carb":76,"fiber":15,"sugar":0.9,"sodium":2,"eco":"High","processed":"no"},
"millet": {"cal":378,"pro":11,"fat":4.2,"carb":72,"fiber":8,"sugar":1,"sodium":5,"eco":"High","processed":"no"},
"buckwheat": {"cal":343,"pro":13,"fat":3.4,"carb":71,"fiber":10,"sugar":0.6,"sodium":1,"eco":"High","processed":"no"},
"spelt": {"cal":338,"pro":14,"fat":2.4,"carb":70,"fiber":10,"sugar":1,"sodium":5,"eco":"High","processed":"no"},
"tapioca": {"cal":358,"pro":0.2,"fat":0.1,"carb":88,"fiber":0.9,"sugar":3.3,"sodium":1,"eco":"Medium","processed":"no"},
"polenta": {"cal":370,"pro":8,"fat":1,"carb":79,"fiber":3,"sugar":0.7,"sodium":3,"eco":"Medium","processed":"no"},
"farro": {"cal":335,"pro":14,"fat":2.5,"carb":70,"fiber":10,"sugar":1,"sodium":2,"eco":"High","processed":"no"},
"rice noodles": {"cal":109,"pro":1.8,"fat":0.2,"carb":24,"fiber":1,"sugar":0.2,"sodium":5,"eco":"Medium","processed":"no"},
"macaroni": {"cal":158,"pro":5.8,"fat":0.9,"carb":30,"fiber":1.5,"sugar":0.8,"sodium":6,"eco":"Medium","processed":"yes"},
"lasagna noodles": {"cal":160,"pro":6,"fat":1,"carb":31,"fiber":2,"sugar":0.5,"sodium":7,"eco":"Medium","processed":"yes"},
"bread roll": {"cal":265,"pro":9,"fat":3,"carb":50,"fiber":2,"sugar":4,"sodium":420,"eco":"Medium","processed":"yes"},
"tortilla": {"cal":218,"pro":5,"fat":3.3,"carb":37,"fiber":2.3,"sugar":1,"sodium":490,"eco":"Medium","processed":"yes"},
"pita bread": {"cal":275,"pro":9,"fat":3.2,"carb":55,"fiber":3,"sugar":5,"sodium":510,"eco":"Medium","processed":"yes"},
"cornmeal": {"cal":370,"pro":9,"fat":1.5,"carb":81,"fiber":7,"sugar":0.6,"sodium":5,"eco":"High","processed":"no"},
"graham crackers": {"cal":413,"pro":6,"fat":10,"carb":77,"fiber":5,"sugar":33,"sodium":340,"eco":"Low","processed":"yes"},
"pretzel": {"cal":380,"pro":8,"fat":3.5,"carb":77,"fiber":3.4,"sugar":3,"sodium":1130,"eco":"Low","processed":"yes"},
"rice cake": {"cal":387,"pro":7.4,"fat":3.3,"carb":84,"fiber":1.5,"sugar":0.6,"sodium":5,"eco":"Medium","processed":"yes"},
"crackers": {"cal":502,"pro":7,"fat":24,"carb":66,"fiber":2.5,"sugar":4,"sodium":450,"eco":"Low","processed":"yes"},
"instant noodles": {"cal":436,"pro":10,"fat":17,"carb":60,"fiber":3,"sugar":2,"sodium":820,"eco":"Low","processed":"yes"},


# ================= MEAT & PROTEIN =================
"chicken breast": {"cal":165,"pro":31,"fat":3.6,"carb":0,"fiber":0,"sugar":0,"sodium":74,"eco":"Medium","processed":"no"},
"chicken thigh": {"cal":209,"pro":26,"fat":11,"carb":0,"fiber":0,"sugar":0,"sodium":82,"eco":"Medium","processed":"no"},
"beef": {"cal":250,"pro":26,"fat":15,"carb":0,"fiber":0,"sugar":0,"sodium":72,"eco":"Low","processed":"no"},
"pork": {"cal":242,"pro":27,"fat":14,"carb":0,"fiber":0,"sugar":0,"sodium":62,"eco":"Low","processed":"no"},
"ham": {"cal":145,"pro":21,"fat":5,"carb":1.5,"fiber":0,"sugar":1.5,"sodium":1200,"eco":"Low","processed":"yes"},
"sausage": {"cal":301,"pro":12,"fat":27,"carb":2,"fiber":0,"sugar":1,"sodium":1240,"eco":"Low","processed":"yes"},
"turkey breast": {"cal":104,"pro":17,"fat":2,"carb":0,"fiber":0,"sugar":0,"sodium":55,"eco":"Medium","processed":"no"},
"tempeh": {"cal":193,"pro":19,"fat":11,"carb":9.4,"fiber":1.4,"sugar":0.5,"sodium":9,"eco":"Very High","processed":"no"},
"tofu": {"cal":76,"pro":8,"fat":4.8,"carb":1.9,"fiber":0.3,"sugar":0.3,"sodium":7,"eco":"Very High","processed":"no"},
"ground beef": {"cal":250,"pro":26,"fat":15,"carb":0,"fiber":0,"sugar":0,"sodium":72,"eco":"Low","processed":"no"},
"bacon": {"cal":541,"pro":37,"fat":42,"carb":1.4,"fiber":0,"sugar":1.4,"sodium":1_717,"eco":"Low","processed":"yes"},
"veal": {"cal":172,"pro":31,"fat":7,"carb":0,"fiber":0,"sugar":0,"sodium":72,"eco":"Low","processed":"no"},
"lamb": {"cal":294,"pro":25,"fat":21,"carb":0,"fiber":0,"sugar":0,"sodium":72,"eco":"Low","processed":"no"},
"duck": {"cal":337,"pro":19,"fat":28,"carb":0,"fiber":0,"sugar":0,"sodium":76,"eco":"Medium","processed":"no"},
"goose": {"cal":305,"pro":29,"fat":23,"carb":0,"fiber":0,"sugar":0,"sodium":82,"eco":"Medium","processed":"no"},
"rabbit": {"cal":173,"pro":33,"fat":3.5,"carb":0,"fiber":0,"sugar":0,"sodium":72,"eco":"High","processed":"no"},
"bison": {"cal":143,"pro":21,"fat":7,"carb":0,"fiber":0,"sugar":0,"sodium":55,"eco":"High","processed":"no"},
"goat": {"cal":122,"pro":20,"fat":3,"carb":0,"fiber":0,"sugar":0,"sodium":72,"eco":"High","processed":"no"},
"venison": {"cal":158,"pro":30,"fat":3,"carb":0,"fiber":0,"sugar":0,"sodium":82,"eco":"High","processed":"no"},
"chicken wings": {"cal":203,"pro":30,"fat":8,"carb":0,"fiber":0,"sugar":0,"sodium":82,"eco":"Medium","processed":"no"},
"chicken drumstick": {"cal":175,"pro":28,"fat":6,"carb":0,"fiber":0,"sugar":0,"sodium":78,"eco":"Medium","processed":"no"},
# ================= FISH & SEAFOOD =================
"salmon": {"cal":208,"pro":20,"fat":13,"carb":0,"fiber":0,"sugar":0,"sodium":59,"eco":"Medium","processed":"no"},
"tuna": {"cal":132,"pro":29,"fat":1,"carb":0,"fiber":0,"sugar":0,"sodium":45,"eco":"Medium","processed":"no"},
"shrimp": {"cal":99,"pro":24,"fat":0.3,"carb":0.2,"fiber":0,"sugar":0,"sodium":111,"eco":"High","processed":"no"},
"cod": {"cal":82,"pro":18,"fat":0.7,"carb":0,"fiber":0,"sugar":0,"sodium":54,"eco":"High","processed":"no"},
"trout": {"cal":148,"pro":20,"fat":7,"carb":0,"fiber":0,"sugar":0,"sodium":50,"eco":"Medium","processed":"no"},
"mackerel": {"cal":205,"pro":19,"fat":13,"carb":0,"fiber":0,"sugar":0,"sodium":90,"eco":"Medium","processed":"no"},
"sardines": {"cal":208,"pro":25,"fat":11,"carb":0,"fiber":0,"sugar":0,"sodium":400,"eco":"Medium","processed":"yes"},
"herring": {"cal":158,"pro":18,"fat":9,"carb":0,"fiber":0,"sugar":0,"sodium":90,"eco":"Medium","processed":"no"},
"crab": {"cal":97,"pro":19,"fat":1.5,"carb":0,"fiber":0,"sugar":0,"sodium":386,"eco":"Medium","processed":"no"},
"lobster": {"cal":89,"pro":19,"fat":0.9,"carb":0,"fiber":0,"sugar":0,"sodium":486,"eco":"Medium","processed":"no"},
"clams": {"cal":74,"pro":12,"fat":0.9,"carb":2.6,"fiber":0,"sugar":0,"sodium":56,"eco":"High","processed":"no"},
"oyster": {"cal":68,"pro":7,"fat":2,"carb":4,"fiber":0,"sugar":0,"sodium":90,"eco":"High","processed":"no"},
"scallops": {"cal":88,"pro":16,"fat":1,"carb":3,"fiber":0,"sugar":0,"sodium":667,"eco":"Medium","processed":"no"},
"squid": {"cal":92,"pro":15,"fat":1.4,"carb":3.1,"fiber":0,"sugar":0,"sodium":44,"eco":"Medium","processed":"no"},
"octopus": {"cal":82,"pro":14,"fat":1,"carb":2.2,"fiber":0,"sugar":0,"sodium":230,"eco":"Medium","processed":"no"},
"anchovy": {"cal":210,"pro":29,"fat":10,"carb":0,"fiber":0,"sugar":0,"sodium":2320,"eco":"Medium","processed":"yes"},
"pollock": {"cal":92,"pro":20,"fat":0.9,"carb":0,"fiber":0,"sugar":0,"sodium":60,"eco":"High","processed":"no"},
"tilapia": {"cal":128,"pro":26,"fat":2.7,"carb":0,"fiber":0,"sugar":0,"sodium":56,"eco":"High","processed":"no"},
"haddock": {"cal":90,"pro":20,"fat":0.8,"carb":0,"fiber":0,"sugar":0,"sodium":60,"eco":"High","processed":"no"},
"yellowfin tuna": {"cal":144,"pro":23,"fat":4,"carb":0,"fiber":0,"sugar":0,"sodium":45,"eco":"Medium","processed":"no"},
"halibut": {"cal":140,"pro":27,"fat":3,"carb":0,"fiber":0,"sugar":0,"sodium":70,"eco":"Medium","processed":"no"},


# ================= EGGS & DAIRY =================
"egg": {"cal":155,"pro":13,"fat":11,"carb":1.1,"fiber":0,"sugar":1.1,"sodium":124,"eco":"Medium","processed":"no"},
"egg white": {"cal":52,"pro":11,"fat":0.2,"carb":0.7,"fiber":0,"sugar":0.7,"sodium":166,"eco":"Medium","processed":"no"},
"milk": {"cal":42,"pro":3.4,"fat":1,"carb":5,"fiber":0,"sugar":5,"sodium":44,"eco":"Low","processed":"yes"},
"yogurt": {"cal":59,"pro":10,"fat":0.4,"carb":3.6,"fiber":0,"sugar":3.2,"sodium":36,"eco":"Medium","processed":"yes"},
"cheese": {"cal":402,"pro":25,"fat":33,"carb":1.3,"fiber":0,"sugar":0.5,"sodium":621,"eco":"Low","processed":"yes"},
"cottage cheese": {"cal":98,"pro":11,"fat":4.3,"carb":3.4,"fiber":0,"sugar":2.7,"sodium":364,"eco":"Low","processed":"yes"},
"butter": {"cal":717,"pro":0.9,"fat":81,"carb":0.1,"fiber":0,"sugar":0.1,"sodium":11,"eco":"Low","processed":"yes"},
"cream": {"cal":340,"pro":2,"fat":37,"carb":3,"fiber":0,"sugar":3,"sodium":40,"eco":"Low","processed":"yes"},
"skim milk": {"cal":34,"pro":3.4,"fat":0.1,"carb":5,"fiber":0,"sugar":5,"sodium":44,"eco":"Low","processed":"yes"},
"evaporated milk": {"cal":134,"pro":7,"fat":7,"carb":10,"fiber":0,"sugar":10,"sodium":92,"eco":"Low","processed":"yes"},
"condensed milk": {"cal":321,"pro":8,"fat":8,"carb":55,"fiber":0,"sugar":55,"sodium":92,"eco":"Low","processed":"yes"},
"parmesan": {"cal":431,"pro":38,"fat":29,"carb":4,"fiber":0,"sugar":0,"sodium":1800,"eco":"Low","processed":"yes"},
"mozzarella": {"cal":280,"pro":28,"fat":17,"carb":3,"fiber":0,"sugar":0.5,"sodium":600,"eco":"Low","processed":"yes"},
"feta": {"cal":264,"pro":14,"fat":21,"carb":4,"fiber":0,"sugar":4,"sodium":900,"eco":"Low","processed":"yes"},
"cream cheese": {"cal":342,"pro":6,"fat":34,"carb":4,"fiber":0,"sugar":4,"sodium":400,"eco":"Low","processed":"yes"},
"ricotta": {"cal":174,"pro":11,"fat":13,"carb":3,"fiber":0,"sugar":3,"sodium":84,"eco":"Low","processed":"yes"},
"blue cheese": {"cal":353,"pro":21,"fat":28,"carb":2,"fiber":0,"sugar":0,"sodium":1200,"eco":"Low","processed":"yes"},
"swiss cheese": {"cal":380,"pro":27,"fat":30,"carb":5,"fiber":0,"sugar":0,"sodium":200,"eco":"Low","processed":"yes"},
"yogurt greek": {"cal":59,"pro":10,"fat":0.4,"carb":3.6,"fiber":0,"sugar":3.2,"sodium":36,"eco":"Medium","processed":"yes"},
"buttermilk": {"cal":40,"pro":3.3,"fat":1,"carb":5,"fiber":0,"sugar":5,"sodium":50,"eco":"Low","processed":"yes"},
# ================= FRUITS =================
"apple": {"cal":52,"pro":0.3,"fat":0.2,"carb":14,"fiber":2.4,"sugar":10,"sodium":1,"eco":"High","processed":"no"},
"banana": {"cal":89,"pro":1.1,"fat":0.3,"carb":23,"fiber":2.6,"sugar":12,"sodium":1,"eco":"Medium","processed":"no"},
"orange": {"cal":47,"pro":0.9,"fat":0.1,"carb":12,"fiber":2.4,"sugar":9,"sodium":0,"eco":"High","processed":"no"},
"strawberry": {"cal":32,"pro":0.7,"fat":0.3,"carb":8,"fiber":2,"sugar":4.9,"sodium":1,"eco":"Medium","processed":"no"},
"grape": {"cal":69,"pro":0.7,"fat":0.2,"carb":18,"fiber":0.9,"sugar":15,"sodium":2,"eco":"Medium","processed":"no"},
"mango": {"cal":60,"pro":0.8,"fat":0.4,"carb":15,"fiber":1.6,"sugar":14,"sodium":1,"eco":"Medium","processed":"no"},
"blueberry": {"cal":57,"pro":0.7,"fat":0.3,"carb":14.5,"fiber":2.4,"sugar":10,"sodium":1,"eco":"High","processed":"no"},
"raspberry": {"cal":52,"pro":1.2,"fat":0.7,"carb":12,"fiber":6.5,"sugar":4.4,"sodium":1,"eco":"High","processed":"no"},
"blackberry": {"cal":43,"pro":1.4,"fat":0.5,"carb":10,"fiber":5.3,"sugar":4.9,"sodium":1,"eco":"High","processed":"no"},
"pineapple": {"cal":50,"pro":0.5,"fat":0.1,"carb":13,"fiber":1.4,"sugar":10,"sodium":1,"eco":"Medium","processed":"no"},
"watermelon": {"cal":30,"pro":0.6,"fat":0.2,"carb":8,"fiber":0.4,"sugar":6,"sodium":1,"eco":"High","processed":"no"},
"peach": {"cal":39,"pro":0.9,"fat":0.3,"carb":10,"fiber":1.5,"sugar":8,"sodium":0,"eco":"High","processed":"no"},
"pear": {"cal":57,"pro":0.4,"fat":0.1,"carb":15,"fiber":3.1,"sugar":10,"sodium":1,"eco":"High","processed":"no"},
"cherry": {"cal":50,"pro":1,"fat":0.3,"carb":12,"fiber":1.6,"sugar":8,"sodium":0,"eco":"Medium","processed":"no"},
"kiwi": {"cal":61,"pro":1.1,"fat":0.5,"carb":15,"fiber":3,"sugar":9,"sodium":3,"eco":"High","processed":"no"},
"papaya": {"cal":43,"pro":0.5,"fat":0.3,"carb":11,"fiber":1.7,"sugar":8,"sodium":8,"eco":"Medium","processed":"no"},
"plum": {"cal":46,"pro":0.7,"fat":0.3,"carb":11.4,"fiber":1.4,"sugar":9.9,"sodium":0,"eco":"High","processed":"no"},
"apricot": {"cal":48,"pro":0.5,"fat":0.4,"carb":11,"fiber":2,"sugar":9,"sodium":1,"eco":"High","processed":"no"},
"fig": {"cal":74,"pro":0.8,"fat":0.3,"carb":19,"fiber":2.9,"sugar":16,"sodium":1,"eco":"Medium","processed":"no"},
"grapefruit": {"cal":42,"pro":0.8,"fat":0.1,"carb":11,"fiber":1.1,"sugar":8.5,"sodium":0,"eco":"High","processed":"no"},


# ================= VEGETABLES =================
"broccoli": {"cal":34,"pro":2.8,"fat":0.4,"carb":7,"fiber":2.6,"sugar":1.7,"sodium":33,"eco":"Very High","processed":"no"},
"spinach": {"cal":23,"pro":2.9,"fat":0.4,"carb":3.6,"fiber":2.2,"sugar":0.4,"sodium":79,"eco":"Very High","processed":"no"},
"tomato": {"cal":18,"pro":0.9,"fat":0.2,"carb":3.9,"fiber":1.2,"sugar":2.6,"sodium":5,"eco":"High","processed":"no"},
"cucumber": {"cal":16,"pro":0.8,"fat":0.1,"carb":3.6,"fiber":0.5,"sugar":1.5,"sodium":2,"eco":"High","processed":"no"},
"carrot": {"cal":41,"pro":0.9,"fat":0.2,"carb":10,"fiber":2.8,"sugar":4.7,"sodium":69,"eco":"Very High","processed":"no"},
"bell pepper": {"cal":31,"pro":1,"fat":0.3,"carb":6,"fiber":2.1,"sugar":4.2,"sodium":2,"eco":"Very High","processed":"no"},
"onion": {"cal":40,"pro":1.1,"fat":0.1,"carb":9,"fiber":1.7,"sugar":4.2,"sodium":4,"eco":"High","processed":"no"},
"garlic": {"cal":149,"pro":6.4,"fat":0.5,"carb":33,"fiber":2.1,"sugar":1,"sodium":17,"eco":"High","processed":"no"},
"potato": {"cal":77,"pro":2,"fat":0.1,"carb":17,"fiber":2.2,"sugar":0.8,"sodium":6,"eco":"High","processed":"no"},
"sweet potato": {"cal":86,"pro":1.6,"fat":0.1,"carb":20,"fiber":3,"sugar":4.2,"sodium":55,"eco":"Very High","processed":"no"},
"lettuce": {"cal":15,"pro":1,"fat":0.2,"carb":2.9,"fiber":1.3,"sugar":1.3,"sodium":28,"eco":"Very High","processed":"no"},
"kale": {"cal":49,"pro":4.3,"fat":0.9,"carb":9,"fiber":2,"sugar":2,"sodium":38,"eco":"Very High","processed":"no"},
"cabbage": {"cal":25,"pro":1.3,"fat":0.1,"carb":6,"fiber":2.5,"sugar":3.2,"sodium":18,"eco":"Very High","processed":"no"},
"cauliflower": {"cal":25,"pro":2,"fat":0.3,"carb":5,"fiber":2,"sugar":1.9,"sodium":30,"eco":"Very High","processed":"no"},
"zucchini": {"cal":17,"pro":1.2,"fat":0.3,"carb":3.1,"fiber":1,"sugar":2.5,"sodium":3,"eco":"Very High","processed":"no"},
"eggplant": {"cal":25,"pro":1,"fat":0.2,"carb":6,"fiber":3,"sugar":3.2,"sodium":2,"eco":"High","processed":"no"},
"mushroom": {"cal":22,"pro":3.1,"fat":0.3,"carb":3.3,"fiber":1,"sugar":2,"sodium":5,"eco":"High","processed":"no"},
"peas": {"cal":81,"pro":5.4,"fat":0.4,"carb":14,"fiber":5,"sugar":5.7,"sodium":5,"eco":"High","processed":"no"},
"corn": {"cal":86,"pro":3.3,"fat":1.2,"carb":19,"fiber":2.7,"sugar":6.3,"sodium":1,"eco":"High","processed":"no"},
# ================= LEGUMES & BEANS =================
"lentils": {"cal":116,"pro":9,"fat":0.4,"carb":20,"fiber":8,"sugar":1.8,"sodium":2,"eco":"Very High","processed":"no"},
"chickpeas": {"cal":164,"pro":8.9,"fat":2.6,"carb":27,"fiber":7.6,"sugar":4.8,"sodium":24,"eco":"Very High","processed":"no"},
"black beans": {"cal":132,"pro":8.9,"fat":0.5,"carb":23,"fiber":8.7,"sugar":0.3,"sodium":1,"eco":"Very High","processed":"no"},
"kidney beans": {"cal":127,"pro":8.7,"fat":0.5,"carb":22,"fiber":6.4,"sugar":0.3,"sodium":2,"eco":"Very High","processed":"no"},
"pinto beans": {"cal":143,"pro":9,"fat":0.8,"carb":27,"fiber":9,"sugar":0.3,"sodium":2,"eco":"Very High","processed":"no"},
"green peas": {"cal":81,"pro":5.4,"fat":0.4,"carb":14,"fiber":5,"sugar":5.7,"sodium":5,"eco":"High","processed":"no"},
"soybeans": {"cal":172,"pro":16.6,"fat":9,"carb":9.9,"fiber":6,"sugar":3,"sodium":2,"eco":"Very High","processed":"no"},
"edamame": {"cal":121,"pro":11,"fat":5,"carb":10,"fiber":5,"sugar":2,"sodium":6,"eco":"Very High","processed":"no"},
"split peas": {"cal":118,"pro":8,"fat":0.4,"carb":21,"fiber":8,"sugar":2,"sodium":2,"eco":"Very High","processed":"no"},
"black-eyed peas": {"cal":114,"pro":7.7,"fat":0.5,"carb":21,"fiber":6.5,"sugar":3,"sodium":2,"eco":"Very High","processed":"no"},


# ================= NUTS & SEEDS =================
"almonds": {"cal":579,"pro":21,"fat":50,"carb":22,"fiber":12.5,"sugar":4.3,"sodium":1,"eco":"Medium","processed":"no"},
"walnuts": {"cal":654,"pro":15,"fat":65,"carb":14,"fiber":6.7,"sugar":2.6,"sodium":2,"eco":"Medium","processed":"no"},
"cashews": {"cal":553,"pro":18,"fat":44,"carb":30,"fiber":3.3,"sugar":5.2,"sodium":12,"eco":"Medium","processed":"no"},
"peanuts": {"cal":567,"pro":26,"fat":49,"carb":16,"fiber":8.5,"sugar":4.7,"sodium":18,"eco":"Medium","processed":"no"},
"pecans": {"cal":691,"pro":9,"fat":72,"carb":14,"fiber":9.6,"sugar":4,"sodium":0,"eco":"Medium","processed":"no"},
"hazelnuts": {"cal":628,"pro":15,"fat":61,"carb":17,"fiber":10,"sugar":4.3,"sodium":0,"eco":"Medium","processed":"no"},
"pistachios": {"cal":562,"pro":20,"fat":45,"carb":28,"fiber":10.3,"sugar":7.7,"sodium":1,"eco":"Medium","processed":"no"},
"sunflower seeds": {"cal":584,"pro":20,"fat":51,"carb":20,"fiber":8.6,"sugar":2.6,"sodium":2,"eco":"Medium","processed":"no"},
"pumpkin seeds": {"cal":559,"pro":30,"fat":49,"carb":10,"fiber":6,"sugar":1.4,"sodium":7,"eco":"Medium","processed":"no"},
"chia seeds": {"cal":486,"pro":16,"fat":31,"carb":42,"fiber":34,"sugar":0,"sodium":16,"eco":"High","processed":"no"},


# ================= OTHER GRAINS & STARCH =================
"quinoa": {"cal":120,"pro":4.1,"fat":1.9,"carb":21,"fiber":2.8,"sugar":0.9,"sodium":7,"eco":"High","processed":"no"},
"couscous": {"cal":112,"pro":3.8,"fat":0.2,"carb":23,"fiber":1.4,"sugar":0.1,"sodium":5,"eco":"High","processed":"no"},
"barley": {"cal":123,"pro":2.3,"fat":0.4,"carb":28,"fiber":3.8,"sugar":0.3,"sodium":5,"eco":"High","processed":"no"},
"millet": {"cal":119,"pro":3.5,"fat":1,"carb":23,"fiber":1.3,"sugar":0.6,"sodium":5,"eco":"High","processed":"no"},
"buckwheat": {"cal":92,"pro":3.4,"fat":0.6,"carb":20,"fiber":2.7,"sugar":0.9,"sodium":1,"eco":"High","processed":"no"},
"oatmeal": {"cal":389,"pro":16.9,"fat":6.9,"carb":66,"fiber":10.6,"sugar":1,"sodium":2,"eco":"Very High","processed":"no"},
"cornmeal": {"cal":370,"pro":9,"fat":4.7,"carb":77,"fiber":7,"sugar":0.6,"sodium":35,"eco":"High","processed":"no"},
"rice noodles": {"cal":109,"pro":3,"fat":0.9,"carb":24,"fiber":1,"sugar":0.5,"sodium":5,"eco":"Medium","processed":"no"},
"whole wheat bread": {"cal":247,"pro":13,"fat":4.2,"carb":41,"fiber":6,"sugar":5,"sodium":400,"eco":"High","processed":"yes"},
"white bread": {"cal":265,"pro":9,"fat":3.2,"carb":49,"fiber":2.7,"sugar":5,"sodium":490,"eco":"Medium","processed":"yes"},
# ================= DISHES & PREPARED FOODS =================
"spaghetti bolognese": {"cal":158,"pro":7.5,"fat":5.5,"carb":20,"fiber":2.5,"sugar":4,"sodium":350,"eco":"Medium","processed":"yes"},
"chicken curry": {"cal":200,"pro":15,"fat":12,"carb":8,"fiber":1.5,"sugar":3,"sodium":450,"eco":"Medium","processed":"yes"},
"beef stew": {"cal":210,"pro":18,"fat":12,"carb":10,"fiber":2,"sugar":2,"sodium":400,"eco":"Low","processed":"yes"},
"grilled salmon with veggies": {"cal":220,"pro":23,"fat":12,"carb":6,"fiber":3,"sugar":2,"sodium":300,"eco":"Medium","processed":"no"},
"chicken stir fry": {"cal":180,"pro":16,"fat":9,"carb":12,"fiber":2,"sugar":3,"sodium":350,"eco":"Medium","processed":"no"},
"beef burger": {"cal":295,"pro":17,"fat":18,"carb":22,"fiber":1.5,"sugar":4,"sodium":500,"eco":"Low","processed":"yes"},
"cheeseburger": {"cal":303,"pro":18,"fat":20,"carb":23,"fiber":1.5,"sugar":4.5,"sodium":530,"eco":"Low","processed":"yes"},
"margherita pizza": {"cal":280,"pro":12,"fat":10,"carb":33,"fiber":2,"sugar":4,"sodium":620,"eco":"Low","processed":"yes"},
"pepperoni pizza": {"cal":310,"pro":14,"fat":14,"carb":33,"fiber":2,"sugar":4,"sodium":680,"eco":"Low","processed":"yes"},
"fried rice": {"cal":250,"pro":8,"fat":9,"carb":34,"fiber":2,"sugar":3,"sodium":420,"eco":"Medium","processed":"yes"},
"omelette": {"cal":154,"pro":11,"fat":11,"carb":1,"fiber":0.2,"sugar":1,"sodium":170,"eco":"Medium","processed":"no"},
"scrambled eggs": {"cal":147,"pro":10,"fat":11,"carb":1,"fiber":0,"sugar":1,"sodium":166,"eco":"Medium","processed":"no"},
"fried chicken": {"cal":320,"pro":23,"fat":18,"carb":15,"fiber":1,"sugar":0.5,"sodium":600,"eco":"Medium","processed":"yes"},
"roast chicken": {"cal":190,"pro":27,"fat":8,"carb":0,"fiber":0,"sugar":0,"sodium":250,"eco":"Medium","processed":"no"},
"grilled chicken": {"cal":165,"pro":31,"fat":4,"carb":0,"fiber":0,"sugar":0,"sodium":70,"eco":"Medium","processed":"no"},
"pancakes": {"cal":227,"pro":6,"fat":8,"carb":34,"fiber":1.5,"sugar":7,"sodium":330,"eco":"Medium","processed":"yes"},
"waffles": {"cal":291,"pro":6,"fat":12,"carb":41,"fiber":2,"sugar":8,"sodium":510,"eco":"Medium","processed":"yes"},
"mac and cheese": {"cal":310,"pro":12,"fat":15,"carb":35,"fiber":1.5,"sugar":5,"sodium":550,"eco":"Low","processed":"yes"},
"lasagna": {"cal":336,"pro":17,"fat":18,"carb":28,"fiber":2,"sugar":5,"sodium":600,"eco":"Low","processed":"yes"},
"tacos": {"cal":226,"pro":12,"fat":12,"carb":20,"fiber":3,"sugar":2,"sodium":420,"eco":"Medium","processed":"yes"},
"burrito": {"cal":290,"pro":14,"fat":12,"carb":36,"fiber":4,"sugar":2.5,"sodium":500,"eco":"Medium","processed":"yes"},
"chili con carne": {"cal":250,"pro":16,"fat":10,"carb":18,"fiber":4,"sugar":3,"sodium":420,"eco":"Medium","processed":"yes"},
"shepherd's pie": {"cal":320,"pro":18,"fat":15,"carb":28,"fiber":3,"sugar":4,"sodium":580,"eco":"Low","processed":"yes"},
"beef tacos": {"cal":250,"pro":15,"fat":12,"carb":20,"fiber":3,"sugar":2,"sodium":420,"eco":"Low","processed":"yes"},
"chicken nuggets": {"cal":290,"pro":15,"fat":17,"carb":19,"fiber":1,"sugar":0.5,"sodium":600,"eco":"Low","processed":"yes"},
"fish and chips": {"cal":430,"pro":20,"fat":22,"carb":40,"fiber":3,"sugar":2,"sodium":850,"eco":"Low","processed":"yes"},
"beef steak": {"cal":271,"pro":25,"fat":18,"carb":0,"fiber":0,"sugar":0,"sodium":72,"eco":"Low","processed":"no"},
"meatloaf": {"cal":280,"pro":20,"fat":15,"carb":18,"fiber":2,"sugar":3,"sodium":520,"eco":"Low","processed":"yes"},
"chicken parmesan": {"cal":350,"pro":28,"fat":20,"carb":22,"fiber":2,"sugar":4,"sodium":600,"eco":"Low","processed":"yes"},
"fettuccine alfredo": {"cal":400,"pro":15,"fat":22,"carb":40,"fiber":2,"sugar":5,"sodium":600,"eco":"Low","processed":"yes"},
"pad thai": {"cal":350,"pro":14,"fat":16,"carb":45,"fiber":3,"sugar":8,"sodium":700,"eco":"Medium","processed":"yes"},
"pho": {"cal":350,"pro":18,"fat":10,"carb":45,"fiber":3,"sugar":6,"sodium":650,"eco":"Medium","processed":"no"},
"ramen": {"cal":436,"pro":17,"fat":14,"carb":60,"fiber":3,"sugar":5,"sodium":900,"eco":"Low","processed":"yes"},
"sushi roll": {"cal":200,"pro":6,"fat":5,"carb":32,"fiber":2,"sugar":3,"sodium":400,"eco":"Medium","processed":"yes"},
"tempura": {"cal":350,"pro":7,"fat":22,"carb":30,"fiber":2,"sugar":3,"sodium":550,"eco":"Low","processed":"yes"},
"spring roll": {"cal":150,"pro":3,"fat":7,"carb":20,"fiber":2,"sugar":2,"sodium":320,"eco":"Low","processed":"yes"},
"dumplings": {"cal":200,"pro":8,"fat":6,"carb":28,"fiber":2,"sugar":2,"sodium":420,"eco":"Medium","processed":"yes"},
"lasagna vegetarian": {"cal":300,"pro":12,"fat":14,"carb":32,"fiber":4,"sugar":6,"sodium":580,"eco":"Medium","processed":"yes"},
"stuffed peppers": {"cal":180,"pro":6,"fat":8,"carb":20,"fiber":4,"sugar":5,"sodium":300,"eco":"Medium","processed":"no"},
"falafel": {"cal":330,"pro":13,"fat":17,"carb":31,"fiber":5,"sugar":2,"sodium":450,"eco":"High","processed":"yes"},
"hummus": {"cal":166,"pro":8,"fat":9,"carb":14,"fiber":6,"sugar":0.3,"sodium":400,"eco":"High","processed":"yes"},
"guacamole": {"cal":150,"pro":2,"fat":13,"carb":8,"fiber":5,"sugar":1,"sodium":250,"eco":"Medium","processed":"yes"},
"caesar salad": {"cal":180,"pro":7,"fat":12,"carb":10,"fiber":2,"sugar":2,"sodium":420,"eco":"Medium","processed":"yes"},
"greek salad": {"cal":120,"pro":4,"fat":7,"carb":8,"fiber":2,"sugar":3,"sodium":300,"eco":"High","processed":"no"},
"caprese salad": {"cal":220,"pro":10,"fat":18,"carb":5,"fiber":1,"sugar":4,"sodium":200,"eco":"High","processed":"no"},
"tuna salad": {"cal":190,"pro":15,"fat":12,"carb":5,"fiber":2,"sugar":1,"sodium":350,"eco":"Medium","processed":"yes"},
"potato salad": {"cal":220,"pro":4,"fat":15,"carb":20,"fiber":2,"sugar":2,"sodium":400,"eco":"Medium","processed":"yes"},
"coleslaw": {"cal":150,"pro":1,"fat":10,"carb":14,"fiber":2,"sugar":6,"sodium":300,"eco":"Medium","processed":"yes"},
"mashed potato": {"cal":88,"pro":2,"fat":3,"carb":13,"fiber":1.2,"sugar":1,"sodium":150,"eco":"High","processed":"no"},
# ================= SNACKS =================
"granola bar": {"cal":190,"pro":4,"fat":7,"carb":29,"fiber":3,"sugar":12,"sodium":120,"eco":"Medium","processed":"yes"},
"protein bar": {"cal":220,"pro":20,"fat":8,"carb":22,"fiber":5,"sugar":7,"sodium":180,"eco":"Medium","processed":"yes"},
"mixed nuts": {"cal":607,"pro":20,"fat":54,"carb":22,"fiber":9,"sugar":4,"sodium":5,"eco":"High","processed":"no"},
"almonds": {"cal":579,"pro":21,"fat":50,"carb":22,"fiber":12,"sugar":3,"sodium":1,"eco":"High","processed":"no"},
"cashews": {"cal":553,"pro":18,"fat":44,"carb":30,"fiber":3,"sugar":6,"sodium":12,"eco":"High","processed":"no"},
"peanuts": {"cal":567,"pro":26,"fat":49,"carb":16,"fiber":8,"sugar":4,"sodium":18,"eco":"High","processed":"no"},
"walnuts": {"cal":654,"pro":15,"fat":65,"carb":14,"fiber":7,"sugar":2,"sodium":2,"eco":"High","processed":"no"},
"cashew trail mix": {"cal":471,"pro":13,"fat":30,"carb":38,"fiber":5,"sugar":18,"sodium":120,"eco":"Medium","processed":"yes"},
"pumpkin seeds": {"cal":559,"pro":30,"fat":49,"carb":11,"fiber":6,"sugar":1,"sodium":7,"eco":"High","processed":"no"},
"sunflower seeds": {"cal":584,"pro":21,"fat":51,"carb":20,"fiber":9,"sugar":2,"sodium":2,"eco":"High","processed":"no"},
"pretzels": {"cal":380,"pro":9,"fat":3.3,"carb":77,"fiber":4,"sugar":3,"sodium":1600,"eco":"Low","processed":"yes"},
"potato chips": {"cal":536,"pro":7,"fat":35,"carb":53,"fiber":4,"sugar":0.5,"sodium":525,"eco":"Low","processed":"yes"},
"tortilla chips": {"cal":496,"pro":7,"fat":24,"carb":63,"fiber":5,"sugar":1,"sodium":600,"eco":"Low","processed":"yes"},
"cheese crackers": {"cal":502,"pro":9,"fat":27,"carb":55,"fiber":3,"sugar":2,"sodium":700,"eco":"Low","processed":"yes"},
"rice cakes": {"cal":387,"pro":7,"fat":4,"carb":84,"fiber":1,"sugar":0.7,"sodium":7,"eco":"High","processed":"yes"},
"popcorn buttered": {"cal":535,"pro":7,"fat":35,"carb":50,"fiber":5,"sugar":0.3,"sodium":400,"eco":"Low","processed":"yes"},
"popcorn plain": {"cal":375,"pro":12,"fat":4,"carb":77,"fiber":15,"sugar":0.9,"sodium":5,"eco":"High","processed":"no"},
"chocolate bar": {"cal":546,"pro":5,"fat":31,"carb":61,"fiber":7,"sugar":48,"sodium":24,"eco":"Low","processed":"yes"},
"dark chocolate": {"cal":598,"pro":7,"fat":43,"carb":46,"fiber":11,"sugar":24,"sodium":20,"eco":"Medium","processed":"yes"},
"milk chocolate": {"cal":535,"pro":6,"fat":30,"carb":59,"fiber":3,"sugar":52,"sodium":30,"eco":"Low","processed":"yes"},
"candy": {"cal":400,"pro":0,"fat":0.5,"carb":100,"fiber":0,"sugar":90,"sodium":10,"eco":"Low","processed":"yes"},
"gummy bears": {"cal":350,"pro":7,"fat":1,"carb":80,"fiber":0,"sugar":55,"sodium":15,"eco":"Low","processed":"yes"},
"marshmallows": {"cal":318,"pro":0,"fat":0,"carb":81,"fiber":0,"sugar":60,"sodium":30,"eco":"Low","processed":"yes"},
"peanut butter": {"cal":588,"pro":25,"fat":50,"carb":20,"fiber":6,"sugar":9,"sodium":17,"eco":"High","processed":"yes"},
"almond butter": {"cal":614,"pro":21,"fat":55,"carb":20,"fiber":10,"sugar":4,"sodium":1,"eco":"High","processed":"yes"},
"fruit leather": {"cal":360,"pro":2,"fat":0.5,"carb":90,"fiber":3,"sugar":65,"sodium":25,"eco":"Low","processed":"yes"},
"yogurt snack": {"cal":150,"pro":4,"fat":3,"carb":28,"fiber":0.5,"sugar":18,"sodium":50,"eco":"Medium","processed":"yes"},
"pudding cup": {"cal":150,"pro":3,"fat":5,"carb":24,"fiber":0.5,"sugar":18,"sodium":80,"eco":"Medium","processed":"yes"},
"instant noodles snack": {"cal":380,"pro":8,"fat":14,"carb":54,"fiber":3,"sugar":2,"sodium":900,"eco":"Low","processed":"yes"},
"beef jerky": {"cal":410,"pro":33,"fat":27,"carb":3,"fiber":0,"sugar":5,"sodium":1150,"eco":"Low","processed":"yes"},
"turkey jerky": {"cal":410,"pro":30,"fat":25,"carb":4,"fiber":0,"sugar":4,"sodium":1100,"eco":"Low","processed":"yes"},
"cheese stick": {"cal":80,"pro":6,"fat":6,"carb":1,"fiber":0,"sugar":0.5,"sodium":200,"eco":"Low","processed":"yes"},
"string cheese": {"cal":80,"pro":7,"fat":6,"carb":1,"fiber":0,"sugar":0.5,"sodium":200,"eco":"Low","processed":"yes"},
"cracker sandwich": {"cal":200,"pro":4,"fat":10,"carb":24,"fiber":1,"sugar":5,"sodium":300,"eco":"Low","processed":"yes"},
"mini muffins": {"cal":110,"pro":2,"fat":5,"carb":16,"fiber":1,"sugar":9,"sodium":150,"eco":"Low","processed":"yes"},
"cupcake": {"cal":235,"pro":3,"fat":12,"carb":33,"fiber":1,"sugar":22,"sodium":210,"eco":"Low","processed":"yes"},
"donut": {"cal":452,"pro":5,"fat":25,"carb":51,"fiber":2,"sugar":24,"sodium":326,"eco":"Low","processed":"yes"},
"croissant": {"cal":406,"pro":8,"fat":21,"carb":45,"fiber":2,"sugar":7,"sodium":396,"eco":"Low","processed":"yes"},
"pretzel sticks": {"cal":380,"pro":9,"fat":3,"carb":77,"fiber":4,"sugar":3,"sodium":1600,"eco":"Low","processed":"yes"},
"fruit cup": {"cal":60,"pro":0.5,"fat":0.2,"carb":15,"fiber":2,"sugar":12,"sodium":5,"eco":"High","processed":"yes"},
"apple chips": {"cal":350,"pro":1,"fat":0.5,"carb":88,"fiber":6,"sugar":70,"sodium":5,"eco":"Medium","processed":"yes"},
"banana chips": {"cal":519,"pro":2,"fat":27,"carb":58,"fiber":4,"sugar":29,"sodium":15,"eco":"Medium","processed":"yes"},
"rice crackers": {"cal":387,"pro":7,"fat":4,"carb":84,"fiber":1,"sugar":0.7,"sodium":7,"eco":"High","processed":"yes"},
"trail mix chocolate": {"cal":471,"pro":10,"fat":25,"carb":50,"fiber":5,"sugar":25,"sodium":150,"eco":"Medium","processed":"yes"},
# ================= DRINKS =================
"water": {"cal":0,"pro":0,"fat":0,"carb":0,"fiber":0,"sugar":0,"sodium":0,"eco":"Very High","processed":"no"},
"cola": {"cal":42,"pro":0,"fat":0,"carb":11,"fiber":0,"sugar":11,"sodium":4,"eco":"Low","processed":"yes"},
"diet cola": {"cal":1,"pro":0,"fat":0,"carb":0,"fiber":0,"sugar":0,"sodium":40,"eco":"Low","processed":"yes"},
"orange juice": {"cal":45,"pro":0.7,"fat":0.2,"carb":10,"fiber":0.2,"sugar":8.4,"sodium":1,"eco":"Medium","processed":"yes"},
"apple juice": {"cal":46,"pro":0.1,"fat":0.1,"carb":11,"fiber":0.2,"sugar":10,"sodium":1,"eco":"Medium","processed":"yes"},
"grape juice": {"cal":60,"pro":0.6,"fat":0.2,"carb":15,"fiber":0.1,"sugar":13,"sodium":2,"eco":"Medium","processed":"yes"},
"lemonade": {"cal":99,"pro":0.1,"fat":0,"carb":25,"fiber":0,"sugar":24,"sodium":5,"eco":"Low","processed":"yes"},
"milk": {"cal":42,"pro":3.4,"fat":1,"carb":5,"fiber":0,"sugar":5,"sodium":44,"eco":"Low","processed":"yes"},
"soy milk": {"cal":54,"pro":3,"fat":1.8,"carb":6,"fiber":0.6,"sugar":4,"sodium":44,"eco":"High","processed":"yes"},
"almond milk": {"cal":15,"pro":0.6,"fat":1.1,"carb":0.6,"fiber":0.2,"sugar":0.2,"sodium":15,"eco":"High","processed":"yes"},
"oat milk": {"cal":43,"pro":1,"fat":1,"carb":7,"fiber":0.5,"sugar":4,"sodium":50,"eco":"High","processed":"yes"},
"coffee black": {"cal":2,"pro":0.3,"fat":0,"carb":0,"fiber":0,"sugar":0,"sodium":5,"eco":"High","processed":"no"},
"coffee latte": {"cal":120,"pro":6,"fat":4.5,"carb":12,"fiber":0,"sugar":10,"sodium":80,"eco":"Medium","processed":"yes"},
"tea black": {"cal":1,"pro":0,"fat":0,"carb":0.3,"fiber":0,"sugar":0,"sodium":1,"eco":"High","processed":"no"},
"green tea": {"cal":1,"pro":0,"fat":0,"carb":0.3,"fiber":0,"sugar":0,"sodium":1,"eco":"High","processed":"no"},
"herbal tea": {"cal":1,"pro":0,"fat":0,"carb":0.3,"fiber":0,"sugar":0,"sodium":1,"eco":"High","processed":"no"},
"smoothie fruit": {"cal":130,"pro":1,"fat":0.5,"carb":31,"fiber":3,"sugar":24,"sodium":10,"eco":"Medium","processed":"yes"},
"smoothie protein": {"cal":200,"pro":20,"fat":4,"carb":25,"fiber":3,"sugar":15,"sodium":50,"eco":"Medium","processed":"yes"},
"energy drink": {"cal":45,"pro":0,"fat":0,"carb":12,"fiber":0,"sugar":12,"sodium":80,"eco":"Low","processed":"yes"},
"sports drink": {"cal":50,"pro":0,"fat":0,"carb":13,"fiber":0,"sugar":12,"sodium":110,"eco":"Low","processed":"yes"},
"coconut water": {"cal":19,"pro":0.7,"fat":0.2,"carb":3.7,"fiber":1,"sugar":2.6,"sodium":105,"eco":"High","processed":"no"},
"milkshake vanilla": {"cal":207,"pro":8,"fat":7,"carb":32,"fiber":0,"sugar":28,"sodium":150,"eco":"Low","processed":"yes"},
"milkshake chocolate": {"cal":214,"pro":8,"fat":7,"carb":34,"fiber":0,"sugar":29,"sodium":150,"eco":"Low","processed":"yes"},
"milkshake strawberry": {"cal":212,"pro":7,"fat":7,"carb":33,"fiber":0,"sugar":27,"sodium":150,"eco":"Low","processed":"yes"},
"hot chocolate": {"cal":190,"pro":4,"fat":7,"carb":26,"fiber":1,"sugar":21,"sodium":80,"eco":"Low","processed":"yes"},
"chai latte": {"cal":120,"pro":4,"fat":3,"carb":20,"fiber":1,"sugar":14,"sodium":60,"eco":"Medium","processed":"yes"},
"matcha latte": {"cal":80,"pro":3,"fat":2,"carb":10,"fiber":0.5,"sugar":7,"sodium":60,"eco":"Medium","processed":"yes"},
"kombucha": {"cal":30,"pro":0,"fat":0,"carb":7,"fiber":0,"sugar":6,"sodium":10,"eco":"High","processed":"yes"},
"iced coffee": {"cal":80,"pro":3,"fat":1.5,"carb":15,"fiber":0,"sugar":12,"sodium":50,"eco":"Medium","processed":"yes"},
"iced tea": {"cal":90,"pro":0,"fat":0,"carb":23,"fiber":0,"sugar":22,"sodium":15,"eco":"Medium","processed":"yes"},
"lemon water": {"cal":6,"pro":0.1,"fat":0,"carb":2,"fiber":0.1,"sugar":0.6,"sodium":1,"eco":"Very High","processed":"no"},
"apple cider": {"cal":120,"pro":0,"fat":0,"carb":28,"fiber":0,"sugar":24,"sodium":5,"eco":"Medium","processed":"yes"},
"sparkling water": {"cal":0,"pro":0,"fat":0,"carb":0,"fiber":0,"sugar":0,"sodium":10,"eco":"Very High","processed":"no"},
"wine red": {"cal":85,"pro":0,"fat":0,"carb":2.6,"fiber":0,"sugar":0.9,"sodium":7,"eco":"Low","processed":"yes"},
"wine white": {"cal":82,"pro":0,"fat":0,"carb":2.7,"fiber":0,"sugar":0.9,"sodium":7,"eco":"Low","processed":"yes"},
"beer": {"cal":43,"pro":0.5,"fat":0,"carb":3.6,"fiber":0,"sugar":0,"sodium":14,"eco":"Low","processed":"yes"},
"lager": {"cal":42,"pro":0.4,"fat":0,"carb":3,"fiber":0,"sugar":0,"sodium":14,"eco":"Low","processed":"yes"},
"ale": {"cal":55,"pro":0.5,"fat":0,"carb":4,"fiber":0,"sugar":0,"sodium":16,"eco":"Low","processed":"yes"},
"cider": {"cal":50,"pro":0,"fat":0,"carb":12,"fiber":0,"sugar":10,"sodium":5,"eco":"Low","processed":"yes"},
"smoothie green": {"cal":120,"pro":2,"fat":0.5,"carb":28,"fiber":3,"sugar":15,"sodium":10,"eco":"Medium","processed":"yes"},


}


# ==================================================
# 2. Warm, adaptive emotional messages
# ==================================================
def generate_warm_message(score, fiber, sugar):
    if score >= 85: return "You’re taking amazing care of yourself today 🌱"
    if fiber < 20: return "Your body might enjoy a bit more fiber tomorrow — gentle progress 💛"
    if sugar > 50: return "Today had some sweetness — that’s okay. Balance comes with time 🍃"
    return "You showed up today, and that already matters 🤍"

def macro_targets(weight, calories):
    p_min = weight * 1.2
    f_min = (0.2 * calories) / 9
    c_min = (calories * 0.45) / 4
    return p_min

def health_score(stats, target_cal, pmin):
    score = 100
    if abs(stats["cal"] - target_cal) > 400: score -= 15
    if stats["pro"] < pmin: score -= 15
    if stats["fiber"] < 25: score -= 10
    if stats["sugar"] > 50: score -= 10
    score -= stats["processed_count"] * 5
    return max(0, score)

@app.route("/", methods=["GET", "POST"])
@app.route("/analyze", methods=["POST"]) # 增加此路由以匹配 HTML form action
def index():
    analysis = None
    error = None
    profile = {}

    if request.method == "POST":
        try:
            # 1. 获取并保存用户信息
            profile = {
                "age": int(request.form.get("age", 0)),
                "weight": float(request.form.get("weight", 0)),
                "height": float(request.form.get("height", 0)),
                "gender": request.form.get("gender"),
                "goal": request.form.get("goal")
            }

            if profile["height"] == 0 or profile["weight"] == 0:
                raise ValueError("Zero height or weight")

            # 2. 计算基础指标
            bmi = round(profile["weight"] / ((profile["height"]/100)**2), 1)
            bmr = 10*profile["weight"] + 6.25*profile["height"] - 5*profile["age"] + (5 if profile["gender"]=="male" else -161)
            tdee = int(bmr * 1.375)
            target_cal = tdee - 500 if profile["goal"]=="lose" else tdee + 300 if profile["goal"]=="gain" else tdee
            pmin = profile["weight"] * 1.2

            # 3. 解析食物
            stats = {"cal":0,"pro":0,"fat":0,"carb":0,"fiber":0,"sugar":0,"processed_count":0}
            meals = ["breakfast", "lunch", "dinner", "snacks"]
            
            for m in meals:
                raw = request.form.get(f"{m}_input", "").lower()
                if not raw: continue
                for item in raw.split(","):
                    if ":" not in item: continue
                    name, grams = item.split(":")
                    name = name.strip()
                    try:
                        g = float(grams)
                    except: g = 100.0
                    
                    if name in FOOD_DB:
                        f = FOOD_DB[name]
                        r = g / 100
                        stats["cal"] += f["cal"] * r
                        stats["pro"] += f["pro"] * r
                        stats["fat"] += f["fat"] * r
                        stats["carb"] += f["carb"] * r
                        stats["fiber"] += f.get("fiber", 0) * r
                        stats["sugar"] += f.get("sugar", 0) * r
                        if f.get("processed") == "yes": stats["processed_count"] += 1

            # 4. 封装分析数据 (与 HTML 变量名完全对应)
            score = health_score(stats, target_cal, pmin)
            percent = min(100, int((stats["cal"] / target_cal) * 100)) if target_cal > 0 else 0
            
            analysis = {
                "bmi": bmi,
                "target": target_cal,
                "total_cal": int(stats["cal"]),
                "pro": round(stats["pro"], 1),
                "fat": round(stats["fat"], 1),
                "carb": round(stats["carb"], 1),
                "fiber": round(stats["fiber"], 1),
                "sugar": round(stats["sugar"], 1),
                "percent": percent,
                "score": score,
                "warm": generate_warm_message(score, stats["fiber"], stats["sugar"])
            }

        except Exception as e:
            error = f"Oops! Please check your input format. (Error: {str(e)})"

    return render_template("index.html", analysis=analysis, error=error, profile=profile)

@app.route("/reset")
def reset():
    return render_template("index.html", analysis=None, error=None, profile={})

if __name__ == "__main__":
    app.run(debug=True)