#!/usr/bin/env bash
# PDF Text Extractor — cURL example (URL input)
# Usage:
#   export RAPIDAPI_KEY="your_key_here"
#   ./examples/curl-url.sh https://example.com/file.pdf

set -e

URL="${1:-https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf}"

if [ -z "$RAPIDAPI_KEY" ]; then
  echo "Set RAPIDAPI_KEY first. Get one at:"
  echo "https://rapidapi.com/mieldekien8660/api/pdf-text-extractor5"
  exit 1
fi

curl -sS -X POST "https://pdf-text-extractor5.p.rapidapi.com/api/extract" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: ${RAPIDAPI_KEY}" \
  -H "X-RapidAPI-Host: pdf-text-extractor5.p.rapidapi.com" \
  -d "{\"url\":\"${URL}\"}" \
  | jq .
