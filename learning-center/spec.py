"""Learning Center: the 22 quiz ideas (V32-V53) as data. Run: python3 spec.py  ->  ideas.json, lines.json, jobs_img_*.json
Every item names its picture (images/<key>.jpg); new pictures are generated with Seedream 5.0 Flash in the V31 3D toy style
(gen_v31.py on the dev box), reused ones are copied from V31 and the planner samples. Voice: Cheeko (MiniMax English_PlayfulGirl).
Text rules: no em dashes, no ellipsis character, no curly quotes; no brands, flags or real songs."""
import json, os

# ---------- pictures ----------
REUSE = {   # key -> existing file
    'car': 'v31:01_car', 'bus': 'v31:02_bus', 'bicycle': 'v31:04_bicycle', 'motorbike': 'v31:05_motorbike', 'aeroplane': 'v31:06_aeroplane',
    'train': 'v31:07_train', 'boat': 'v31:08_boat', 'scooter': 'v31:10_scooter', 'fire_engine': 'v31:11_fire_engine', 'helicopter': 'v31:14_helicopter',
    'ship': 'v31:15_ship', 'tractor': 'v31:16_tractor', 'school_bus': 'v31:17_school_bus', 'hot_air_balloon': 'v31:20_hot_air_balloon',
    'rocket': 'v31:26_rocket', 'submarine': 'v31:27_submarine',
    'cow': 'lc:s01_cow', 'mango': 'lc:s02_mango', 'red_balloon': 'lc:s03_red_balloon', 'girl_nose': 'lc:s04_nose', 'elephant_pair': 'lc:s05_elephants',
    'ball': 'lc:s06_ball', 'rubber_duck': 'lc:s07_duck', 'lion': 'lc:s08_lion', 'clock': 'lc:s10_clock', 'doctor': 'lc:s11_doctor',
    'pressure_cooker': 'lc:s12_cooker', 'peacock': 'lc:s13_peacock', 'big_small': 'lc:s14_big_small', 'tabla': 'lc:s15_tabla', 'saturn': 'lc:s16_saturn',
    'umbrella_red': 'lc:s18_umbrella', 'taj_mahal': 'env:taj_mahal', 'sun': 'lc:s22_sun', 'pink_flower': 'lc:s22_flower',
}
NEW = {}    # key -> subject phrase (goes into the style prompt)
DEFAULTED = set()
def img(key, what=None):
    if key in REUSE: return key
    if key not in NEW or (what and key in DEFAULTED):    # a later, better description replaces a default one
        NEW[key] = what or key.replace('_', ' ')
        (DEFAULTED.discard if what else DEFAULTED.add)(key)
    return key

# ---------- voice lines ----------
LINES = {}  # idea id -> list of [speaker, emotion, text, gap, {}]
def line(vid, text, emo='happy'):
    L = LINES.setdefault(vid, [])
    for i, l in enumerate(L):
        if l[2] == text: return [vid, i]
    L.append(['cheeko', emo, text, 0, {}]); return [vid, len(L) - 1]

SHARED = 'LCX'
for t in ["Hi! I'm Cheeko!", "Ready? Let's go!", "Here's the first one!", "Here's the last one!", "How many did you get right?", "Bye bye!",
          "Level one!", "Level two!", "Level three!", "Can you guess this one?", "Do you know this one?", "Look closely!", "Make your guess!",
          "Try this one!", "Ooh, what's this?", "Ready for level two?", "Now try level three!", "Play again and beat your score!"]:
    line(SHARED, t, 'surprised' if t.startswith('Level') else 'happy')
S = lambda t: line(SHARED, t)

IDEAS = []
def idea(n, slug, title, t1, t2, head, mode, theme, music, rules, specific_prompts, done_line, levels, **kw):
    vid = f'V{31 + n}'
    d = dict(n=n, id=vid, slug=f'{n:02d}-{slug}', title=title, t1=t1, t2=t2, head=head, mode=mode, theme=theme, music=music,
             title_line=line(vid, f"Let's play {title}!"), rules_line=line(vid, rules), done_line=line(vid, done_line, 'surprised'),
             prompts=[line(vid, p) for p in specific_prompts] + [S(p) for p in ["Can you guess this one?", "Do you know this one?", "Look closely!",
                      "Make your guess!", "Try this one!", "Ooh, what's this?"]],
             levels=[], **kw)
    for lv in levels:
        items = []
        for it in lv['items']:
            it = dict(it)
            if 'say' in it: it['say_line'] = line(vid, it['say'], it.get('emo', 'happy'))
            if 'ask' in it: it['ask_line'] = line(vid, it['ask'])
            items.append(it)
        d['levels'].append({'answer': lv['answer'], 'items': items})
    IDEAS.append(d); return d

def simple(names, keyfmt=lambda n: n.lower().replace(' ', '_').replace('.', ''), whatfmt=None, say=lambda n: n + '!'):
    out = []
    for nm in names:
        k = keyfmt(nm); img(k, whatfmt(nm) if whatfmt else None)
        out.append({'label': nm, 'img': k, 'say': say(nm)})
    return out

# 1 Who Says That? (animal sounds; the sound files come from Envato after Ravi's yes)
A1 = ['Dog', 'Cat', 'Cow', 'Duck', 'Sheep', 'Horse', 'Pig', 'Rooster', 'Goat', 'Donkey']
A2 = ['Lion', 'Elephant', 'Monkey', 'Frog', 'Tiger', 'Bear', 'Wolf', 'Owl', 'Snake', 'Bee']
animal_what = {'Dog': 'friendly brown dog', 'Cat': 'cute orange cat', 'Duck': 'white duck with an orange beak, a real farm duck', 'Sheep': 'fluffy white sheep',
               'Horse': 'brown horse', 'Pig': 'pink pig', 'Rooster': 'colourful rooster', 'Goat': 'white goat with small horns', 'Donkey': 'grey donkey',
               'Elephant': 'grey elephant', 'Monkey': 'playful brown monkey', 'Frog': 'green frog', 'Tiger': 'Bengal tiger', 'Bear': 'brown bear',
               'Wolf': 'grey wolf', 'Owl': 'brown owl', 'Snake': 'friendly green snake, coiled', 'Bee': 'honey bee with yellow and black stripes'}
anim = lambda names: [{'label': a, 'img': img(a.lower(), animal_what.get(a)), 'say': a + '!', 'sound': a.lower()} for a in names]
idea(1, 'who-says-that', 'Who Says That', 'Who Says', 'That?', 'Who says <span>that</span>?', 'sound', 'farm', 'farm',
     "Listen to the sound, and say which animal it is!", ['Listen! Who is that?', 'Who makes this sound?'], 'You know so many animal sounds!',
     [{'answer': 3, 'items': anim(A1)}, {'answer': 4, 'items': anim(A2)}], needs_sound=True)

