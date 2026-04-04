#!/usr/bin/env python3
"""
Dashboard Web léger pour ONKYO TX-RZ50 via FastAPI.

Interface de contrôle du récepteur accessible depuis un navigateur.
Fonctionnalités : alimentation, volume, sources, modes d'écoute, ZONE2.

Dépendances:
    pip install fastapi uvicorn requests

Usage:
    python web_dashboard.py --host 192.168.1.100
    # Ouvrir http://localhost:8080 dans un navigateur
"""

import argparse
import logging
import sys
from contextlib import asynccontextmanager

import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException, Timeout

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

SOURCES = [
    {"code": "00", "name": "BD/DVD", "icon": "disc"},
    {"code": "01", "name": "GAME", "icon": "gamepad"},
    {"code": "02", "name": "CBL/SAT", "icon": "tv"},
    {"code": "03", "name": "STRM BOX", "icon": "cast"},
    {"code": "04", "name": "PC", "icon": "desktop"},
    {"code": "05", "name": "AUX", "icon": "aux"},
    {"code": "06", "name": "CD", "icon": "music"},
    {"code": "07", "name": "TV", "icon": "television"},
    {"code": "08", "name": "PHONO", "icon": "record"},
    {"code": "26", "name": "TUNER", "icon": "radio"},
    {"code": "27", "name": "NET", "icon": "wifi"},
    {"code": "28", "name": "USB", "icon": "usb"},
    {"code": "29", "name": "BLUETOOTH", "icon": "bluetooth"},
]

