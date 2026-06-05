# PDF Text Extractor — code examples

Quick-start examples for the [PDF Text Extractor API](https://rapidapi.com/mieldekien8660/api/pdf-text-extractor5) on RapidAPI.

Extract clean text + metadata from any PDF (URL or base64) in a single HTTP call. No `pdf-parse` dependency hell. No cold-start pain.

- 🔑 **Get a free API key**: <https://rapidapi.com/mieldekien8660/api/pdf-text-extractor5>

## What the API returns

```json
{
  "success": true,
  "pages": 12,
  "words": 3421,
  "characters": 19872,
  "info": {
    "PDFFormatVersion": "1.4",
    "Author": "Acme Corp",
    "Creator": "Microsoft Word",
    "CreationDate": "D:20240315103221Z"
  },
  "text": "Invoice\nNumber: INV-2024-0312\n…",
  "probablyScanned": false,
  "extractedAt": "2026-06-05T09:42:00.000Z"
}
```

- `text` — extracted plain text
- `probablyScanned: true` — heuristic warning that the PDF likely needs OCR
- `info` — PDF metadata (author, creator, version, etc.)

## Examples

| Language / Use case | File |
|---|---|
| cURL — URL input | [`examples/curl-url.sh`](examples/curl-url.sh) |
| cURL — base64 input | [`examples/curl-base64.sh`](examples/curl-base64.sh) |
| Node.js (Node 18+) | [`examples/node.mjs`](examples/node.mjs) |
| TypeScript | [`examples/typescript.ts`](examples/typescript.ts) |
| Python | [`examples/python.py`](examples/python.py) |
| PHP | [`examples/php.php`](examples/php.php) |
| **LangChain RAG demo** | [`examples/rag-langchain.py`](examples/rag-langchain.py) |

## Setup

1. Get a free API key from the [RapidAPI marketplace](https://rapidapi.com/mieldekien8660/api/pdf-text-extractor5) (50 PDFs/month, no credit card).
2. Export it:

   ```sh
   export RAPIDAPI_KEY="your_key_here"
   ```

3. Run an example:

   ```sh
   node examples/node.mjs https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf
   python examples/python.py https://example.com/sample.pdf
   ```

## Two input modes

**URL** — easiest, the API fetches the PDF for you. Public URL only.

```json
{ "url": "https://example.com/invoice.pdf" }
```

**Base64** — for PDFs you have in memory or behind auth. Encode and send.

```json
{ "base64": "JVBERi0xLjQKJeLjz9MK…" }
```

Max 8 MB either way.

## Pricing

| Plan | Price | Quota |
|---|---|---|
| Basic | Free | 50 PDFs / month |
| Pro | $14.99 / mo | 1 000 PDFs / month |
| Ultra | $59.99 / mo | 10 000 PDFs / month |

## Scanned PDFs

This version is text-only. Scanned (image-only) PDFs return `probablyScanned: true` and empty/very short `text`. OCR support is on the roadmap for v2.

## License

MIT — do whatever you want with the example code.

## Feedback

Built by [miel1](https://rapidapi.com/mieldekien8660). Want OCR or extra format support? Open an issue.
