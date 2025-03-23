from flask import Flask, render_template, Response, request
from flask_cors import CORS
import http.client
import os

app = Flask(__name__)
CORS(app)

RADIO_HOST = '82.145.41.50'
RADIO_PORT = 7005

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream/<path:path>')
def stream(path):
    try:
        conn = http.client.HTTPConnection(RADIO_HOST, RADIO_PORT, timeout=10)
        conn.putrequest("GET", f"/{path}")
        conn.putheader("User-Agent", request.headers.get("User-Agent", ""))
        conn.endheaders()

        res = conn.getresponse()
        if res.status != 200:
            return f"Erro ao acessar rádio: {res.status} {res.reason}", 500

        def generate():
            while True:
                chunk = res.read(1024)
                if not chunk:
                    break
                yield chunk

        return Response(generate(), content_type="audio/mpeg")

    except Exception as e:
        return f"Erro ao acessar rádio: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render define a porta pela env PORT
    app.run(host='0.0.0.0', port=port)
