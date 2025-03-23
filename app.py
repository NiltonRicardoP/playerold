from flask import Flask, render_template, Response, request
from flask_cors import CORS
import requests
from urllib.parse import urljoin
import os

app = Flask(__name__)
CORS(app)

RADIO_HOST = 'http://82.145.41.50:7005/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream/<path:path>')
def stream(path):
    proxied_url = urljoin(RADIO_HOST, path)
    headers = {'User-Agent': request.headers.get('User-Agent', '')}
    try:
        r = requests.get(proxied_url, headers=headers, stream=True, timeout=10)
        return Response(r.iter_content(chunk_size=1024), content_type=r.headers.get('Content-Type', 'audio/mpeg'))
    except Exception as e:
        return f"Erro ao acessar rádio: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
