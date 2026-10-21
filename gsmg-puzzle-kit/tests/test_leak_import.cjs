// Run: node --test tests/test_leak_import.cjs
// Source inspection only: never import leak.py or run cipher operations.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const source = fs.readFileSync(
  path.join(__dirname, '..', 'claude', 'rabbit-holes', 'leak.py'), 'utf8').replace(/\r\n/g, '\n');

function checkAesBinding(text) {
  assert.match(text, /\bAES\.new\(/, 'fixture must retain the AES reference');
  assert.match(text, /^from Crypto\.Cipher import AES[ \t]*$/m,
    'leak.py must bind AES at module scope before main uses it');
}

test('leak.py binds the AES name used by its fake-control source', () => {
  checkAesBinding(source);
});

test('the static check rejects the missing-import regression', () => {
  const missing = source.replace(/^from Crypto\.Cipher import AES[ \t]*\r?\n/m, '');
  assert.notEqual(missing, source, 'negative fixture must remove the import');
  assert.throws(() => checkAesBinding(missing), /must bind AES/);
});

test('an import under another name does not bind AES', () => {
  const renamed = source.replace(/^from Crypto\.Cipher import AES[ \t]*$/m,
    'from Crypto.Cipher import AES as OtherAES');
  assert.notEqual(renamed, source, 'negative fixture must rename the import');
  assert.throws(() => checkAesBinding(renamed), /must bind AES/);
});
