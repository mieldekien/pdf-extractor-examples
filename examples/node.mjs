// PDF Text Extractor — Node.js example (Node 18+, native fetch)
// Usage:
//   RAPIDAPI_KEY="your_key" node examples/node.mjs https://example.com/file.pdf

const KEY = process.env.RAPIDAPI_KEY;
if (!KEY) {
  console.error("Missing RAPIDAPI_KEY env var.");
  console.error("Get one at https://rapidapi.com/mieldekien8660/api/pdf-text-extractor5");
  process.exit(1);
}

const pdfUrl =
  process.argv[2] ??
  "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf";

const res = await fetch(
  "https://pdf-text-extractor5.p.rapidapi.com/api/extract",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-RapidAPI-Key": KEY,
      "X-RapidAPI-Host": "pdf-text-extractor5.p.rapidapi.com",
    },
    body: JSON.stringify({ url: pdfUrl }),
  }
);

const data = await res.json();

if (!data.success) {
  console.error("Extraction failed:", data.error ?? data);
  process.exit(1);
}

console.log(`Pages: ${data.pages}`);
console.log(`Words: ${data.words}`);
console.log(`Characters: ${data.characters}`);
if (data.probablyScanned) console.log("⚠️  Probably a scanned PDF (needs OCR)");
console.log("\n--- TEXT (first 500 chars) ---");
console.log(data.text.slice(0, 500));
