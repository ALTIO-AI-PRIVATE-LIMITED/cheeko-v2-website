"""Original light comedy score: D-major pizzicato, playful bass, tiny desk bells and a falling market sting."""
from pathlib import Path
import json,wave
import numpy as np
SR=44100;J=json.loads(Path('warp.json').read_text());DUR=J['dur'];N=round(DUR*SR);rng=np.random.default_rng(808)
M=np.zeros(N);FX=np.zeros(N)
def T(d):return np.arange(round(d*SR))/SR
def hz(m):return 440*2**((m-69)/12)
def W(t):return float(np.interp(t,[0]+J['old'],[0]+J['new']))
def put(dst,x,t,g=1):
 a=round(t*SR);b=min(N,a+len(x))
 if 0<=a<b:dst[a:b]+=x[:b-a]*g
def pluck(m,d=.27):
 t=T(d);f=hz(m);env=np.minimum(t/.004,1)*np.exp(-t*15)*np.minimum((d-t)/.015,1)
 return (np.sin(2*np.pi*f*t)+.35*np.sin(4*np.pi*f*t)+.13*np.sin(6*np.pi*f*t))*env
def bass(m):
 t=T(.33);f=hz(m);return (np.sin(2*np.pi*f*t)+.18*np.sin(4*np.pi*f*t))*np.minimum(t/.007,1)*np.exp(-t*12)
def tick():
 t=T(.035);return rng.normal(0,.25,len(t))*np.exp(-t*150)*np.minimum(t/.002,1)
def bell(m):
 t=T(.32);f=hz(m);return (np.sin(2*np.pi*f*t)+.25*np.sin(2*np.pi*2.01*f*t))*np.exp(-t*14)*np.minimum(t/.003,1)
def boing():
 t=T(.23);return np.sin(2*np.pi*(120*t+90*.04*(1-np.exp(-t/.04))))*np.exp(-t*17)*.16
chords=[(38,[62,66,69]),(45,[61,64,69]),(47,[62,66,71]),(43,[62,67,71])]
for beat in range(int(DUR/.5)+1):
 t=beat*.5;root,notes=chords[(beat//4)%4];put(M,bass(root if beat%2==0 else root+7),t,.095)
 for n in notes:put(M,pluck(n),t+.25,.027)
 put(M,tick(),t+.25,.14)
 if beat%4 in (1,3):put(M,pluck(notes[beat%3]+12,.18),t+.375,.025)
# Brand reveal brightens the same musical idea.
for i,m in enumerate([74,78,81,86]):put(FX,bell(m),W(18)+i*.09,.08)
# Three portfolio crayons each get a little note.
for i,m in enumerate([74,78,81]):put(FX,bell(m),W(4)+i*.18,.035)
put(FX,boing(),W(13.2),.38)
for t in [7.8,9.5,10.7,11.9,22,22.7,23.4]:put(FX,pluck(74,.12),W(t),.06)
# Soft descending bassoon-like sting on the falling portfolio callback.
for i,m in enumerate([57,54,50]):
 t=T(.27);f=hz(m);sig=(np.sin(2*np.pi*f*t)+.15*np.sin(6*np.pi*f*t))*np.minimum(t/.025,1)*np.exp(-t*8)
 put(FX,sig,W(28.0)+i*.19,.065)
for i,m in enumerate([74,78,81]):put(FX,bell(m),DUR-.7+i*.11,.035)
with wave.open('vo/vo-tight.wav') as w:v=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768
V=np.zeros(N);V[:min(N,len(v))]=v[:N]*.82
x=(np.abs(V)>.018).astype(float);k=int(.15*SR);cs=np.r_[0,np.cumsum(np.pad(x,(k//2,k-k//2)))];env=np.clip((cs[k:k+N]-cs[:N])/k*3,0,1)
t=np.arange(N)/SR;fade=np.minimum(t/.02,1)*np.clip((DUR-t)/.6,0,1)
# A short musical breath makes the sarcastic "Brilliant" land.
break_t=W(13.2);dip=1-.9*np.exp(-((t-break_t)/.16)**6)
bed=(M*(1-.62*env)*dip+FX)*fade;mix=V+bed;mix*=min(1,.94/np.max(np.abs(mix)))
def save(n,x):
 st=np.column_stack([x,x*.985]);
 with wave.open(n,'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(st,-1,1)*32767).astype(np.int16).tobytes())
save('music-only.wav',(M*dip+FX)*fade);save('music-final.wav',mix)
L=json.loads(Path('voice-lines.json').read_text())['V08']['lines']
Path('timeline.js').write_text('const TIMELINE='+json.dumps(J)+';\nconst LINES='+json.dumps([l[1] for l in L])+';\nconst LINE_ENDS='+json.dumps([J['new'][i+1]-(L[i+1][-1] if i+1<len(L) else 0) for i in range(len(L))])+';\n')
print(json.dumps({'duration':DUR,'peak':float(abs(mix).max()),'rms':float(np.sqrt(np.mean(mix**2))),'voice_lines':len(L)}))