# 2 Guess the Fruit
F1 = ['Apple', 'Banana', 'Mango', 'Orange', 'Grapes', 'Watermelon', 'Strawberry', 'Pineapple', 'Papaya', 'Guava']
F2 = ['Pomegranate', 'Pear', 'Cherry', 'Coconut', 'Lemon', 'Kiwi', 'Chikoo', 'Jackfruit', 'Custard apple', 'Lychee']
F3 = ['Dragon fruit', 'Fig', 'Blueberry', 'Peach', 'Apricot', 'Avocado', 'Jamun', 'Star fruit', 'Plum', 'Muskmelon']
fruit_what = {'Apple': 'shiny red apple', 'Banana': 'bunch of three yellow bananas', 'Orange': 'round orange fruit (an orange) with a leaf', 'Grapes': 'bunch of purple grapes',
              'Watermelon': 'whole green striped watermelon with one red slice cut out', 'Strawberry': 'red strawberry', 'Pineapple': 'pineapple',
              'Papaya': 'papaya cut in half showing orange flesh and black seeds', 'Guava': 'green guava with one half cut showing pink flesh',
              'Pomegranate': 'pomegranate cut open showing red seeds', 'Pear': 'green pear', 'Cherry': 'pair of red cherries on a stem', 'Coconut': 'brown coconut with one half cracked open showing white inside',
              'Lemon': 'yellow lemon', 'Kiwi': 'kiwi fruit cut in half showing green flesh', 'Chikoo': 'brown chikoo (sapota) fruit with one cut in half',
              'Jackfruit': 'big green spiky jackfruit', 'Custard apple': 'green custard apple (sitaphal) with bumpy skin', 'Lychee': 'bunch of red lychees with one peeled',
              'Dragon fruit': 'pink dragon fruit cut in half showing white flesh with black seeds', 'Fig': 'purple fig cut in half', 'Blueberry': 'small heap of blueberries',
              'Peach': 'fuzzy peach', 'Apricot': 'orange apricot', 'Avocado': 'avocado cut in half with its seed', 'Jamun': 'small heap of dark purple jamun berries',
              'Star fruit': 'yellow star fruit with one star-shaped slice', 'Plum': 'dark red plum', 'Muskmelon': 'muskmelon (cantaloupe) cut open showing orange flesh'}
fr = lambda names: [{'label': f, 'img': img('fruit_' + f.lower().replace(' ', '_'), fruit_what.get(f, f.lower())), 'say': f + '!'} for f in names]
REUSE['fruit_mango'] = REUSE['mango']
idea(2, 'guess-the-fruit', 'Guess the Fruit', 'Guess the', 'Fruit!', 'Guess the <span>fruit</span>!', 'picture', 'garden', 'calypso',
     "Look at the picture, and say the fruit's name before the time runs out!", ['What fruit is this?', 'Which fruit is this?'], 'Yum! You know so many fruits!',
     [{'answer': 3, 'items': fr(F1)}, {'answer': 4, 'items': fr(F2)}, {'answer': 5, 'items': fr(F3)}])

# 3 What Colour Is It?
C1 = [('Red', 'red_balloon', None, 'The balloon is red.'), ('Yellow', 'fruit_banana', None, 'The banana is yellow.'), ('Blue', 'umbrella_blue', 'open blue umbrella', 'The umbrella is blue.'),
      ('Green', 'leaf_green', 'big green leaf', 'The leaf is green.'), ('Orange', 'pumpkin', 'orange pumpkin', 'The pumpkin is orange.'),
      ('Pink', 'pink_flower', None, 'The flower is pink.'), ('Purple', 'fruit_grapes', None, 'The grapes are purple.'), ('Brown', 'teddy_bear', 'brown teddy bear', 'The teddy bear is brown.'),
      ('Black', 'black_cat', 'black cat sitting', 'The cat is black.'), ('White', 'cloud', 'fluffy white cloud', 'The cloud is white.')]
C2 = [('Red', 'fire_engine', None, 'The fire engine is red.'), ('Yellow', 'school_bus', None, 'The school bus is yellow.'), ('Blue', 'blue_whale_toy', 'blue whale', 'The whale is blue.'),
      ('Green', 'frog', None, 'The frog is green.'), ('Orange', 'carrot', 'orange carrot with green leaves', 'The carrot is orange.'),
      ('Pink', 'piggy_bank', 'pink piggy bank', 'The piggy bank is pink.'), ('Purple', 'purple_butterfly', 'purple butterfly', 'The butterfly is purple.'),
      ('Brown', 'cookie', 'brown chocolate chip cookie', 'The cookie is brown.'), ('Black', 'black_boots', 'pair of black rain boots', 'The boots are black.'),
      ('White', 'milk_glass', 'glass of white milk', 'The milk is white.')]
col = lambda rows: [{'label': c, 'img': img(k, w), 'say': f'{c}! {why}'} for c, k, w, why in rows]
idea(3, 'what-colour', 'What Colour Is It', 'What Colour', 'Is It?', 'What <span>colour</span>?', 'picture', 'rainbow', 'musicbox',
     "Look at the picture, and say its colour!", ['What colour is this?', 'Which colour do you see?'], 'You know all your colours!',
     [{'answer': 3, 'items': col(C1)}, {'answer': 4, 'items': col(C2)}])

# 4 Touch Your Nose! (zoom rings are set in rings.json after the two pictures are made)
img('boy_full', 'cheerful little Indian boy standing and facing the viewer, full body from head to bare feet, arms a little away from his body with open hands, wearing a yellow t-shirt and blue shorts')
img('boy_face', 'face and shoulders of a cheerful little Indian boy looking at the viewer, close up, black hair')
B = [('Nose', 'boy_face'), ('Eyes', 'boy_face'), ('Ears', 'boy_face'), ('Mouth', 'boy_face'), ('Hair', 'boy_face'), ('Cheeks', 'boy_face'),
     ('Hands', 'boy_full'), ('Tummy', 'boy_full'), ('Knees', 'boy_full'), ('Feet', 'boy_full'), ('Shoulders', 'boy_full'), ('Toes', 'boy_full')]
idea(4, 'touch-your-nose', 'Touch Your Nose', 'Touch Your', 'Nose!', 'Touch and <span>say</span>!', 'zoom', 'playroom', 'claps',
     "Look where the circle is, touch it on your own body, and say its name!", ['What is this part called?', 'Touch it! What is it?'], 'You know your body so well!',
     [{'answer': 4, 'items': [{'label': p, 'img': k, 'say': f'{p}! Touch your {p.lower()}!', 'ring': p.lower()} for p, k in B]}])

# 5 Mummy and Baby (Ravi 2026-10-12: show the MUMMY alone, the child names the BABY; the reveal shows them together)
BM = [('Hen', 'Chick', 'grown-up mother hen standing alone, no chicks'), ('Dog', 'Puppy', 'grown-up mother dog standing alone, clearly an adult dog, no puppies'),
      ('Cat', 'Kitten', 'grown-up mother cat sitting alone, clearly an adult cat, no kittens'), ('Cow', 'Calf', 'grown-up mother cow standing alone, no calf'),
      ('Sheep', 'Lamb', 'grown-up mother sheep with thick wool standing alone, no lamb'), ('Horse', 'Foal', 'grown-up mother horse standing alone, no foal'),
      ('Duck', 'Duckling', 'grown-up mother duck standing alone, no ducklings'), ('Pig', 'Piglet', 'grown-up mother pig standing alone, no piglets'),
      ('Lioness', 'Cub', 'grown-up lioness (female lion with no mane) standing alone, no cubs'),
      ('Kangaroo', 'Joey', 'grown-up mother kangaroo standing alone, her pouch empty, no joey'),
      ('Frog', 'Tadpole', 'grown-up green frog sitting on a lily pad, alone, no tadpoles'), ('Elephant', 'Calf', 'grown-up mother elephant standing alone, no baby elephant')]
