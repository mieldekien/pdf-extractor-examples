"""PDF Text Extractor — Python example.

Usage:
    export RAPIDAPI_KEY="your_key"
    python examples/python.py https://example.com/file.pdf
"""

import os
import sys
import base64
import requests


API_URL = "https://pdf-text-extractor5.p.rapidapi.com/api/extract"
API_HOST = "pdf-text-extractor5.p.rapidapi.com"


def extract_from_url(url: str, api_key: str) -> dict:
    r = requests.post(
        API_URL,
        json={"url": url},
        headers={
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": API_HOST,
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def extract_from_file(path: str, api_key: str) -> dict:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    r = requests.post(
        API_URL,
        json={"base64": b64},
        headers={
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": API_HOST,
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def main():
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        print("Set RAPIDAPI_KEY first. Get one at:")
        print("https://rapidapi.com/mieldekien8660/api/pdf-text-extractor5")
        sys.exit(1)

    arg = sys.argv[1] if len(sys.argv) > 1 else (
        "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    )

    data = (
        extract_from_file(arg, key)
        if os.path.isfile(arg)
        else extract_from_url(arg, key)
    )

    if not data.get("success"):
        print("Extraction failed:", data.get("error"))
        sys.exit(1)

    print(f"Pages: {data['pages']}")
    print(f"Words: {data['words']}")
    if data.get("probablyScanned"):
        print("⚠️  Probably a scanned PDF (needs OCR)")
    print("\n--- TEXT (first 500 chars) ---")
    print(data["text"][:500])


if __name__ == "__main__":
    main()
