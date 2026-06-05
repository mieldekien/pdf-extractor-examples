// PDF Text Extractor — TypeScript example
// Run: npx tsx examples/typescript.ts <pdf-url>

type ExtractResponse =
  | {
      success: true;
      pages: number;
      words: number;
      characters: number;
      info: Record<string, unknown> | null;
      metadata: Record<string, unknown> | null;
      text: string;
      probablyScanned: boolean;
      extractedAt: string;
    }
  | { success?: false; error: string; detail?: string };

async function extractPdf(
  source: { url: string } | { base64: string },
  apiKey: string
): Promise<ExtractResponse> {
  const res = await fetch(
    "https://pdf-text-extractor5.p.rapidapi.com/api/extract",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": apiKey,
        "X-RapidAPI-Host": "pdf-text-extractor5.p.rapidapi.com",
      },
      body: JSON.stringify(source),
    }
  );
  return (await res.json()) as ExtractResponse;
}

const key = process.env.RAPIDAPI_KEY;
if (!key) {
  console.error("Set RAPIDAPI_KEY env var first.");
  process.exit(1);
}

const url =
  process.argv[2] ??
  "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf";

const result = await extractPdf({ url }, key);
console.log(JSON.stringify(result, null, 2));