PAIR = {'Hen': img('mum_hen', 'mother hen with her yellow chick'), 'Dog': img('mum_dog', 'mother dog with her puppy'), 'Cat': img('mum_cat', 'mother cat with her kitten'),
        'Cow': img('mum_cow', 'mother cow with her calf'), 'Sheep': img('mum_sheep', 'mother sheep with her lamb'), 'Horse': img('mum_horse', 'mother horse with her foal'),
        'Duck': img('mum_duck', 'mother duck with her duckling'), 'Pig': img('mum_pig', 'mother pig with her piglet'), 'Lioness': img('mum_lion', 'lioness with her cub'),
        'Kangaroo': img('mum_kangaroo', 'mother kangaroo with a joey in her pouch'), 'Frog': img('mum_frog', 'green frog next to a tadpole in water'), 'Elephant': 'elephant_pair'}
bm = []
for m, b, wm in BM:
    art = 'An' if b[0] in 'AEIOU' else 'A'
    say = (f"{art} {b.lower()}! An elephant's baby is called a calf, just like a cow's." if m == 'Elephant'
           else f"{art} {b.lower()}! The {m.lower()}'s baby is {art.lower()} {b.lower()}.")
    bm.append({'label': b, 'sub': m, 'img': img('mummy_' + m.lower(), wm), 'img2': PAIR[m], 'say': say})
idea(5, 'mummy-and-baby', 'Mummy and Baby', 'Mummy and', 'Baby!', 'Who is my <span>baby</span>?', 'swap', 'meadow', 'lullaby',
     "Look at the mummy animal, and say the name of her baby!", ['Who is my baby?', 'What is my baby called?'], 'Every mummy found her baby!',
     [{'answer': 4, 'items': bm}])

# 6 A for Apple
LT = [('A', 'Apple', 'fruit_apple'), ('B', 'Ball', 'ball'), ('C', 'Cat', 'cat'), ('D', 'Dog', 'dog'), ('E', 'Elephant', 'elephant'), ('F', 'Fish', 'fish'),
      ('G', 'Grapes', 'fruit_grapes'), ('H', 'Hat', 'hat'), ('I', 'Ice cream', 'ice_cream'), ('J', 'Jug', 'jug'), ('K', 'Kite', 'kite'), ('L', 'Lion', 'lion'),
      ('M', 'Monkey', 'monkey'), ('N', 'Nest', 'nest'), ('O', 'Orange', 'fruit_orange'), ('P', 'Parrot', 'bird_parrot'), ('Q', 'Quilt', 'quilt'), ('R', 'Rabbit', 'rabbit'),
      ('S', 'Sun', 'sun'), ('T', 'Train', 'train'), ('U', 'Umbrella', 'umbrella_red'), ('V', 'Van', 'van'), ('W', 'Watermelon', 'fruit_watermelon'),
      ('X', 'Xylophone', 'inst_xylophone'), ('Y', 'Yo-yo', 'yoyo'), ('Z', 'Zebra', 'zebra')]
lw = {'fish': 'orange fish', 'hat': 'straw sun hat', 'ice_cream': 'ice cream cone with two scoops', 'jug': 'blue water jug', 'kite': 'colourful diamond-shaped kite with a tail',
      'nest': 'bird nest with three eggs', 'quilt': 'colourful patchwork quilt, folded', 'rabbit': 'white rabbit', 'van': 'small blue van', 'yoyo': 'red yo-yo with its string', 'zebra': 'zebra'}
lets = [{'label': f'{L} for {w}', 'letter': L, 'img': img(k, lw.get(k)), 'say': f'{L} for {w}!'} for L, w, k in LT]
idea(6, 'a-for-apple', 'A for Apple', 'A for', 'Apple!', 'What starts with <span>this</span>?', 'letter', 'chalk', 'piano',
     "Look at the letter and the picture, and say the word!", ['What starts with this letter?', 'Say the word!'], 'You know your A B C!',
     [{'answer': 3, 'items': lets[:9]}, {'answer': 4, 'items': lets[9:18]}, {'answer': 5, 'items': lets[18:]}])

# 7 How Many?
NUM = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']
CNT1 = [(3, 'rubber_duck', 'ducks'), (1, 'ball', 'ball'), (4, 'red_balloon', 'balloons'), (2, 'star', 'stars'), (5, 'fish', 'fish'),
        (2, 'fruit_apple', 'apples'), (4, 'pink_flower', 'flowers'), (1, 'sun', 'sun'), (5, 'car', 'cars'), (3, 'butterfly', 'butterflies')]
CNT2 = [(6, 'star', 'stars'), (8, 'rubber_duck', 'ducks'), (7, 'fruit_strawberry', 'strawberries'), (10, 'ball', 'balls'), (9, 'pink_flower', 'flowers'),
        (6, 'cupcake', 'cupcakes'), (7, 'fish', 'fish'), (8, 'red_balloon', 'balloons'), (10, 'butterfly', 'butterflies'), (9, 'fruit_apple', 'apples')]
cw = {'star': 'shiny yellow star', 'butterfly': 'orange and blue butterfly', 'cupcake': 'cupcake with pink icing'}
cnt = lambda rows: [{'label': f'{n} {w}', 'count': n, 'img': img(k, cw.get(k)), 'say': f'{NUM[n - 1]} {w}!'} for n, k, w in rows]
idea(7, 'how-many', 'How Many', 'How', 'Many?', 'How <span>many</span>?', 'count', 'counting', 'xylophone',
     "Count the things on the screen, and say how many!", ['How many can you count?', 'Count them with me!'], 'Super counting!',
     [{'answer': 4, 'items': cnt(CNT1)}, {'answer': 5, 'items': cnt(CNT2)}])

# 8 Shadow Match (reuses pictures; shadows are cut in code)
SH = [['Dog', 'dog'], ['Cat', 'cat'], ['Cow', 'cow'], ['Horse', 'horse'], ['Rooster', 'rooster'], ['Elephant', 'elephant'], ['Lion', 'lion'], ['Monkey', 'monkey'], ['Rabbit', 'rabbit'], ['Owl', 'owl']], \
     [['Car', 'car'], ['Bus', 'bus'], ['Bicycle', 'bicycle'], ['Aeroplane', 'aeroplane'], ['Helicopter', 'helicopter'], ['Tractor', 'tractor'], ['Train', 'train'], ['Rocket', 'rocket'], ['Boat', 'boat'], ['Hot air balloon', 'hot_air_balloon']], \
     [['Banana', 'fruit_banana'], ['Apple', 'fruit_apple'], ['Pineapple', 'fruit_pineapple'], ['Grapes', 'fruit_grapes'], ['Strawberry', 'fruit_strawberry'], ['Pear', 'fruit_pear'], ['Cherry', 'fruit_cherry'], ['Mango', 'fruit_mango'], ['Coconut', 'fruit_coconut'], ['Lemon', 'fruit_lemon']]
