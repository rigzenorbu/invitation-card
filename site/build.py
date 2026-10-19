"""Build the two outputs from src.html:
   page.html  – self-contained page for the Claude artifact (images embedded as data URIs)
   index.html – standalone site for any web host (uses the files in assets/)"""
import base64, json, pathlib
here = pathlib.Path(__file__).parent
src = (here / 'src.html').read_text()
files = {'env_back': 'env_back.webp', 'env_front': 'env_front.webp', 'env_flap': 'env_flap.webp',
         'letter': 'letter.webp', 'seal': 'seal.webp', 'poster': 'poster.jpg', 'bg': 'new_background.png'}
mime = {'webp': 'image/webp', 'jpg': 'image/jpeg', 'png': 'image/png'}

def uri(f):
    return f'data:{mime[f.rsplit(".", 1)[1]]};base64,' + base64.b64encode((here / 'assets' / f).read_bytes()).decode()

embedded = {k: uri(f) for k, f in files.items()} | {'video': 'data:video/mp4;base64,' + base64.b64encode((here / 'assets' / 'intro.mp4').read_bytes()).decode()}
linked = {k: 'assets/' + f for k, f in files.items()} | {'video': 'assets/intro.mp4'}

(here / 'page.html').write_text(src.replace('/*ASSETS*/null', json.dumps(embedded)))
head, rest = src.split('</style>', 1)
(here / 'index.html').write_text(
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    + head + '</style>\n</head>\n<body>\n' + rest.replace('/*ASSETS*/null', json.dumps(linked)) + '\n</body>\n</html>\n')
print('page.html', (here / 'page.html').stat().st_size, 'bytes')
