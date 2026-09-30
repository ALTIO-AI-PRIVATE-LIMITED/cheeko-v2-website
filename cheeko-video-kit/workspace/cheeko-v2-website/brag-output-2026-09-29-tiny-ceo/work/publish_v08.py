"""Use the established publisher for V08 only; preserve every other Drive deliverable."""
import importlib.util, shutil
from pathlib import Path
TOOLS=Path('/Users/ravikumar/Cheeko Master/marketing/tools')
spec=importlib.util.spec_from_file_location('publisher',TOOLS/'publish_to_drive.py'); P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
v=next(x for x in P.VIDEOS if x[0]=='V08'); row=P.build(v,P.DRIVE)
vid,title,fmt,secs,status,voice,stem=row
src=P.REPO/v[3];base=P.DRIVE/f'{vid} {title}'; ready=P.DRIVE/'Ready to post/English'/f'{vid} {title}';ready.mkdir(parents=True,exist_ok=True)
for source,label in [('brag.mp4','video.mp4'),('thumbnail.jpg','thumbnail.jpg'),('share-copy.txt','caption.txt')]:shutil.copy2(src/source,ready/f'{vid} {title} - {label}')
shutil.copytree(src/'work/assets',base/'5 Source/assets',dirs_exist_ok=True)
shutil.copytree(src/'work/vo',base/'5 Source/vo',dirs_exist_ok=True)
for name in ['timeline.js','voice-lines.json','qa.mjs','voice-verification.log','publish_v08.py','art-prompt.txt']:
 shutil.copy2(src/'work'/name,base/'5 Source'/name)
shutil.copy2(src/'TECHNICAL.md',base/'TECHNICAL.md')
shutil.copy2(src/'script.md',base/'1 Script/script.md')
for phase in ['settled','transition']:shutil.copy2(src/f'work/qa/{phase}-sheet.jpg',base/f'3 Test/{phase}-sheet.jpg')
plan=P.DRIVE/'00 Plan';tracker=plan/'Video tracker.md';s=tracker.read_text();line=f'| {vid} | {title} | {fmt} | {secs}s | {status} | {voice} | {stem}.mp4 |'
if '| V08 |' in s:s='\n'.join(line if x.startswith('| V08 |') else x for x in s.splitlines())+'\n'
else:s=s.replace('\nArchive:', '\n'+line+'\n\nArchive:')
tracker.write_text(s)
shutil.copy2(P.MKT/'cheeko-video-ideas.md',plan/'Cheeko video ideas (all 28).md')
print('Saved Drive-sync draft:',base)
print('Saved posting package:',ready)