idea(8, 'shadow-match', 'Shadow Match', 'Shadow', 'Match!', 'Whose <span>shadow</span>?', 'shadow', 'night', 'mystery',
     "Look at the shadow, and guess what it is!", ['Whose shadow is this?', 'What is hiding in the shadow?'], 'You are a shadow detective!',
     [{'answer': a, 'items': [{'label': l, 'img': k, 'say': l + '!'} for l, k in lv]} for a, lv in zip((3, 4, 5), SH)])

# 9 How Does Cheeko Feel? (Cheeko faces are made from our fox art as the reference)
EM = [('Happy', 'happy, with a big smile', 'Happy! Cheeko got a big hug.'), ('Sad', 'sad, with droopy ears and one small tear', 'Sad. Cheeko dropped an ice cream.'),
      ('Angry', 'angry, frowning with puffed cheeks and arms crossed', 'Angry! Someone broke Cheeko\'s block tower.'), ('Scared', 'scared, ears back, hiding behind its paws', 'Scared! There was a loud thunder sound.'),
      ('Surprised', 'surprised, mouth open in an O and eyes wide', 'Surprised! A present for Cheeko!'), ('Sleepy', 'sleepy, yawning with half-closed eyes', 'Sleepy. It is time for bed.'),
      ('Silly', 'silly, sticking out its tongue and making a funny face', 'Silly! Cheeko is making funny faces.'), ('Proud', 'proud, standing tall with paws on its hips and a big smile', 'Proud! Cheeko built a tall tower all alone.')]
emos = [{'label': e, 'img': img('cheeko_' + e.lower(), f'CHEEKO:{w}'), 'say': s} for e, w, s in EM]
idea(9, 'how-does-cheeko-feel', 'How Does Cheeko Feel', 'How Does', 'Cheeko Feel?', 'How does Cheeko <span>feel</span>?', 'picture', 'pastel', 'ukulele',
     "Look at Cheeko's face, and say how Cheeko feels!", ['How does Cheeko feel?', 'What is Cheeko feeling?'], 'You understand feelings so well!',
     [{'answer': 4, 'items': emos}])

# 10 Shapes Around Us
SHP1 = [('Circle', 'clock', None, 'The clock is a circle.'), ('Square', 'gift_box', 'square gift box with a ribbon, seen from the front', 'The gift box is a square.'),
        ('Triangle', 'pizza_slice', 'slice of pizza', 'The pizza slice is a triangle.'), ('Rectangle', 'door', 'wooden door, seen from the front', 'The door is a rectangle.'),
        ('Oval', 'egg', 'white egg', 'The egg is an oval.'), ('Star', 'star', None, 'It is a star!'), ('Heart', 'heart_balloon', 'red heart-shaped balloon', 'The balloon is a heart.'),
        ('Diamond', 'kite', None, 'The kite is a diamond.'), ('Semicircle', 'watermelon_slice', 'half-moon slice of watermelon', 'The watermelon slice is a semicircle.'),
        ('Hexagon', 'honeycomb', 'single golden honeycomb cell shape, a hexagon of honey', 'The honeycomb is a hexagon.')]
SHP2 = [('Circle', 'plate', 'round white plate, seen from above', 'The plate is a circle.'), ('Square', 'cushion', 'square blue cushion, seen from the front', 'The cushion is a square.'),
        ('Triangle', 'samosa', 'samosa', 'The samosa is a triangle.'), ('Rectangle', 'book', 'closed book lying flat, seen from above', 'The book is a rectangle.'),
        ('Oval', 'mirror_oval', 'oval mirror with a wooden frame', 'The mirror is an oval.'), ('Star', 'starfish', 'orange starfish', 'The starfish is a star.'),
        ('Heart', 'heart_cookie', 'heart-shaped cookie', 'The cookie is a heart.'), ('Diamond', 'diamond_sign', 'yellow diamond-shaped road sign with no text', 'The sign is a diamond.'),
        ('Semicircle', 'rainbow', 'rainbow arc', 'The rainbow is a semicircle.'), ('Hexagon', 'hex_nut', 'metal hexagon nut', 'The nut is a hexagon.')]
shp = lambda rows: [{'label': s, 'shape': s.lower(), 'img': img(k, w), 'say': f'{"An" if s[0] in "AEIOU" else "A"} {s.lower()}! {why}'} for s, k, w, why in rows]
idea(10, 'shapes-around-us', 'Shapes Around Us', 'Shapes', 'Around Us!', 'What <span>shape</span>?', 'picture', 'shapes', 'synthpop',
     "Look at the picture, and say its shape!", ['What shape is this?', 'Which shape do you see?'], 'You found all the shapes!',
     [{'answer': 4, 'items': shp(SHP1)}, {'answer': 5, 'items': shp(SHP2)}])

# 11 Who Helps Us?
HP1 = [('Doctor', 'Doctors help us get better.'), ('Nurse', 'Nurses take care of us.'), ('Police officer', 'Police officers keep us safe.'), ('Firefighter', 'Firefighters put out fires.'),
       ('Teacher', 'Teachers help us learn.'), ('Farmer', 'Farmers grow our food.'), ('Chef', 'Chefs cook yummy food.'), ('Postman', 'Postmen bring our letters.'),
       ('Pilot', 'Pilots fly aeroplanes.'), ('Bus driver', 'Bus drivers take us places.')]
HP2 = [('Dentist', 'Dentists keep our teeth healthy.'), ('Mechanic', 'Mechanics fix cars.'), ('Carpenter', 'Carpenters make things from wood.'), ('Tailor', 'Tailors stitch our clothes.'),
       ('Barber', 'Barbers cut our hair.'), ('Painter', 'Painters paint our walls.'), ('Plumber', 'Plumbers fix our taps.'), ('Electrician', 'Electricians fix our lights.'),
       ('Astronaut', 'Astronauts go to space.'), ('Vegetable seller', 'Vegetable sellers bring us fresh vegetables.')]
hw = {'Nurse': 'friendly Indian nurse in a light blue uniform', 'Police officer': 'friendly Indian police officer in a khaki uniform and cap, no badges or text',
      'Firefighter': 'firefighter in a red helmet and fire suit holding a hose', 'Teacher': 'friendly Indian teacher holding a book in front of a blank green board',
      'Farmer': 'Indian farmer with a turban holding a basket of vegetables', 'Chef': 'chef in a white chef hat holding a ladle', 'Postman': 'Indian postman in a khaki uniform with a mail bag and letters',
      'Pilot': 'pilot in a dark uniform and cap', 'Bus driver': 'smiling Indian bus driver at the steering wheel', 'Dentist': 'dentist holding a big toothbrush, with a smiling tooth',
      'Mechanic': 'mechanic in blue overalls holding a spanner', 'Carpenter': 'carpenter holding a saw and a wooden plank', 'Tailor': 'Indian tailor with a measuring tape around the neck and a sewing machine',
      'Barber': 'barber holding scissors and a comb', 'Painter': 'house painter with a roller and a paint bucket', 'Plumber': 'plumber holding a pipe wrench next to a tap',
      'Electrician': 'electrician holding a light bulb and a screwdriver, wearing a helmet', 'Astronaut': 'astronaut in a white space suit with the helmet visor up, no flags or logos',
      'Vegetable seller': 'Indian vegetable seller with a cart full of vegetables'}
hp = lambda rows: [{'label': h, 'img': 'doctor' if h == 'Doctor' else img('helper_' + h.lower().replace(' ', '_'), hw[h] + ', full body'),
                     'say': f'{"An" if h[0] in "AEIOU" else "A"} {h.lower()}! {why}'} for h, why in rows]
