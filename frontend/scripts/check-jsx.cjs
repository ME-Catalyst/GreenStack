const fs = require('fs');
const path = require('path');
const acorn = require('acorn');
const jsx = require('acorn-jsx');

const parser = acorn.Parser.extend(jsx());

const TARGET_DIR = path.join(__dirname, '..', 'src');
const extensions = new Set(['.jsx', '.tsx']);
const issues = [];

function walkDir(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkDir(full);
    } else if (extensions.has(path.extname(entry.name))) {
      checkFile(full);
    }
  }
}

function checkFile(file) {
  const code = fs.readFileSync(file, 'utf8');
  try {
    parser.parse(code, {
      ecmaVersion: 'latest',
      sourceType: 'module',
      locations: true
    });
  } catch (err) {
    issues.push({ file, message: err.message, line: err.loc?.line, column: err.loc?.column });
  }
}

walkDir(TARGET_DIR);

if (issues.length === 0) {
  console.log('No JSX syntax issues detected.');
  process.exit(0);
}

console.log('JSX issues found:');
for (const issue of issues) {
  console.log(`- ${issue.file}:${issue.line ?? '?'}:${issue.column ?? '?'} -> ${issue.message}`);
}
process.exitCode = 1;