LISTENING_MODES = [
    {"code": "LMST", "name": "Stéréo"},
    {"code": "LMDIR", "name": "Direct"},
    {"code": "LMPDA", "name": "Pure Audio"},
    {"code": "LMDA", "name": "Dolby Atmos"},
    {"code": "LMDTS", "name": "DTS:X"},
    {"code": "LMTHX", "name": "THX Cinema"},
    {"code": "LMTHXM", "name": "THX Music"},
    {"code": "LMTHXG", "name": "THX Games"},
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ONKYO TX-RZ50</title>
<style>
:root { --bg: #1a1a2e; --card: #16213e; --accent: #e94560; --text: #eee; --text-dim: #888; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--text); padding: 1rem; }
.container { max-width: 800px; margin: 0 auto; }
h1 { text-align: center; margin-bottom: 1rem; font-size: 1.5rem; }
.card { background: var(--card); border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem; }
.card h2 { font-size: 1rem; color: var(--text-dim); margin-bottom: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }
.row { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.btn { background: #0f3460; color: var(--text); border: none; padding: 0.6rem 1rem; border-radius: 8px; cursor: pointer; font-size: 0.9rem; transition: background 0.2s; }
.btn:hover { background: #1a5276; }
.btn.active { background: var(--accent); }
.btn.power-on { background: #27ae60; }
.btn.power-off { background: #c0392b; }
.volume-control { display: flex; align-items: center; gap: 1rem; }
.volume-control input[type=range] { flex: 1; accent-color: var(--accent); }
.volume-value { font-size: 1.5rem; font-weight: bold; min-width: 3ch; text-align: center; }
.status { display: flex; justify-content: space-between; align-items: center; }
.status-dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 0.5rem; }
.status-dot.on { background: #27ae60; }
.status-dot.off { background: #c0392b; }
.zone2 { border-left: 3px solid var(--accent); }
</style>
</head>
<body>
<div class="container">
<h1>ONKYO TX-RZ50</h1>

<div class="card">
<div class="status">
<div><span class="status-dot" id="powerDot"></span><span id="powerText">—</span></div>
<div id="sourceText" style="color:var(--text-dim)">—</div>
</div>
</div>

<div class="card">
<h2>Alimentation</h2>
<div class="row">
<button class="btn power-on" onclick="power(true)">ON</button>
<button class="btn power-off" onclick="power(false)">STANDBY</button>
</div>
</div>

<div class="card">
<h2>Volume</h2>
<div class="volume-control">
<span>0</span>
<input type="range" id="volSlider" min="0" max="80" value="0" oninput="setVolume(this.value)">
<span>80</span>
<span class="volume-value" id="volValue">—</span>
</div>
</div>

<div class="card">
<h2>Source</h2>
<div class="row" id="sourceBtns"></div>
</div>

<div class="card">
<h2>Mode d'écoute</h2>
<div class="row" id="modeBtns"></div>
</div>

<div class="card zone2">
<h2>ZONE 2</h2>
<div class="row" style="margin-bottom:0.5rem">
<button class="btn" onclick="zone2Power(true)">ON</button>
<button class="btn" onclick="zone2Power(false)">OFF</button>
</div>
<div class="row" id="zone2SourceBtns"></div>
</div>
</div>

<script>
const API = '';
let currentSource = null;
let currentMode = null;

async function api(method, path, body) {
    const opts = { method, headers: {'Content-Type':'application/json'} };
    if (body) opts.body = JSON.stringify(body);
    const r = await fetch(API + path, opts);
    if (!r.ok) throw new Error(await r.text());
    return r.json();
}

async function power(on) { await api('POST', '/power', {on}); refresh(); }
async function setVolume(v) { await api('POST', '/volume', {level: parseInt(v)}); }
async function setSource(code) { await api('POST', '/source', {code}); refresh(); }
async function setMode(code) { await api('POST', '/mode', {code}); refresh(); }
async function zone2Power(on) { await api('POST', '/zone2/power', {on}); }
async function zone2Source(code) { await api('POST', '/zone2/source', {code}); }

async function refresh() {
    try {
        const s = await (await fetch(API + '/status')).json();
        document.getElementById('powerDot').className = 'status-dot ' + (s.power === 'on' ? 'on' : 'off');
        document.getElementById('powerText').textContent = s.power === 'on' ? 'Allumé' : 'Veille';
        document.getElementById('volValue').textContent = s.volume ?? '—';
        document.getElementById('volSlider').value = s.volume ?? 0;
        document.getElementById('sourceText').textContent = s.source_name ?? '—';
        currentSource = s.source_code;
        document.querySelectorAll('#sourceBtns .btn').forEach(b => {
            b.classList.toggle('active', b.dataset.code === currentSource);
        });
        document.querySelectorAll('#modeBtns .btn').forEach(b => {
            b.classList.toggle('active', b.dataset.code === currentMode);
        });
    } catch(e) { console.error(e); }
}

// Build source buttons
const sources = SOURCES_PLACEHOLDER;
const sourceContainer = document.getElementById('sourceBtns');
sources.forEach(s => {
    const btn = document.createElement('button');
    btn.className = 'btn';
    btn.dataset.code = s.code;
    btn.textContent = s.name;
    btn.onclick = () => setSource(s.code);
    sourceContainer.appendChild(btn);
});

// Build mode buttons
const modes = MODES_PLACEHOLDER;
const modeContainer = document.getElementById('modeBtns');
modes.forEach(m => {
    const btn = document.createElement('button');
    btn.className = 'btn';
    btn.dataset.code = m.code;
    btn.textContent = m.name;
    btn.onclick = () => setMode(m.code);
    modeContainer.appendChild(btn);
});

// Build zone2 source buttons
const z2Container = document.getElementById('zone2SourceBtns');
sources.forEach(s => {
    const btn = document.createElement('button');
    btn.className = 'btn';
    btn.textContent = s.name;
    btn.onclick = () => zone2Source(s.code);
    z2Container.appendChild(btn);
});

refresh();
setInterval(refresh, 5000);
</script>
</body>
</html>"""


class OnkyoClient:
    """Client HTTP pour le TX-RZ50."""

    def __init__(self, host: str, username: str = "admin", password: str = "admin"):
        self.base_url = f"http://{host}"
        self.auth = HTTPBasicAuth(username, password)

    def _post(self, endpoint: str, payload: dict):
        url = f"{self.base_url}{endpoint}"
        try:
            r = requests.post(url, json=payload, auth=self.auth, timeout=5)
            r.raise_for_status()
            return r.json()
        except Timeout as e:
            raise HTTPException(status_code=504, detail=f"Timeout: {e}") from e
        except RequestException as e:
            raise HTTPException(status_code=502, detail=str(e)) from e

    def _get(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        try:
            r = requests.get(url, auth=self.auth, timeout=5)
            r.raise_for_status()
            return r.json()
        except Timeout as e:
            raise HTTPException(status_code=504, detail=f"Timeout: {e}") from e
        except RequestException as e:
            raise HTTPException(status_code=502, detail=str(e)) from e

    def get_status(self):
        data = self._get("/Status/getStatus")
        source_code = str(data.get("source", "00"))
        source_name = next(
            (s["name"] for s in SOURCES if s["code"] == source_code), "Unknown"
        )
        return {
            "power": data.get("power", "unknown"),
            "volume": data.get("volume", 0),
            "source_code": source_code,
            "source_name": source_name,
        }

    def set_power(self, on: bool):
        return self._post("/Power/setPower", {"power": "on" if on else "standby"})

    def set_volume(self, level: int):
        level = max(0, min(80, level))
        return self._post("/Volume/setVolume", {"volume": level})

    def set_source(self, code: str):
        return self._post("/Source/setSource", {"source": code})

    def set_mode(self, code: str):
        return self._post("/ListeningMode/setListeningMode", {"mode": code})

    def zone2_power(self, on: bool):
        return self._post("/Zone2/setPower", {"power": "on" if on else "standby"})

    def zone2_source(self, code: str):
        return self._post("/Zone2/setSource", {"source": code})


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Dashboard ONKYO TX-RZ50 -> {app.state.onkyo_host}")
    yield


def create_app(onkyo_host: str, username: str, password: str) -> FastAPI:
    app = FastAPI(title="ONKYO TX-RZ50 Dashboard", lifespan=lifespan)
    app.state.onkyo_host = onkyo_host
    client = OnkyoClient(onkyo_host, username, password)

    sources_json = json_dumps(SOURCES)
    modes_json = json_dumps(LISTENING_MODES)
    html = HTML_TEMPLATE.replace("SOURCES_PLACEHOLDER", sources_json).replace(
        "MODES_PLACEHOLDER", modes_json
    )

    @app.get("/", response_class=HTMLResponse)
    async def index():
        return HTMLResponse(content=html)

    @app.get("/status")
    async def status():
        return client.get_status()

    @app.post("/power")
    async def power(req: dict):
        return client.set_power(req.get("on", False))

    @app.post("/volume")
    async def volume(req: dict):
        return client.set_volume(req.get("level", 0))

    @app.post("/source")
    async def source(req: dict):
        return client.set_source(req.get("code", "00"))

    @app.post("/mode")
    async def mode(req: dict):
        return client.set_mode(req.get("code", "LMST"))

    @app.post("/zone2/power")
    async def z2_power(req: dict):
        return client.zone2_power(req.get("on", False))

    @app.post("/zone2/source")
    async def z2_source(req: dict):
        return client.zone2_source(req.get("code", "00"))

    return app


def json_dumps(obj):
    import json

    return json.dumps(obj)


def main():
    parser = argparse.ArgumentParser(description="Dashboard Web ONKYO TX-RZ50")
    parser.add_argument("--host", required=True, help="IP du TX-RZ50")
    parser.add_argument("--user", default="admin", help="Identifiant Web Setup")
    parser.add_argument(
        "--pass", dest="password", default="admin", help="Mot de passe Web Setup"
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port du serveur (défaut: 8080)"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode debug")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        import uvicorn
    except ImportError:
        print("Erreur: uvicorn n'est pas installé.")
        print("Installer avec: pip install uvicorn")
        sys.exit(1)

    app = create_app(args.host, args.user, args.password)
    logger.info(f"Dashboard disponible sur http://localhost:{args.port}")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=args.port,
        log_level="info" if not args.verbose else "debug",
    )


if __name__ == "__main__":
    main()
