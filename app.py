from flask import Flask, render_template, Response, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

RADIO_STREAM_URL = "http://82.145.41.50:7005/;stream.mp3"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    try:
        headers = {
            'Icy-MetaData': '1',
            'User-Agent': request.headers.get('User-Agent', 'Mozilla/5.0'),
        }
        r = requests.get(RADIO_STREAM_URL, headers=headers, stream=True, timeout=10)
        return Response(
            r.iter_content(chunk_size=1024),
            content_type="audio/mpeg"
        )
    except Exception as e:
        return f"Erro ao acessar stream: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
