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

logger = logging.getLogger(__name__)
MANIFEST = {}
def _load_manifest():
    global MANIFEST
    if MANIFEST:
        return MANIFEST
    if settings.DEBUG:
        return {}
    manifest_path = os.path.join(settings.BASE_DIR, "core", "static", ".vite", "manifest.json")
    try:
        if os.path.exists(manifest_path):
            with open(manifest_path, "r", encoding="utf-8") as f:
                MANIFEST = json.load(f)
        else:
            logger.warning("Vite manifest not found at %s", manifest_path)
            MANIFEST = {}
    except Exception:
        logger.exception("Failed to load Vite manifest from %s", manifest_path)
        MANIFEST = {}
    return MANIFEST


def index(req):
    MANIFEST = _load_manifest()
    context = {
        'asset_url': os.environ.get('ASSET_URL', ''),
        'debug': settings.DEBUG,
        'manifest': MANIFEST,
        'js_file': '' if settings.DEBUG else MANIFEST.get('src/main.js', {}).get('file', ''),
        'css_file': '' if settings.DEBUG else MANIFEST.get('src/main.js', {}).get('css', [''])[0]
    }
    return render(req, 'core/index.html', context)


def get_image(req: HttpRequest):
    path = os.path.join(settings.BASE_DIR, "core", "static", "cupid_logo.png")
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
