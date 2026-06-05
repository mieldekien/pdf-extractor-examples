<?php
// PDF Text Extractor — PHP example
// Usage:
//   RAPIDAPI_KEY="your_key" php examples/php.php https://example.com/file.pdf

$key = getenv('RAPIDAPI_KEY');
if (!$key) {
    fwrite(STDERR, "Set RAPIDAPI_KEY first.\n");
    exit(1);
}

$source = $argv[1] ?? 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf';

if (is_file($source)) {
    $payload = ['base64' => base64_encode(file_get_contents($source))];
} else {
    $payload = ['url' => $source];
}

$ch = curl_init('https://pdf-text-extractor5.p.rapidapi.com/api/extract');
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode($payload),
    CURLOPT_HTTPHEADER => [
        'Content-Type: application/json',
        'X-RapidAPI-Key: ' . $key,
        'X-RapidAPI-Host: pdf-text-extractor5.p.rapidapi.com',
    ],
    CURLOPT_TIMEOUT => 30,
]);
$body = curl_exec($ch);
curl_close($ch);

$data = json_decode($body, true);

if (!($data['success'] ?? false)) {
    fwrite(STDERR, "Extraction failed: " . ($data['error'] ?? 'unknown') . "\n");
    exit(1);
}

echo "Pages: {$data['pages']}\n";
echo "Words: {$data['words']}\n";
if ($data['probablyScanned'] ?? false) {
    echo "⚠️  Probably a scanned PDF (needs OCR)\n";
}
echo "\n--- TEXT (first 500 chars) ---\n";
echo substr($data['text'], 0, 500) . "\n";
