import ftplib
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path("d:/VSCode/HKDN/BookVerse")
STATIC_DIR = ROOT / "duwcsanhlib-static-web"

FTP_HOST = "ftpupload.net"
FTP_USER = "if0_43340192"
FTP_PASS = "BbN4cd1EUQ"

files_to_upload = [
    ("index.html", STATIC_DIR / "index.html"),
    ("store.html", STATIC_DIR / "store.html"),
    ("landing.html", STATIC_DIR / "landing.html"),
    ("index.php", STATIC_DIR / "index.php"),
    (".htaccess", STATIC_DIR / ".htaccess"),
]

assets_to_upload = [
    ("logo-header.png", STATIC_DIR / "assets" / "logo-header.png"),
    ("logo.png", STATIC_DIR / "assets" / "logo.png"),
]

print("Connecting to FTP...")
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
print("Connected:", ftp.getwelcome())

targets = ["/duwcsanhlib.wuaze.com/htdocs", "/htdocs"]

for target in targets:
    print(f"\n==========================================")
    print(f"Deploying to: {target}")
    print(f"==========================================")
    try:
        ftp.cwd(target)
    except Exception as e:
        print(f"Error accessing directory {target}: {e}")
        continue
    
    for filename, filepath in files_to_upload:
        if not filepath.exists():
            print(f"File not found locally: {filepath}")
            continue
        size = filepath.stat().st_size
        print(f"Uploading {filename} ({size:,} bytes)...")
        with open(filepath, "rb") as f:
            ftp.storbinary(f"STOR {filename}", f)
        print(f"  -> Successfully uploaded {filename}")

    # Ensure assets dir exists and upload logos
    try:
        ftp.cwd(f"{target}/assets")
        for filename, filepath in assets_to_upload:
            if filepath.exists():
                size = filepath.stat().st_size
                print(f"Uploading assets/{filename} ({size:,} bytes)...")
                with open(filepath, "rb") as f:
                    ftp.storbinary(f"STOR {filename}", f)
                print(f"  -> Successfully uploaded assets/{filename}")
    except Exception as e:
        print(f"Error uploading to assets: {e}")

ftp.quit()
print("\n>>> All files and assets uploaded successfully! <<<")
