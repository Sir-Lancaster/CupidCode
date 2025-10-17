import json
import os
import requests
import logging

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.http import HttpRequest
from django.http import FileResponse

from api.models import User
# Load manifest when server launches
MANIFEST = {}
if not settings.DEBUG:
    logger = logging.getLogger(__name__)
    candidates = [
        os.path.join(settings.BASE_DIR, "core", "static", "core", ".vite", "manifest.json"),
        os.path.join(settings.BASE_DIR, "core", "static", "core", "manifest.json"),
        os.path.join(settings.BASE_DIR, "static", "core", "manifest.json"),
    ]
    for p in candidates:
        try:
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    MANIFEST = json.load(f)
                logger.info("Loaded Vite manifest from %s", p)
                break
        except Exception as e:
            logger.warning("Failed to load Vite manifest at %s: %s", p, e)
    else:
        # No manifest found — log (do not raise) so app does not 500
        logger.warning("Vite manifest not found in expected locations. Frontend assets may be missing.")
# ...existing code...


def index(req):
    context = {
        'asset_url': os.environ.get('ASSET_URL', ''),
        'debug': settings.DEBUG,
        'manifest': MANIFEST,
        'js_file': '' if settings.DEBUG else MANIFEST.get('src/main.js', {}).get('file', ''),
        'css_file': '' if settings.DEBUG else MANIFEST.get('src/main.js', {}).get('css', [''])[0]
    }
    return render(req, 'core/index.html', context)


def get_image(req: HttpRequest):
    FILE_EXTENSION = os.environ.get('FILE_EXTENSION', '')
    VAULT_PATH = os.environ.get('VAULT_PATH', '')
    path = os.path.join(VAULT_PATH, 'cupid_logo' + '.' + FILE_EXTENSION)
    return FileResponse(open(path, "rb"))

def get_graph(req: HttpRequest):
    FILE_EXTENSION = os.environ.get('FILE_EXTENSION', '')
    VAULT_PATH = os.environ.get('VAULT_PATH', '')
    path = os.path.join(VAULT_PATH, 'graph' + '.' + FILE_EXTENSION)
    return FileResponse(open(path, "rb"))

@login_required
def logout_view(request):
    logout(request)
    return redirect("/")
