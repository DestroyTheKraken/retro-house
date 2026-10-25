#!/usr/bin/env python3
"""Apply the Retro House Batocera look on a machine that already has Batocera.

This file is the public installer. It does not read or publish Wi-Fi,
ScreenScraper, RetroAchievements, NAS addresses, or account files.
Running it on an existing console only sets the keys below. Everything
else in batocera.conf and es_settings.cfg is left as it is.
"""

import io
import shutil
import sys
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

REPO = "https://github.com/DestroyTheKraken/retro-house"
RAW = "https://raw.githubusercontent.com/DestroyTheKraken/retro-house/main"

# Names that must never be written by this installer.
FORBIDDEN = (
    "ssid",
    "wifi",
    "screenscraper",
    "screen scraper",
    "password",
    "passwd",
    "psk",
    "token",
    "secret",
    "apikey",
    "api_key",
    "login",
    "retroachievements",
    "cheevos",
)

# Portable settings only. No network, no accounts, no machine addresses.
CONF_KEYS = {
    "kodi.enabled": "1",
    "kodi.atstartup": "0",
    "kodi.xbutton": "1",
    "splash.screen.enabled": "1",
    "splash.screen.sound": "0",
    "system.timezone": "America/Los_Angeles",
    "audio.bgmusic": "1",
    "audio.volume": "35",
    "controllers.bluetooth.enabled": "1",
    "controllers.xarcade.enabled": "1",
    "global.videooutput": "HDMI-1",
    "global.ai_service_enabled": "0",
    "global.netplay": "0",
    "global.batterymode": "highperformance",
    "global.powermode": "highperformance",
    "system.cpu.governor": "schedutil",
    "updates.enabled": "1",
    "updates.type": "stable",
}

# EmulationStation look. Not accounts, not gamelists.
ES_KEYS = (
    ("bool", "ClockMode12", "true"),
    ("bool", "StartupOnGameList", "true"),
    ("int", "ScreenSaverTime", "3600000"),
    ("string", "PowerSaverMode", "disabled"),
    ("string", "SortSystems", "hardware"),
    ("string", "StartupSystem", "all"),
    ("string", "CollectionSystemsAuto", "all,arcade"),
    ("string", "ThemeSet", "es-theme-batocer-club-reloaded"),
    ("string", "ThemeColorSet", "defaultBlue"),
    ("string", "ThemeRegionName", "us"),
    ("string", "TransitionStyle", "fade & slide"),
    ("string", "subset.staticEffect", "crt"),
    ("string", "subset.staticEffectApply", "screenApply"),
    ("string", "subset.transition", "yes"),
    ("string", "subset.wallpaperVideo", "no"),
)

THEMES = (
    (
        "es-theme-batocer-club-reloaded",
        "https://github.com/lehcimcramtrebor/es-theme-batocer-club-reloaded/archive/refs/heads/master.zip",
    ),
    (
        "es-theme-retrorama-ce",
        "https://github.com/lipebello/es-theme-retrorama-ce/archive/refs/heads/master.zip",
    ),
    (
        "ES-THEME-ARCADEPLANET",
        "https://github.com/EvilDindon/ES-THEME-ARCADEPLANET/archive/refs/heads/master.zip",
    ),
)

SPLASH = ("dtk-boot.mp4", "dtk-bg.jpg")


def refuse(label):
    low = label.lower().replace("_", "").replace(".", "").replace("-", "")
    for word in FORBIDDEN:
        if word.replace(" ", "").replace("_", "") in low:
            sys.exit("Refusing to write a private setting: " + label)


def download(url, timeout=180):
    print("  get " + url)
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read()


def install_theme(dest_name, url, themes_dir):
    dest = themes_dir / dest_name
    if (dest / "theme.xml").is_file():
        print("Theme already installed: " + dest_name)
        return
    print("Installing " + dest_name + " from the author's repository")
    blob = download(url, timeout=600)
    archive = zipfile.ZipFile(io.BytesIO(blob))
    roots = {name.split("/")[0] for name in archive.namelist() if "/" in name}
    if len(roots) != 1:
        sys.exit("Unexpected theme archive layout for " + dest_name)
    root = roots.pop()
    staging = themes_dir / (".partial-" + dest_name)
    if staging.exists():
        shutil.rmtree(staging)
    archive.extractall(themes_dir)
    extracted = themes_dir / root
    extracted.rename(staging)
    if dest.exists():
        shutil.rmtree(dest)
    staging.rename(dest)
    if not (dest / "theme.xml").is_file():
        sys.exit("Theme install did not include theme.xml: " + dest_name)


def install_splash(script_dir, splash_dir):
    splash_dir.mkdir(parents=True, exist_ok=True)
    local = script_dir / "splash"
    for name in SPLASH:
        target = splash_dir / name
        bundled = local / name
        if bundled.is_file():
            shutil.copyfile(bundled, target)
        else:
            target.write_bytes(download(RAW + "/splash/" + name))
        print("Splash: " + name)


def merge_conf(path):
    for key in CONF_KEYS:
        refuse(key)
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines() if path.is_file() else []
    seen = set()
    out = []
    for line in lines:
        if "=" in line and not line.lstrip().startswith("#"):
            key = line.split("=", 1)[0].strip()
            if key in CONF_KEYS:
                out.append(key + "=" + CONF_KEYS[key])
                seen.add(key)
                continue
        out.append(line)
    for key, value in CONF_KEYS.items():
        if key not in seen:
            out.append(key + "=" + value)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def merge_es(path):
    for _tag, name, _value in ES_KEYS:
        refuse(name)
    if path.is_file():
        tree = ET.parse(path)
        root = tree.getroot()
    else:
        root = ET.Element("config")
        tree = ET.ElementTree(root)
    for tag, name, value in ES_KEYS:
        found = None
        for element in root.findall(tag):
            if element.get("name") == name:
                found = element
                break
        if found is None:
            found = ET.SubElement(root, tag)
            found.set("name", name)
        found.set("value", value)
    path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def backup(paths, stamp):
    folder = Path("/userdata/system") / ("retro-house-backup-" + stamp)
    folder.mkdir(parents=True, exist_ok=True)
    for path in paths:
        if path.is_file():
            shutil.copy2(path, folder / path.name)
    print("Backup: " + str(folder))


def main():
    if not Path("/userdata/system").is_dir():
        sys.exit("Run this on the Batocera machine, as root.")
    script_dir = Path(__file__).resolve().parent
    conf = Path("/userdata/system/batocera.conf")
    es = Path("/userdata/system/configs/emulationstation/es_settings.cfg")
    themes = Path("/userdata/themes")
    splash = Path("/userdata/splash")
    themes.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup((conf, es), stamp)
    for name, url in THEMES:
        install_theme(name, url, themes)
    install_splash(script_dir, splash)
    merge_conf(conf)
    merge_es(es)
    print("")
    print("Retro House look is staged.")
    print("ROMs, gamelists, Wi-Fi, and ScreenScraper were not changed.")
    print("Reboot so the splash is copied to the boot partition.")
    print("In Kodi, install the Copacetic skin from the official Kodi repository.")
    print("Source: " + REPO)


if __name__ == "__main__":
    main()
