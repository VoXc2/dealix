#!/usr/bin/env python3
from __future__ import annotations
import argparse, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DEFAULT_HTML=ROOT/'assets/company-profile/Dealix_Company_Profile_2026.html'
DEFAULT_OUT=ROOT/'artifacts/commercial/Dealix_Company_Profile_2026.pdf'
BROWSERS=['chromium','chromium-browser','google-chrome','google-chrome-stable']
def render_browser(browser: str, src: Path, out: Path) -> int:
    p=subprocess.run([browser,'--headless','--disable-gpu','--no-sandbox','--disable-dev-shm-usage','--print-to-pdf-no-header',f'--print-to-pdf={out}',src.resolve().as_uri()],check=False,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if p.returncode: sys.stderr.write(p.stdout)
    return p.returncode
def render_playwright(src: Path, out: Path) -> int:
    try: from playwright.sync_api import sync_playwright
    except ImportError: return 127
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); page=b.new_page(viewport={'width':1600,'height':1131}); page.goto(src.resolve().as_uri(),wait_until='networkidle'); page.pdf(path=str(out),format='A4',landscape=True,print_background=True,margin={'top':'0','right':'0','bottom':'0','left':'0'}); b.close()
    return 0
def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('--html',type=Path,default=DEFAULT_HTML); ap.add_argument('--out',type=Path,default=DEFAULT_OUT); a=ap.parse_args(); src=a.html.resolve(); out=a.out.resolve()
    if not src.is_file(): print(f'COMPANY_PROFILE=BLOCKED_HTML_MISSING path={src}'); return 2
    out.parent.mkdir(parents=True,exist_ok=True)
    for name in BROWSERS:
        binary=shutil.which(name)
        if binary and render_browser(binary,src,out)==0 and out.is_file() and out.stat().st_size>20_000: print(f'COMPANY_PROFILE=PASS renderer={name} path={out} bytes={out.stat().st_size}'); return 0
    if render_playwright(src,out)==0 and out.is_file() and out.stat().st_size>20_000: print(f'COMPANY_PROFILE=PASS renderer=playwright path={out} bytes={out.stat().st_size}'); return 0
    print('COMPANY_PROFILE=HOLD_NO_SUPPORTED_RENDERER'); return 3
if __name__=='__main__': raise SystemExit(main())