idea(11, 'who-helps-us', 'Who Helps Us', 'Who Helps', 'Us?', 'Who <span>helps</span> us?', 'picture', 'city', 'march',
     "Look at the helper, and say what their job is!", ['Who is this helper?', 'What is this job called?'], 'Thank you, helpers!',
     [{'answer': 4, 'items': hp(HP1)}, {'answer': 5, 'items': hp(HP2)}])

# 12 Sounds Around the House (sound files: Envato and our own recordings, after Ravi's yes)
H1 = [('Doorbell', 'doorbell button next to a door', 'doorbell'), ('Pressure cooker', None, 'pressure_cooker'), ('Mixer', 'kitchen mixer grinder', 'mixer'),
      ('Tap water', 'kitchen tap with water running', 'tap'), ('Clock', None, 'clock'), ('Knock on the door', 'hand knocking on a wooden door', 'knock'),
      ('Alarm clock', 'red twin-bell alarm clock', 'alarm'), ('Kettle', 'steel kettle whistling with steam', 'kettle'), ('Broom', 'Indian broom sweeping the floor', 'broom'),
      ('Ceiling fan', 'white ceiling fan', 'fan')]
H2 = [('Washing machine', 'washing machine with clothes inside the round door', 'washer'), ('Keys', 'bunch of keys on a ring', 'keys'), ('Zip', 'zipper on a bag being opened', 'zip'),
      ('Scissors', 'pair of scissors cutting paper', 'scissors'), ('Brushing teeth', 'toothbrush with toothpaste next to a cup', 'brushing'), ('Rain', 'rain falling on a window', 'rain'),
      ('Sizzling dosa', 'dosa cooking on a hot tawa with a little steam', 'tawa'), ('Door creak', 'old wooden door opening a little', 'creak'), ('Car horn', 'small plain red car with a few curved sound lines coming from its front, a normal car with no face and no eyes', 'horn'),
      ('Footsteps', 'pair of sneakers walking', 'footsteps')]
hs = lambda rows: [{'label': l, 'img': k if k in ('pressure_cooker', 'clock') else img('house_' + k, w), 'say': l + '!', 'sound': 'house_' + k} for l, w, k in rows]
idea(12, 'sounds-around-the-house', 'Sounds Around the House', 'Sounds Around', 'the House!', 'What is that <span>sound</span>?', 'sound', 'home', 'soft',
     "Listen to the sound, and say what it is!", ['Listen! What is that sound?', 'Where have you heard this sound?'], 'Your ears are so clever!',
     [{'answer': 4, 'items': hs(H1)}, {'answer': 5, 'items': hs(H2)}], needs_sound=True)

# 13 Indian Birds
BD1 = ['Peacock', 'Parrot', 'Crow', 'Sparrow', 'Pigeon', 'Hen', 'Duck', 'Owl', 'Eagle', 'Kingfisher']
BD2 = ['Myna', 'Koel', 'Hornbill', 'Flamingo', 'Sarus crane', 'Woodpecker', 'Bulbul', 'Swan', 'Vulture', 'Weaver bird']
bw = {'Parrot': 'green Indian parrot with a red beak', 'Crow': 'black crow', 'Sparrow': 'house sparrow', 'Pigeon': 'grey pigeon', 'Hen': 'brown hen',
      'Kingfisher': 'blue and orange kingfisher on a branch', 'Eagle': 'eagle with spread wings', 'Myna': 'common myna bird, brown with a yellow beak and yellow eye patch',
      'Koel': 'Asian koel bird, glossy black with red eyes', 'Hornbill': 'great hornbill with a big yellow beak', 'Flamingo': 'pink flamingo standing on one leg',
      'Sarus crane': 'tall grey sarus crane with a red head', 'Woodpecker': 'woodpecker on a tree trunk', 'Bulbul': 'red-whiskered bulbul with a black crest',
      'Swan': 'white swan', 'Vulture': 'vulture sitting on a rock', 'Weaver bird': 'yellow weaver bird next to its hanging nest'}
bd = lambda names: [{'label': b, 'img': 'peacock' if b == 'Peacock' else ('owl' if b == 'Owl' else 'duck' if b == 'Duck' else img('bird_' + b.lower().replace(' ', '_'), bw.get(b, b.lower()))), 'say': b + '!'} for b in names]
idea(13, 'indian-birds', 'Indian Birds', 'Indian', 'Birds!', 'Guess the <span>bird</span>!', 'picture', 'sky', 'flute',
     "Look at the bird, and say its name!", ['Which bird is this?', 'What is this bird called?'], 'You are a bird expert!',
     [{'answer': 4, 'items': bd(BD1)}, {'answer': 5, 'items': bd(BD2)}])

# 14 Big or Small? (opposites)
OP = [('big_small', None, 'The elephant is big. And the mouse is?', 'Small! Big and small.', 'Big and small'),
      ('tall_short', 'tall giraffe standing next to a short penguin', 'The giraffe is tall. And the penguin is?', 'Short! Tall and short.', 'Tall and short'),
      ('hot_cold', 'steaming cup of hot tea next to a cold ice cream cone', 'The tea is hot. And the ice cream is?', 'Cold! Hot and cold.', 'Hot and cold'),
      ('fast_slow', 'fast rabbit running next to a slow tortoise', 'The rabbit is fast. And the tortoise is?', 'Slow! Fast and slow.', 'Fast and slow'),
      ('full_empty', 'glass full of milk next to an empty glass', 'This glass is full. And that glass is?', 'Empty! Full and empty.', 'Full and empty'),
      ('day_night', 'bright yellow sun on the left and a crescent moon with stars on the right', 'The sun comes out in the day. And the moon comes out at?', 'Night! Day and night.', 'Day and night'),
      ('open_closed', 'open gift box next to a closed gift box', 'This box is open. And that box is?', 'Closed! Open and closed.', 'Open and closed'),
      ('wet_dry', 'wet towel dripping water next to a dry folded towel', 'This towel is wet. And that towel is?', 'Dry! Wet and dry.', 'Wet and dry'),
      ('heavy_light', 'heavy grey stone next to a light white feather', 'The stone is heavy. And the feather is?', 'Light! Heavy and light.', 'Heavy and light'),
      ('long_short', 'long yellow pencil next to a short yellow pencil', 'This pencil is long. And that pencil is?', 'Short! Long and short.', 'Long and short'),
      ('clean_dirty', 'clean white plate next to a dirty plate with food on it', 'This plate is clean. And that plate is?', 'Dirty! Clean and dirty.', 'Clean and dirty'),
      ('thick_thin', 'thick book next to a thin book', 'This book is thick. And that book is?', 'Thin! Thick and thin.', 'Thick and thin')]
ops = [{'label': lab, 'img': img(k if k == 'big_small' else 'opp_' + k, w), 'ask': ask, 'say': say} for k, w, ask, say, lab in OP]
idea(14, 'big-or-small', 'Big or Small', 'Big or', 'Small?', 'Say the <span>opposite</span>!', 'ask', 'split', 'funky',
     "Listen to Cheeko, and say the opposite word!", ['Say the opposite!'], 'You know your opposites!',
     [{'answer': 4, 'items': ops}])

