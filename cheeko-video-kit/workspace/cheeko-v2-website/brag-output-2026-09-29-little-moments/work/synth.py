"""Original D-major 120 BPM mallet-pop score, quiet matched-key effects and voice ducking."""
import json, wave
import numpy as np
from pathlib import Path
SR=44100
J=json.loads(Path('warp.json').read_text()); DUR=J['dur']; N=round(DUR*SR)
rng=np.random.default_rng(707)
M=np.zeros(N); FX=np.zeros(N)
def hz(n):return 440*2**((n-69)/12)
def place(dst,x,t,g=1):
 a=round(t*SR);b=min(N,a+len(x))
 if a>=0 and b>a:dst[a:b]+=x[:b-a]*g
def mallet(note,d=.36):
 t=np.arange(round(d*SR))/SR;f=hz(note)
 return (np.sin(2*np.pi*f*t)*np.exp(-t*11)+.18*np.sin(2*np.pi*2*f*t)*np.exp(-t*22))*np.minimum(t/.005,1)*np.minimum((d-t)/.025,1)
def bass(note):
 t=np.arange(round(.42*SR))/SR;f=hz(note)
 return (np.sin(2*np.pi*f*t)+.12*np.sin(4*np.pi*f*t))*np.minimum(t/.012,1)*np.exp(-t*7)
def kick():
 t=np.arange(round(.16*SR))/SR
 return np.sin(2*np.pi*(48*t+50*.016*(1-np.exp(-t/.016))))*np.exp(-t*27)*np.minimum(t/.003,1)
def hat():
 t=np.arange(round(.045*SR))/SR;n=rng.normal(0,.4,len(t));return np.diff(np.r_[0,n])*np.exp(-t*95)*.3
chords=[(50,[62,66,69,74]),(45,[61,64,69,73]),(47,[62,66,71,74]),(43,[62,67,71,74])]
for beat in range(int(DUR/.5)+1):
 t=beat*.5;root,notes=chords[(beat//4)%4]
 place(M,bass(root),t,.09)
 place(M,kick(),t,.055 if beat%2==0 else .025)
 place(M,hat(),t+.25,.12)
 place(M,mallet(notes[beat%4]),t+.02,.09)
 if beat%2:place(M,mallet(notes[(beat+2)%4],.22),t+.25,.045)
for i,t in enumerate(J['new'][:-2]):place(FX,mallet([74,78,81,86][i%4],.17),t,.027)
with wave.open('vo/vo-tight.wav') as w:v=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768
V=np.zeros(N);V[:min(N,len(v))]=v[:N]*.82
# Fast moving energy envelope, with smooth attack and release.
x=(np.abs(V)>.018).astype(float);k=int(.15*SR);cs=np.r_[0,np.cumsum(np.pad(x,(k//2,k-k//2)))];env=(cs[k:k+N]-cs[:N])/k;env=np.clip(env*3,0,1)
t=np.arange(N)/SR;fade=np.minimum(t/.03,1)*np.clip((DUR-t)/.8,0,1)
bed=(M*(1-.62*env)+FX)*fade
mix=V+bed;peak=np.max(np.abs(mix));mix*=min(1,.94/peak)
def save(name,x):
 stereo=np.column_stack([x,x*.99]);
 with wave.open(name,'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(stereo,-1,1)*32767).astype(np.int16).tobytes())
save('music-only.wav',(M+FX)*fade);save('music-final.wav',mix)
lines=json.loads(Path('voice-lines.json').read_text())['V07']['lines']
Path('timeline.js').write_text('const TIMELINE='+json.dumps(J)+';\nconst LINES='+json.dumps([x[1] for x in lines])+';\nconst LINE_ENDS='+json.dumps([J['new'][i+1]-(lines[i+1][-1] if i+1<len(lines) else 0) for i in range(len(lines))])+';\n')
print(json.dumps({'duration':DUR,'peak':float(np.max(np.abs(mix))),'rms':float(np.sqrt(np.mean(mix**2))),'voice_lines':len(lines)},indent=2))
