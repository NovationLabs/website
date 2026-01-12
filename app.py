from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn, os, json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_translation(lang_code):
    if lang_code not in ['fr', 'en']:
        lang_code = 'en'
    path = os.path.join('translations', f'{lang_code}.json')
    if not os.path.exists(path):
        path = os.path.join('translations', 'en.json')

    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_language_from_header(accept_language: str) -> str:
    if not accept_language:
        return 'en'
    langs = [l.strip().split(';')[0].split('-')[0].lower() for l in accept_language.split(',')]
    for lang in langs:
        if lang == 'fr':
            return 'fr'
        if lang == 'en':
            return 'en'
    return 'en'

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    accept_language = request.headers.get("accept-language", "")
    lang = get_language_from_header(accept_language)
    translation = get_translation(lang)
    return templates.TemplateResponse("index.html", {"request": request, "t": translation})

if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=9998, reload=True)