# 15 Guess the Instrument (sounds from Envato; veena and shehnai had no clean clips, so harmonica and cymbals took their place)
I1 = ['Drum', 'Piano', 'Guitar', 'Flute', 'Tabla', 'Bell', 'Xylophone', 'Trumpet', 'Violin', 'Harmonium']
I2 = ['Sitar', 'Dhol', 'Harmonica', 'Cymbals', 'Mridangam', 'Tambourine', 'Saxophone', 'Harp', 'Accordion', 'Triangle']
iw = {'Drum': 'red snare drum with two drumsticks', 'Piano': 'small black upright piano', 'Guitar': 'acoustic guitar', 'Flute': 'Indian bamboo flute (bansuri)',
      'Bell': 'golden hand bell', 'Xylophone': 'colourful xylophone with two mallets', 'Trumpet': 'golden trumpet', 'Violin': 'violin with its bow', 'Harmonium': 'Indian harmonium',
      'Sitar': 'sitar', 'Dhol': 'Indian dhol drum with two sticks', 'Harmonica': 'silver harmonica (mouth organ)', 'Cymbals': 'pair of shiny golden cymbals', 'Mridangam': 'mridangam drum',
      'Tambourine': 'tambourine', 'Saxophone': 'golden saxophone', 'Harp': 'golden harp', 'Accordion': 'red accordion', 'Triangle': 'metal triangle instrument with its beater'}
ins = lambda names: [{'label': x, 'img': 'tabla' if x == 'Tabla' else img('inst_' + x.lower(), iw.get(x)), 'say': x + '!', 'sound': 'inst_' + x.lower()} for x in names]
idea(15, 'guess-the-instrument', 'Guess the Instrument', 'Guess the', 'Instrument!', 'What is <span>playing</span>?', 'sound', 'notes', 'indian',
     "Listen to the music, and say which instrument is playing!", ['Listen! What is playing?', 'Which instrument is this?'], 'You have musical ears!',
     [{'answer': 4, 'items': ins(I1)}, {'answer': 5, 'items': ins(I2)}], needs_sound=True)

# 16 Space Quiz: Sun, Moon and Planets (a picture and one clue)
SP = [('Sun', 'the Sun, a glowing yellow and orange star', 'I am a big hot star. I give light to all the planets.'),
      ('Mercury', 'planet Mercury, small and grey with craters', 'I am the smallest planet, and the closest to the Sun.'),
      ('Venus', 'planet Venus, pale yellow with swirly clouds', 'I am the hottest planet. I shine bright in the evening sky.'),
      ('Earth', 'planet Earth with blue oceans, green land and white clouds', 'I am blue and green. I am our home!'),
      ('Moon', 'the Moon, grey with craters', 'I go around the Earth. You see me at night.'),
      ('Mars', 'planet Mars, red and dusty', 'I am red and dusty. People call me the red planet.'),
      ('Jupiter', 'planet Jupiter with orange and white stripes and a big red spot', 'I am the biggest planet. I have a big red spot.'),
      ('Saturn', None, 'I have big shiny rings around me.'),
      ('Uranus', 'planet Uranus, pale blue-green with thin rings, tilted on its side', 'I am a cold blue green planet. I spin on my side.'),
      ('Neptune', 'planet Neptune, deep blue', 'I am dark blue and very windy. I am the farthest planet from the Sun.')]
sp = [{'label': nm, 'img': 'saturn' if nm == 'Saturn' else img('space_' + nm.lower(), w + ', floating in space with a few small stars on a dark blue background instead of sky blue'),
       'ask': clue, 'say': f'{"The " if nm in ("Sun", "Moon") else ""}{nm}!'} for nm, w, clue in SP]
idea(16, 'space-quiz', 'Space Quiz', 'Space', 'Quiz!', 'What am <span>I</span>?', 'ask', 'space', 'space',
     "Listen to Cheeko's clue, and say what it is!", ['What am I?'], 'You are a space explorer!',
     [{'answer': 5, 'items': sp}])

# 17 Odd One Out (reuses pictures)
OD = [(['car', 'bus', 'train', 'fruit_mango'], 3, 'Mango', 'The mango! It is a fruit, not a vehicle.'),
      (['cow', 'dog', 'cat', 'bicycle'], 3, 'Bicycle', 'The bicycle! It is not an animal.'),
      (['fruit_apple', 'fruit_banana', 'fruit_grapes', 'ball'], 3, 'Ball', 'The ball! You cannot eat it.'),
      (['aeroplane', 'helicopter', 'hot_air_balloon', 'boat'], 3, 'Boat', 'The boat! It cannot fly.'),
      (['bird_parrot', 'bird_crow', 'duck', 'dog'], 3, 'Dog', 'The dog! It is not a bird.'),
      (['red_balloon', 'fruit_strawberry', 'fire_engine', 'bus'], 3, 'Bus', 'The bus! It is blue. The others are red.'),
      (['doctor', 'helper_teacher', 'helper_chef', 'elephant'], 3, 'Elephant', 'The elephant! It is not a helper.'),
      (['clock', 'ball', 'plate', 'gift_box'], 3, 'Gift box', 'The gift box! It is a square. The others are round.'),
      (['lion', 'tiger', 'monkey', 'tractor'], 3, 'Tractor', 'The tractor! It is not an animal.'),
      (['sun', 'space_moon', 'star', 'fish'], 3, 'Fish', 'The fish! It is not in the sky.')]
OD2 = [(['boat', 'ship', 'submarine', 'aeroplane'], 3, 'Aeroplane', 'The aeroplane! It does not go on water.'),
       (['bicycle', 'motorbike', 'scooter', 'car'], 3, 'Car', 'The car! It has four wheels. The others have two.'),
       (['fruit_strawberry', 'fruit_cherry', 'fruit_apple', 'fruit_banana'], 3, 'Banana', 'The banana! It is yellow. The others are red.'),
       (['frog', 'fish', 'duck', 'cow'], 3, 'Cow', 'The cow! It does not swim in water.'),
       (['tabla', 'inst_drum', 'inst_dhol', 'inst_flute'], 3, 'Flute', 'The flute! It is not a drum.'),
       (['t_rex', 'dino_triceratops', 'dino_stegosaurus', 'elephant'], 3, 'Elephant', 'The elephant! It is not a dinosaur.'),
       (['bee', 'butterfly', 'bird_sparrow', 'snake'], 3, 'Snake', 'The snake! It cannot fly.'),
       (['pizza_slice', 'samosa', 'kite', 'egg'], 2, 'Kite', 'The kite! You cannot eat it.'),
       (['sun', 'opp_hot_cold', 'pressure_cooker', 'house_fan'], 3, 'Ceiling fan', 'The fan! It keeps us cool. The others are hot.'),
       (['fruit_lemon', 'fruit_banana', 'sun', 'fruit_grapes'], 3, 'Grapes', 'The grapes! They are purple. The others are yellow.')]
odd = lambda rows: [{'label': lab, 'imgs': ims, 'odd': o, 'img': ims[o], 'say': s} for ims, o, lab, s in rows]
idea(17, 'odd-one-out', 'Odd One Out', 'Odd One', 'Out!', 'Which one is <span>different</span>?', 'odd', 'puzzle', 'quirky',
     "Look at the four pictures, and find the one that is different!", ['Which one is different?', 'Find the odd one out!'], 'Great thinking!',
     [{'answer': 5, 'items': odd(OD)}, {'answer': 6, 'items': odd(OD2)}])

