# Retro House

A one-step Batocera look for a home lab TV. It installs the menu themes used on this build, the Destroy the Kraken boot splash, and a short list of display settings.

It does not install games. Bring your own legal library. This repository has no ROMs, no scraped metadata, no gamelists, no Wi-Fi name or password, no ScreenScraper account, and no network addresses.

## Install

On the Batocera machine, as root, with a network connection:

```bash
curl -fsSL https://raw.githubusercontent.com/DestroyTheKraken/retro-house/main/install.py -o /tmp/retro-house-install.py
python3 /tmp/retro-house-install.py
reboot
```

The script downloads the themes from the authors' repositories. Batocera Club Reloaded is large because it includes video. If a theme is already in `/userdata/themes`, that download is skipped.

The script changes only the settings listed in `install.py`. An existing `batocera.conf` keeps every other line, including a Wi-Fi name or a scraper login that is already on that machine. Those values are not in this repository.

Reboot once. Batocera copies `/userdata/splash` to the boot splash on the next start.

After reboot, open Kodi and install the Copacetic skin from Kodi's own add-on repository: Settings, Add-ons, Install from repository, Look and feel, Skins, Copacetic. This repo does not ship the skin.

In EmulationStation, the menu theme is Batocera Club Reloaded. Arcade Planet and Retrorama Champion Edition are installed beside it so you can switch to them in the theme menu.

## What you still do yourself

Add your own games. Scrape them with your own ScreenScraper account, or skip scraping. Pair your own controllers. Point Kodi at your own movie and music folders. None of that is in this install.

## Credits

The menu themes and the Kodi skin are not mine. They are used unmodified and downloaded from the authors.

**Batocera Club Reloaded**, the theme this build boots into.

Theme mod by SNAKERVILL and The Mini Cake TV. Reloaded by Hel Mic (Lehcim Cram Trebor) and Fred Golfietti, with a Swedish translation by Jonas Bohdén. It is a fork of Retrobat-Roleta by Lorenzolamas. The upstream README says the theme is no longer maintained.

https://github.com/lehcimcramtrebor/es-theme-batocer-club-reloaded

https://www.youtube.com/channel/UCJdquk3Rr_nZVLEc9JryhAA

**Retrorama Champion Edition**, installed as an alternate menu theme.

By Filipe Bello (lipebello). The theme file names the license as Creative Commons CC-BY-NC-SA. The repository also includes the GNU GPL version 3. Use the author's terms. This project does not relicense it.

https://github.com/lipebello/es-theme-retrorama-ce

**Arcade Planet**, installed as an alternate menu theme.

By Mickaël Isman (EvilDindon), 2021. The theme file names the license as Creative Commons CC-BY-NC-SA. The author says it was originally based on the Carbon EmulationStation theme. This project does not relicense it.

https://github.com/EvilDindon/ES-THEME-ARCADEPLANET

**Copacetic**, the Kodi skin on this build. Not downloaded by the installer.

By realcopacetic. Designs are Creative Commons Attribution-NonCommercial-ShareAlike 4.0. The code is GPL-3.0. It started from Hitcher's Copacetic skin. Install it from the official Kodi repository.

https://github.com/realcopacetic/skin.copacetic

https://kodi.wiki/view/Add-on:Copacetic

**Destroy the Kraken splash** (`splash/dtk-boot.mp4` and `splash/dtk-bg.jpg`) is the only artwork in this repository. It is the boot screen for this lab. Joshua Hickman, Destroy the Kraken.

The controllers on the original desk are two 8BitDo Pro 2 pads and one 8BitDo Arcade Stick. Pair your own. This repo does not include Bluetooth pairings.

https://www.8bitdo.com/pro2/

https://www.8bitdo.com/arcade-stick/

The computer on the original desk is a used Lenovo ThinkCentre M93p Tiny.

https://psref.lenovo.com/Detail/ThinkCentre/ThinkCentre_M93p_Tiny

## License

The installer script is MIT. See `LICENSE`.

The themes and the Kodi skin stay under the authors' licenses above. Do not sell those themes. Do not put someone else's game files in a download of this repository.
