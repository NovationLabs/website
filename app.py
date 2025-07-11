from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

def get_translation(lang_code):
    if lang_code not in ['fr', 'en']:
        lang_code = 'en'
    path = os.path.join('translations', f'{lang_code}.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    lang = request.accept_languages.best_match(['fr', 'en'])
    translation = get_translation(lang)
    return render_template('index.html', t=translation)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9997, debug=True)