# 18 Cheeko's Riddles
RD = [('Umbrella', 'umbrella_red', 'I open up when it rains. I keep you dry. What am I?', 'An umbrella!'),
      ('Clock', 'clock', 'I have a face and two hands, but no arms or legs. I tell you the time. What am I?', 'A clock!'),
      ('Sun', 'sun', 'I am big, yellow and hot. I come up in the sky every morning. What am I?', 'The sun!'),
      ('Moon', 'space_moon', 'I come out at night. Sometimes I am round, sometimes I am thin. What am I?', 'The moon!'),
      ('Cow', 'cow', 'I say moo. I eat grass. I give you milk. Who am I?', 'A cow!'),
      ('Elephant', 'elephant', 'I am very big and grey. I have a long trunk. Who am I?', 'An elephant!'),
      ('Banana', 'fruit_banana', 'I am long and yellow. Monkeys love me. You peel me before you eat me. What am I?', 'A banana!'),
      ('Ice cream', 'ice_cream', 'I am cold and sweet. I melt in the sun. What am I?', 'An ice cream!'),
      ('Fish', 'fish', 'I live in water. I have fins and a tail. I swim but I cannot walk. Who am I?', 'A fish!'),
      ('Rainbow', 'rainbow', 'I come after the rain. I have seven colours. I bend across the sky. What am I?', 'A rainbow!'),
      ('Egg', 'egg', 'I am white and oval. A little chick comes out of me. What am I?', 'An egg!'),
      ('Kite', 'kite', 'I fly high in the sky, but I have no wings. You hold my string. What am I?', 'A kite!'),
      ('Tree', 'tree', 'I am tall and green. Birds make nests in me. I give you shade. What am I?', 'A tree!'),
      ('Toothbrush', 'toothbrush', 'I help you clean your teeth every morning and every night. What am I?', 'A toothbrush!'),
      ('Pillow', 'pillow', 'I am soft. You put your head on me when you sleep. What am I?', 'A pillow!'),
      ('Shoes', 'shoes', 'You wear us on your feet. We always come in a pair. What are we?', 'Shoes!'),
      ('Bee', 'bee', 'I am small and I buzz. I make sweet honey. Who am I?', 'A bee!'),
      ('Spider', 'spider', 'I have eight legs. I make a sticky web. Who am I?', 'A spider!'),
      ('Mirror', 'mirror_oval', 'When you look at me, you see yourself. What am I?', 'A mirror!'),
      ('Pencil', 'pencil', 'I help you write and draw. I get shorter when you sharpen me. What am I?', 'A pencil!')]
rw = {'tree': 'big green tree', 'toothbrush': 'blue toothbrush with white toothpaste', 'pillow': 'soft white pillow', 'shoes': 'pair of red sneakers',
      'spider': 'friendly cartoon spider on its web', 'pencil': 'yellow pencil with a pink eraser'}
rid = [{'label': lab, 'img': img(k, rw.get(k)), 'ask': ask, 'say': ans} for lab, k, ask, ans in RD]
idea(18, 'cheekos-riddles', "Cheeko's Riddles", "Cheeko's", 'Riddles!', "Cheeko's <span>riddle</span>", 'riddle', 'question', 'mystery2',
     "Listen to Cheeko's riddle, and guess the answer!", ['Guess my riddle!'], 'You solved my riddles!',
     [{'answer': 5, 'items': rid[:10]}, {'answer': 6, 'items': rid[10:]}])

# 19 Guess the Dinosaur
D1 = ['T. rex', 'Triceratops', 'Stegosaurus', 'Brachiosaurus', 'Velociraptor', 'Ankylosaurus', 'Spinosaurus', 'Diplodocus', 'Parasaurolophus', 'Iguanodon']
D2 = ['Pachycephalosaurus', 'Allosaurus', 'Dilophosaurus', 'Carnotaurus', 'Therizinosaurus', 'Gallimimus', 'Baryonyx', 'Oviraptor', 'Argentinosaurus', 'Maiasaura']
dw = {'Triceratops': 'Triceratops with three horns and a big frill', 'Stegosaurus': 'Stegosaurus with plates on its back and a spiky tail', 'Brachiosaurus': 'Brachiosaurus with a very long neck',
      'Velociraptor': 'Velociraptor with feathers', 'Ankylosaurus': 'Ankylosaurus with armour and a club tail', 'Spinosaurus': 'Spinosaurus with a tall sail on its back',
      'Diplodocus': 'Diplodocus with a long neck and a very long tail', 'Parasaurolophus': 'Parasaurolophus with a long curved crest on its head', 'Iguanodon': 'Iguanodon with thumb spikes',
      'Pachycephalosaurus': 'Pachycephalosaurus with a thick dome head', 'Allosaurus': 'Allosaurus, a big meat-eating dinosaur with small horns above the eyes',
      'Dilophosaurus': 'Dilophosaurus with two crests on its head', 'Carnotaurus': 'Carnotaurus with two horns and tiny arms', 'Therizinosaurus': 'Therizinosaurus with very long claws',
      'Gallimimus': 'Gallimimus, a fast ostrich-like dinosaur', 'Baryonyx': 'Baryonyx with a long crocodile-like snout and big thumb claws', 'Oviraptor': 'Oviraptor with a crest, next to its eggs',
      'Argentinosaurus': 'Argentinosaurus, a giant long-necked dinosaur', 'Maiasaura': 'Maiasaura mother dinosaur next to its nest of eggs'}
dn = lambda names: [{'label': x, 'img': img('t_rex', 'friendly T. rex dinosaur with brown and orange skin, big head, small arms, side view, a plain dinosaur toy, not green') if x == 'T. rex' else img('dino_' + x.lower(), 'friendly ' + dw.get(x, x) + ' dinosaur, side view'), 'say': x + '!'} for x in names]
idea(19, 'guess-the-dinosaur', 'Guess the Dinosaur', 'Guess the', 'Dinosaur!', 'Guess the <span>dinosaur</span>!', 'picture', 'jungle', 'jungle',
     "Look at the dinosaur, and say its name!", ['Which dinosaur is this?', 'Do you know this dinosaur?'], 'Roar! You are a dinosaur expert!',
     [{'answer': 4, 'items': dn(D1)}, {'answer': 5, 'items': dn(D2)}])

# 20 Famous Places of India (real photos from Envato, photos/raw/; Ravi 2026-10-09: places as photos, no flags in frame)
P1 = ['Taj Mahal', 'India Gate', 'Qutub Minar', 'Gateway of India', 'Red Fort', 'Hawa Mahal', 'Mysore Palace', 'Victoria Memorial', 'Lotus Temple', 'Golden Temple']
P2 = ['Howrah Bridge', 'Jantar Mantar', 'Amber Fort', 'Hampi Stone Chariot', 'Bandra Worli Sea Link', 'Shore Temple', 'Meenakshi Temple', 'Sanchi Stupa', 'Mehrangarh Fort', 'Konark Sun Temple']
pkey = lambda x: 'taj_mahal' if x == 'Taj Mahal' else 'place_' + x.lower().replace(' ', '_')
for x in P1 + P2: REUSE.setdefault(pkey(x), 'env:' + pkey(x))
pl = lambda names: [{'label': x, 'img': pkey(x),
                     'say': ('The ' if x not in ('Hampi Stone Chariot', 'Bandra Worli Sea Link', 'Amber Fort', 'Mysore Palace', 'Mehrangarh Fort') else '') + x + '!'} for x in names]
