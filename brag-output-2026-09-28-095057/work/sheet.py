"""Tile every still-<t>.png in time order into sheet.png. Usage: python3 sheet.py [columns]"""
import subprocess, glob, sys
files = sorted(glob.glob('still-*.png'), key=lambda f: float(f[6:-4]))
import shutil; FF = shutil.which('ffmpeg') or subprocess.check_output(['python3', '-c', 'import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())']).decode().strip()
args = [FF, '-y', '-loglevel', 'error']
for f in files: args += ['-i', f]
n = len(files); cols = int(sys.argv[1]) if len(sys.argv) > 1 else 8
scale = ''.join(f'[{i}:v]scale=240:-2[s{i}];' for i in range(n))
if n == 1:
    fc = '[0:v]scale=240:-2'
else:
    fc = scale + ''.join(f'[s{i}]' for i in range(n)) + f'xstack=inputs={n}:layout=' + \
         '|'.join(f'{(i % cols) * 244}_{(i // cols) * 431}' for i in range(n)) + ':fill=black'
subprocess.run(args + ['-filter_complex', fc, '-frames:v', '1', 'sheet.png'], check=True)
print([f[6:-4] for f in files])
