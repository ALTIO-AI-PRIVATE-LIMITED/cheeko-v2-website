"""Trimmed length + 30 fps loudness envelope for every voice clip (vo/clips/FILM_NN.mp3) -> lipsync.json.
The same trim is used when the audio is placed, so envelopes line up with the voice.
Usage (inside work/): ../../.venv/bin/python lipsync.py"""
import glob, json, subprocess, numpy as np
SR = 44100; out = {}
for f in sorted(glob.glob('vo/clips/FILM_*.mp3')):
    i = int(f[-6:-4])
    x = np.frombuffer(subprocess.check_output(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-ar',str(SR),'-f','s16le','-']), dtype=np.int16).astype(float) / 32768
    env = np.convolve(np.abs(x), np.ones(441)/441, mode='same'); on = np.nonzero(env > 0.006)[0]
    y = x[max(0, on[0]-int(.03*SR)): min(len(x), on[-1]+int(.06*SR))]
    hop = SR // 30; fr = [float(np.sqrt(np.mean(y[k*hop:(k+1)*hop]**2))) for k in range(len(y)//hop)]
    m = max(fr); out[i] = {'dur': round(len(y)/SR, 3), 'env': [round(min(1, v/m*1.25), 2) for v in fr]}
json.dump(out, open('lipsync.json', 'w')); print({k: v['dur'] for k, v in out.items()})
