#!/usr/bin/env bash
# PDF Text Extractor — cURL example (base64 input)
# Usage:
#   export RAPIDAPI_KEY="your_key_here"
#   ./examples/curl-base64.sh path/to/file.pdf

set -e

FILE="${1:-./sample.pdf}"

if [ -z "$RAPIDAPI_KEY" ]; then
  echo "Set RAPIDAPI_KEY first."
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "File not found: $FILE"
  exit 1
fi

B64=$(base64 -i "$FILE" | tr -d '\n')

curl -sS -X POST "https://pdf-text-extractor5.p.rapidapi.com/api/extract" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: ${RAPIDAPI_KEY}" \
  -H "X-RapidAPI-Host: pdf-text-extractor5.p.rapidapi.com" \
  -d "{\"base64\":\"${B64}\"}" \
  | jq .
