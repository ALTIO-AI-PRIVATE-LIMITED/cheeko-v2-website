"""Write the lyric + arrangement files for ElevenLabs Music (v2 arrangement after Ravi's feedback 2026-10-10: shorter Hindi lines,
more music: instrumental intro, a mid-song instrumental break and an instrumental ending, voice soft inside the music).
All lyrics are original, written for Cheeko. Hindi needs a native speaker check before release.
Usage: /usr/bin/python3 build_songs.py  ->  song1_v2.json, song2_everyone_home.json, song3_soft_rain.json"""
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
MUSIC = ['instruments prominent in the mix', 'vocals soft and blended into the music, not upfront', 'long instrumental passages']
EN_STYLE = ['gentle lullaby', 'soft warm female vocal, intimate', 'music box, harp and soft strings', 'slow rocking 3/4 waltz feel',
            'about 64 bpm', 'very quiet and calm', 'simple melody with falling phrases'] + MUSIC
HI_STYLE = ['gentle Indian lori lullaby', 'soft warm Indian female vocal singing in Hindi', 'short sung phrases with long held notes and pauses',
            'harp, music box and soft bansuri with a tanpura drone', 'slow rocking 6/8 feel', 'about 64 bpm', 'very quiet and calm'] + MUSIC
NEG_EN = ['drums', 'percussion', 'electric guitar', 'loud', 'auto-tune', 'belting', 'choir', 'fast singing']
NEG_HI = ['drums', 'tabla', 'percussion', 'electric guitar', 'loud', 'auto-tune', 'belting', 'Bollywood film orchestra', 'choir', 'fast singing', 'long wordy lines']
def song(refrain, v1, v2, style, neg, inst_lang):
    I = lambda what: [f'{{instrumental only, {what}, no vocals}}']
    return {'styles': style, 'negative': neg, 'sections': [
        {'name': 'Intro', 'ms': 12000, 'lines': I(inst_lang + ' play the melody softly')},
        {'name': 'Refrain', 'ms': 20000, 'lines': refrain},
        {'name': 'Verse 1', 'ms': 20000, 'lines': v1},
        {'name': 'Interlude', 'ms': 16000, 'lines': I(inst_lang + ' play the refrain melody')},
        {'name': 'Verse 2', 'ms': 20000, 'lines': v2},
        {'name': 'Refrain', 'ms': 20000, 'lines': refrain},
        {'name': 'Outro', 'ms': 18000, 'lines': ['{instruments carry the melody, very soft humming, slowing down and fading out}', 'Mmm.']}]}
EN_INST, HI_INST = 'music box and harp', 'bansuri, harp and music box'
SONGS = {
 'song1_v2': ('The Moon Keeps Watch / Chaand Jaage (v2, more music, short Hindi)',
   (['The moon is in the sky,', 'the stars are winking slow.', 'Rest now, little one,', 'the night is soft and low.'],
    ['The trees have gone to sleep,', 'the lamps are glowing gold,', 'your blanket keeps you warm,', 'your hand is mine to hold.'],
    ['The wind is humming low,', 'the clouds are drifting by,', 'the moon will stay awake', 'and hum a lullaby.']),
   (['सो जा रे,', 'चाँद जागे,', 'तारे गाएँ,', 'आ आ आ।'],
    ['पेड़ सोए,', 'दीप मद्धम,', 'नरम रज़ाई,', 'सपने आएँ।'],
    ['हवा गाए,', 'बादल जाएँ,', 'चाँद जागे,', 'लोरी गाए।'])),
 'song2_everyone_home': ('Everyone Is Home / Sab Ghar Aaye',
   (['Little moon is shining,', 'little stars are near.', 'Everyone is home now,', 'everyone is here.'],
    ['The bird is in her nest,', 'the calf is by the cow,', 'the fish is in the pond,', 'and you are sleepy now.'],
    ['The bee is in the hive,', 'the lamb is with the sheep,', 'the moon is in the sky,', 'and you are fast asleep.']),
   (['सब घर आए,', 'चाँद मुस्काए,', 'तारे पास,', 'आ आ आ।'],
    ['चिड़िया घोंसले में,', 'बछड़ा माँ के पास,', 'मछली ताल में,', 'तू मेरे पास।'],
    ['मधुमक्खी छत्ते में,', 'मेमना भेड़ के पास,', 'चाँद आसमान में,', 'नींद तेरे पास।'])),
 'song3_soft_rain': ('Soft Rain / Dheemi Baarish',
   (['Soft rain, falling slow,', 'river humming low.', 'Close your eyes, my love,', 'off to dreams you go.'],
    ['The frogs have said goodnight,', 'the boats are tied up tight,', 'the window wears the rain', 'like ribbons, soft and light.'],
    ['The puddles hold the moon,', 'the crickets hum a tune,', 'the morning will be bright,', 'and I will see you soon.']),
   (['धीमी बारिश,', 'नदिया गाए,', 'आँखें मूँदो,', 'नींद आए।'],
    ['मेंढक सोए,', 'नाव किनारे,', 'खिड़की पे बूँदें,', 'चमकें तारे।'],
    ['पानी में चाँद,', 'झींगुर गाए,', 'कल फिर सुबह,', 'धूप मुस्काए।'])),
}
for key, (title, en, hi) in SONGS.items():
    json.dump({'title': title, 'note': 'Original lyrics written for Cheeko. Not based on any existing song. Hindi needs a native speaker check.',
               'en': song(*en, EN_STYLE, NEG_EN, EN_INST), 'hi': song(*hi, HI_STYLE, NEG_HI, HI_INST)},
              open(f'{key}.json', 'w'), indent=1, ensure_ascii=False)
    print(key, sum(s['ms'] for s in song(*en, EN_STYLE, NEG_EN, EN_INST)['sections']) / 1000, 's')
