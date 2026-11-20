"""V31 vehicle images through the dev box image lab (images.py); the keys stay on the box in .env.images.
Runs on the dev box: python3 gen_v31.py jobs.json
Job: {"tag", "model", "prompt", "aspect_ratio": "4:3", "resolution": "2K"|"1K", "size": "1536x1152" and "ref": "<style image path on the box>" (Seedream only)}.
Seedream jobs are sent with watermark off (the API's own switch) and an explicit size; Kling goes through images.generate.
Prints one JSON line per job with the provider's usage; copies each result to /root/tts-compare/out/v31/<tag>.<ext>."""
import json, sys, shutil, time, urllib.request
sys.path.insert(0, '/root/tts-compare')
import images
OUT = '/root/tts-compare/out/v31/'
images.load_keys()
import os
for j in json.load(open(sys.argv[1])):
    try:
        t0 = time.monotonic()
        if j['model'].startswith('kling'):
            r = images.generate({'model': j['model'], 'prompt': j['prompt'], 'aspect_ratio': j.get('aspect_ratio', '4:3'), 'resolution': j.get('resolution', '2K')})
            src = images.RESULTS / r['id'] / r['images'][0].split('/')[-1]; dst = OUT + j['tag'] + src.suffix; shutil.copy(src, dst)
            usage = r['response'].get('tokenhub_usage')
        else:
            p = {'model': j['model'], 'prompt': j['prompt'], 'size': j.get('size', '1536x1152'), 'response_format': 'url', 'stream': False, 'watermark': False}
            if j.get('ref'):   # style reference image on the box, sent as a data URL
                import base64
                b = open(j['ref'], 'rb').read(); mime = 'png' if b.startswith(b'\x89PNG') else 'jpeg'
                p['image'] = ['data:image/%s;base64,%s' % (mime, base64.b64encode(b).decode())]
            resp = images.request_json(images.SEEDREAM_URL, os.environ['SEEDREAM_API_KEY'], p)
            raw = urllib.request.urlopen(resp['data'][0]['url'], timeout=180).read()
            dst = OUT + j['tag'] + ('.png' if raw.startswith(b'\x89PNG') else '.jpg'); open(dst, 'wb').write(raw)
            usage = resp.get('usage'); usage['size'] = resp['data'][0].get('size')
        print(json.dumps({'tag': j['tag'], 'file': dst, 's': round(time.monotonic() - t0, 1), 'usage': usage}), flush=True)
    except Exception as e:
        print(json.dumps({'tag': j['tag'], 'error': str(e)[:300]}), flush=True)
