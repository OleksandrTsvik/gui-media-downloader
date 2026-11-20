# gui-media-downloader

## 🚀 How-to run

1. Install Python `3.12.6` and Node.js `23 or later`.
2. Install required dependencies:

```bash
pip install -r requirements.txt

pip install -U yt-dlp-ejs
playwright install --with-deps chromium

winget install ffmpeg                     # PowerShell
winget install -e --id mikf.gallery-dl    # PowerShell
```

3. Run [main.py](src/main.py).

```bash
python src/main.py
```

## 💻 Requirements before pushing changes

1. Update `requirements.txt`:

```bash
pip install pipreqs
pipreqs . --force --ignore ".venv"
```

## ⚠️ Disclaimer

This project is in no way affiliated with, authorized, maintained, or endorsed by YouTube, Google, Meta (including Facebook and Instagram), TikTok, or any other third-party platforms or their affiliates and subsidiaries. It is an independent and unofficial project. Use it at your own risk.

This project is intended for downloading content that you own, have permission to download, or that is otherwise legally available for download. Users are solely responsible for ensuring that their use of this software complies with the Terms of Service of the respective platforms, applicable copyright laws, and other relevant regulations.

The developers do not encourage or condone copyright infringement, unauthorized distribution, or any misuse of this software.

This project is licensed under the MIT License. Refer to the [LICENSE](LICENSE) file for more information.