idea(20, 'famous-places-of-india', 'Famous Places of India', 'Famous Places', 'of India!', 'Where is <span>this</span>?', 'picture', 'postcard', 'travel',
     "Look at the famous place, and say its name!", ['Which place is this?', 'Have you seen this place?'], 'You know India so well!',
     [{'answer': 4, 'items': pl(P1)}, {'answer': 5, 'items': pl(P2)}])

# 21 What Is Missing? (reuses pictures)
MS = [(['car', 'bus', 'train', 'boat'], 1, 'Bus', 'The bus!'), (['fruit_apple', 'fruit_banana', 'fruit_mango', 'fruit_grapes'], 2, 'Mango', 'The mango!'),
      (['cow', 'dog', 'cat', 'duck'], 3, 'Duck', 'The duck!'), (['ball', 'red_balloon', 'rubber_duck', 'umbrella_red'], 0, 'Ball', 'The ball!'),
      (['sun', 'pink_flower', 'star', 'butterfly'], 1, 'Flower', 'The flower!'), (['clock', 'gift_box', 'kite', 'egg'], 2, 'Kite', 'The kite!'),
      (['doctor', 'helper_chef', 'helper_teacher', 'helper_farmer'], 3, 'Farmer', 'The farmer!'), (['tabla', 'inst_drum', 'inst_flute', 'inst_bell'], 2, 'Flute', 'The flute!'),
      (['lion', 'monkey', 'elephant', 'tiger'], 0, 'Lion', 'The lion!'), (['rocket', 'aeroplane', 'helicopter', 'hot_air_balloon'], 3, 'Hot air balloon', 'The hot air balloon!')]
idea(21, 'what-is-missing', 'What Is Missing', 'What Is', 'Missing?', 'What is <span>missing</span>?', 'missing', 'cards', 'ticktock',
     "Look at the four pictures and remember them. Then say which one went away!", ['Remember these four!'], 'Your memory is amazing!',
     [{'answer': 5, 'items': [{'label': lab, 'imgs': ims, 'odd': o, 'img': ims[o], 'say': s} for ims, o, lab, s in MS]}],
     after_line=line('V52', 'What is missing?'))

# 22 Emoji Words (our own icons)
EW = [('sun', 'pink_flower', 'Sunflower'), ('rain_cloud', 'ribbon_bow', 'Rainbow'), ('star', 'fish', 'Starfish'), ('butter', 'housefly', 'Butterfly'),
      ('foot', 'ball', 'Football'), ('teacup', 'birthday_cake', 'Cupcake'), ('snowflake', 'man', 'Snowman'), ('tooth', 'paintbrush', 'Toothbrush'),
      ('frying_pan', 'birthday_cake', 'Pancake'), ('sea_waves', 'horse', 'Seahorse'), ('jelly', 'fish', 'Jellyfish'), ('rain_cloud', 'winter_coat', 'Raincoat')]
ewh = {'rain_cloud': 'small grey cloud with raindrops', 'ribbon_bow': 'pink ribbon bow', 'butter': 'block of yellow butter on a small plate', 'housefly': 'cute cartoon housefly',
       'foot': 'cartoon bare foot', 'teacup': 'white teacup', 'birthday_cake': 'birthday cake with candles', 'snowflake': 'white snowflake', 'man': 'cheerful cartoon man waving',
       'tooth': 'smiling white tooth', 'paintbrush': 'paintbrush with blue paint', 'frying_pan': 'black frying pan', 'sea_waves': 'blue sea waves', 'jelly': 'wobbly red jelly dessert',
       'winter_coat': 'red winter coat'}
ew = [{'label': w, 'imgs': [img(a, ewh.get(a)), img(b, ewh.get(b))], 'img': a, 'say': f'{w}!'} for a, b, w in EW]
idea(22, 'emoji-words', 'Emoji Words', 'Emoji', 'Words!', 'Two pictures, one <span>word</span>!', 'pair', 'stickers', 'happysynth',
     "Look at the two pictures, put them together, and say the word!", ['What word do they make?', 'Put them together!'], 'You are a word wizard!',
     [{'answer': 5, 'items': ew}])

for k in ['bird_crow', 'bird_sparrow', 'helper_teacher', 'helper_chef', 'helper_farmer', 'inst_drum', 'inst_dhol', 'inst_flute', 'inst_bell', 'dino_triceratops',
          'dino_stegosaurus', 'house_fan', 'space_moon', 'opp_hot_cold', 'fruit_cherry', 'fruit_lemon', 'fruit_pineapple', 'fruit_pear', 'fruit_coconut']:
    assert k in NEW or k in REUSE, k

# ---------- write ----------
STYLE = ('A cute 3D rendered {what} for a children\'s picture book, smooth glossy rounded shapes, the whole subject visible, centred with space around it, '
         'on a plain soft sky-blue background with a gentle shadow under it. No text, no letters, no numbers, no logos, no flags, no brand names.')
REF_STYLE = ' Use the reference image only for its style: the same 3D toy render look, soft lighting and plain sky-blue background. Do not copy the car.'
CHEEKO = ('This exact fox character from the reference image (same face, same orange fur, same bandana), now {what}. Keep the same 3D look. '
          'Plain soft sky-blue background, the character centred, upper body visible. No text.')
jobs = []
for k, what in NEW.items():
    if what.startswith('CHEEKO:'):
        jobs.append({'tag': 'lc_' + k, 'model': 'dola-seedream-5-0-flash-260915', 'prompt': CHEEKO.format(what=what[7:]), 'ref': '/root/tts-compare/out/v31/cheeko_hero.png'})
    else:
        jobs.append({'tag': 'lc_' + k, 'model': 'dola-seedream-5-0-flash-260915', 'prompt': STYLE.format(what=what) + REF_STYLE,
                     'ref': '/root/tts-compare/out/v31/test2_car_toy_seedflash.jpg'})
for i in range(4):
    json.dump(jobs[i::4], open(f'jobs_img_{i}.json', 'w'), indent=1)
voices = json.load(open('/Users/ravikumar/Cheeko Master/marketing/tools/feature_lines.json'))['voices']
json.dump({'voices': voices, **{k: {'lines': v} for k, v in LINES.items()}}, open('lines.json', 'w'), indent=1, ensure_ascii=False)
json.dump({'reuse': REUSE, 'new': NEW, 'ideas': IDEAS}, open('ideas.json', 'w'), indent=1, ensure_ascii=False)
print(len(IDEAS), 'ideas;', len(NEW), 'new pictures;', len(REUSE), 'reused;', sum(len(v) for v in LINES.values()), 'voice lines;',
      sum(len(lv['items']) for d in IDEAS for lv in d['levels']), 'rounds;', sum(len(d['levels']) for d in IDEAS), 'videos')
for t in [l[2] for v in LINES.values() for l in v]:
    assert '...' not in t and '—' not in t and '…' not in t and '“' not in t and '’' not in t, t
