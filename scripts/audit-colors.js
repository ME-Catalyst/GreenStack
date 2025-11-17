/**
 * Color Audit Script
 *
 * Scans all JSX component files to identify hardcoded colors that need
 * to be replaced with theme variables. This ensures comprehensive coverage
 * of the theming system migration.
 *
 * Usage: node scripts/audit-colors.js
 */

const fs = require('fs');
const path = require('path');

// Configuration
const FRONTEND_DIR = path.join(__dirname, '../frontend/src');
const OUTPUT_FILE = path.join(__dirname, '../docs/color-audit-report.md');

// Color patterns to detect
const COLOR_PATTERNS = [
  // Tailwind color classes (cyan, blue, purple, etc. - not green)
  {
    name: 'Tailwind Cyan Classes',
    regex: /\b(text|bg|border)-cyan-\d{2,3}\b/g,
    shouldReplace: true,
    replacement: 'Use text-brand-green, bg-brand-green, or border-brand-green'
  },
  {
    name: 'Tailwind Blue Classes',
    regex: /\b(text|bg|border)-blue-\d{2,3}\b/g,
    shouldReplace: true,
    replacement: 'Use semantic colors (text-primary, bg-surface, etc.)'
  },
  {
    name: 'Tailwind Purple Classes',
    regex: /\b(text|bg|border)-purple-\d{2,3}\b/g,
    shouldReplace: true,
    replacement: 'Use semantic colors (text-secondary, bg-accent, etc.)'
  },
  {
    name: 'Tailwind Orange Classes',
    regex: /\b(text|bg|border)-orange-\d{2,3}\b/g,
    shouldReplace: false, // May be used for warnings
    replacement: 'Acceptable for warning states, or use text-warning'
  },
  {
    name: 'Tailwind Red Classes',
    regex: /\b(text|bg|border)-red-\d{2,3}\b/g,
    shouldReplace: false, // May be used for errors
    replacement: 'Acceptable for error states, or use text-error'
  },
  {
    name: 'Tailwind Yellow Classes',
    regex: /\b(text|bg|border)-yellow-\d{2,3}\b/g,
    shouldReplace: false, // May be used for warnings
    replacement: 'Acceptable for warning states, or use text-warning'
  },
  {
    name: 'Tailwind Slate/Gray Classes',
    regex: /\b(text|bg|border)-(slate|gray)-\d{2,3}\b/g,
    shouldReplace: true,
    replacement: 'Use semantic colors (text-muted, bg-secondary, border-subtle, etc.)'
  },
  // Hex colors
  {
    name: 'Hex Colors (Cyan/Blue)',
    regex: /#[0-9a-fA-F]{6}\b/g,
    filter: (match) => {
      // Check if it's a cyan/blue shade
      const hex = match.toLowerCase();
      return hex.includes('00d4ff') || hex.includes('00a8cc') || hex.includes('0099cc');
    },
    shouldReplace: true,
    replacement: 'Use #3DB60F (BRAND_GREEN) or CSS variables'
  },
  {
    name: 'Hex Colors (All)',
    regex: /#[0-9a-fA-F]{6}\b/g,
    shouldReplace: true,
    replacement: 'Use CSS variables or semantic color classes'
  },
  // RGB/RGBA colors
  {
    name: 'RGB/RGBA Colors',
    regex: /rgba?\([^)]+\)/g,
    shouldReplace: true,
    replacement: 'Use CSS variables or Tailwind opacity utilities'
  },
  // HSL colors
  {
    name: 'HSL Colors',
    regex: /hsl\([^)]+\)/g,
    shouldReplace: false, // Usually from CSS variables
    replacement: 'Verify using CSS variables from theme system'
  }
];

// Results storage
const results = {
  totalFiles: 0,
  scannedFiles: 0,
  filesWithIssues: 0,
  totalIssues: 0,
  issuesByFile: {},
  issuesByPattern: {},
  summary: {}
};

/**
 * Recursively scan directory for JSX files
 */
function scanDirectory(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      // Skip node_modules, dist, build directories
      if (!['node_modules', 'dist', 'build', '.git'].includes(entry.name)) {
        scanDirectory(fullPath, files);
      }
    } else if (entry.isFile()) {
      // Only scan JSX and TSX files
      if (entry.name.endsWith('.jsx') || entry.name.endsWith('.tsx')) {
        files.push(fullPath);
      }
    }
  }

  return files;
}

/**
 * Scan a file for color patterns
 */
function scanFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  const relativePath = path.relative(FRONTEND_DIR, filePath);

  const fileIssues = [];

  // Check each pattern
  for (const pattern of COLOR_PATTERNS) {
    let match;
    const regex = new RegExp(pattern.regex.source, pattern.regex.flags);

    while ((match = regex.exec(content)) !== null) {
      // Apply filter if exists
      if (pattern.filter && !pattern.filter(match[0])) {
        continue;
      }

      // Find line number
      let lineNumber = 1;
      let charCount = 0;
      for (let i = 0; i < lines.length; i++) {
        charCount += lines[i].length + 1; // +1 for newline
        if (charCount > match.index) {
          lineNumber = i + 1;
          break;
        }
      }

      const issue = {
        pattern: pattern.name,
        match: match[0],
        line: lineNumber,
        lineContent: lines[lineNumber - 1].trim(),
        shouldReplace: pattern.shouldReplace,
        replacement: pattern.replacement
      };

      fileIssues.push(issue);

      // Update pattern statistics
      if (!results.issuesByPattern[pattern.name]) {
        results.issuesByPattern[pattern.name] = {
          count: 0,
          shouldReplace: pattern.shouldReplace,
          files: new Set()
        };
      }
      results.issuesByPattern[pattern.name].count++;
      results.issuesByPattern[pattern.name].files.add(relativePath);
    }
  }

  if (fileIssues.length > 0) {
    results.issuesByFile[relativePath] = fileIssues;
    results.filesWithIssues++;
    results.totalIssues += fileIssues.length;
  }
}

/**
 * Generate markdown report
 */
function generateReport() {
  let report = `# Greenstack Color Audit Report\n\n`;
  report += `Generated: ${new Date().toISOString()}\n\n`;

  // Executive Summary
  report += `## Executive Summary\n\n`;
  report += `- **Total Files Scanned:** ${results.scannedFiles}\n`;
  report += `- **Files with Issues:** ${results.filesWithIssues}\n`;
  report += `- **Total Color Issues Found:** ${results.totalIssues}\n`;
  report += `- **Files Clean:** ${results.scannedFiles - results.filesWithIssues}\n\n`;

  // Issues by Pattern
  report += `## Issues by Pattern\n\n`;
  report += `| Pattern | Count | Files | Requires Replacement | Recommendation |\n`;
  report += `|---------|-------|-------|---------------------|----------------|\n`;

  for (const [patternName, data] of Object.entries(results.issuesByPattern)) {
    const shouldReplace = data.shouldReplace ? '✅ Yes' : '⚠️  Review';
    const pattern = COLOR_PATTERNS.find(p => p.name === patternName);
    report += `| ${patternName} | ${data.count} | ${data.files.size} | ${shouldReplace} | ${pattern.replacement} |\n`;
  }
  report += `\n`;

  // Priority Files (most issues)
  report += `## Priority Files for Migration\n\n`;
  const sortedFiles = Object.entries(results.issuesByFile)
    .sort((a, b) => b[1].length - a[1].length)
    .slice(0, 20);

  report += `| File | Issues | Critical Issues |\n`;
  report += `|------|--------|----------------|\n`;
  for (const [file, issues] of sortedFiles) {
    const critical = issues.filter(i => i.shouldReplace).length;
    report += `| ${file} | ${issues.length} | ${critical} |\n`;
  }
  report += `\n`;

  // Detailed Issues by File
  report += `## Detailed Issues by File\n\n`;

  for (const [file, issues] of Object.entries(results.issuesByFile)) {
    report += `### ${file}\n\n`;
    report += `Total issues: ${issues.length} (${issues.filter(i => i.shouldReplace).length} require replacement)\n\n`;

    // Group by line
    const lineMap = {};
    for (const issue of issues) {
      if (!lineMap[issue.line]) {
        lineMap[issue.line] = [];
      }
      lineMap[issue.line].push(issue);
    }

    for (const [line, lineIssues] of Object.entries(lineMap)) {
      report += `**Line ${line}:**\n`;
      report += `\`\`\`jsx\n${lineIssues[0].lineContent}\n\`\`\`\n\n`;

      for (const issue of lineIssues) {
        const icon = issue.shouldReplace ? '🔴' : '🟡';
        report += `${icon} **${issue.pattern}**: \`${issue.match}\`\n`;
        report += `   - ${issue.replacement}\n\n`;
      }
    }

    report += `---\n\n`;
  }

  // Recommendations
  report += `## Migration Recommendations\n\n`;
  report += `### Phase 1: Critical Replacements\n\n`;
  report += `Focus on files with hardcoded cyan, blue, and purple colors that should use brand green:\n\n`;

  const criticalFiles = Object.entries(results.issuesByFile)
    .filter(([_, issues]) => issues.some(i => i.shouldReplace && (i.pattern.includes('Cyan') || i.pattern.includes('Blue') || i.pattern.includes('Purple'))))
    .sort((a, b) => b[1].length - a[1].length)
    .slice(0, 10);

  for (const [file, issues] of criticalFiles) {
    const criticalCount = issues.filter(i => i.shouldReplace).length;
    report += `- [ ] **${file}** (${criticalCount} critical issues)\n`;
  }

  report += `\n### Phase 2: Semantic Color Replacements\n\n`;
  report += `Replace gray/slate colors with semantic theme colors:\n\n`;

  const semanticFiles = Object.entries(results.issuesByFile)
    .filter(([_, issues]) => issues.some(i => i.pattern.includes('Slate') || i.pattern.includes('Gray')))
    .sort((a, b) => b[1].length - a[1].length)
    .slice(0, 10);

  for (const [file, issues] of semanticFiles) {
    const semanticCount = issues.filter(i => i.pattern.includes('Slate') || i.pattern.includes('Gray')).length;
    report += `- [ ] **${file}** (${semanticCount} semantic color issues)\n`;
  }

  report += `\n### Phase 3: Hex Color Cleanup\n\n`;
  report += `Replace all hardcoded hex colors with CSS variables:\n\n`;

  const hexFiles = Object.entries(results.issuesByFile)
    .filter(([_, issues]) => issues.some(i => i.pattern.includes('Hex')))
    .sort((a, b) => b[1].length - a[1].length)
    .slice(0, 10);

  for (const [file, issues] of hexFiles) {
    const hexCount = issues.filter(i => i.pattern.includes('Hex')).length;
    report += `- [ ] **${file}** (${hexCount} hex colors)\n`;
  }

  report += `\n## Color Replacement Guide\n\n`;
  report += `### Tailwind Class Replacements\n\n`;
  report += `| Old Class | New Class | Use Case |\n`;
  report += `|-----------|-----------|----------|\n`;
  report += `| \`text-cyan-400\` | \`text-brand-green\` | Brand identity, primary text |\n`;
  report += `| \`text-cyan-500\` | \`text-brand-green\` | Brand identity, primary text |\n`;
  report += `| \`bg-cyan-500\` | \`bg-brand-green\` | Brand backgrounds |\n`;
  report += `| \`border-cyan-500\` | \`border-brand-green\` | Brand borders |\n`;
  report += `| \`text-blue-400\` | \`text-primary\` | Primary interactive elements |\n`;
  report += `| \`text-purple-400\` | \`text-secondary\` or \`text-accent\` | Secondary/accent colors |\n`;
  report += `| \`text-slate-400\` | \`text-muted-foreground\` | Muted text |\n`;
  report += `| \`text-gray-300\` | \`text-foreground-secondary\` | Secondary text |\n`;
  report += `| \`bg-slate-800\` | \`bg-surface\` | Card/surface backgrounds |\n`;
  report += `| \`border-slate-700\` | \`border-border\` | Standard borders |\n\n`;

  report += `### CSS Variable Usage\n\n`;
  report += `\`\`\`jsx\n`;
  report += `// BEFORE\n`;
  report += `<div style={{ color: '#00d4ff' }}>Text</div>\n\n`;
  report += `// AFTER\n`;
  report += `<div style={{ color: 'var(--brand-green)' }}>Text</div>\n`;
  report += `// OR\n`;
  report += `<div className="text-brand-green">Text</div>\n`;
  report += `\`\`\`\n\n`;

  report += `---\n\n`;
  report += `**Next Steps:**\n`;
  report += `1. Review this report and prioritize files for migration\n`;
  report += `2. Use the replacement guide to update components systematically\n`;
  report += `3. Run this audit script after each batch of changes to track progress\n`;
  report += `4. Verify visual appearance in browser after each component migration\n`;

  return report;
}

/**
 * Main execution
 */
function main() {
  console.log('🎨 Greenstack Color Audit Script\n');
  console.log('Scanning for hardcoded colors in JSX components...\n');

  // Scan all JSX files
  const files = scanDirectory(FRONTEND_DIR);
  results.totalFiles = files.length;

  console.log(`Found ${files.length} JSX/TSX files to scan\n`);

  // Scan each file
  for (const file of files) {
    scanFile(file);
    results.scannedFiles++;
  }

  // Generate report
  const report = generateReport();

  // Write to file
  fs.writeFileSync(OUTPUT_FILE, report, 'utf-8');

  // Console summary
  console.log('✅ Audit Complete!\n');
  console.log(`📊 Summary:`);
  console.log(`   - Files scanned: ${results.scannedFiles}`);
  console.log(`   - Files with issues: ${results.filesWithIssues}`);
  console.log(`   - Total issues: ${results.totalIssues}`);
  console.log(`   - Critical replacements needed: ${Object.values(results.issuesByFile).flat().filter(i => i.shouldReplace).length}\n`);
  console.log(`📄 Full report saved to: ${OUTPUT_FILE}\n`);

  // Show top 5 files with most issues
  if (results.filesWithIssues > 0) {
    console.log('🔝 Top files requiring attention:');
    const top5 = Object.entries(results.issuesByFile)
      .sort((a, b) => b[1].length - a[1].length)
      .slice(0, 5);

    for (const [file, issues] of top5) {
      const critical = issues.filter(i => i.shouldReplace).length;
      console.log(`   ${file}: ${issues.length} issues (${critical} critical)`);
    }
  }

  console.log('\n✨ Ready to start migration!\n');
}

// Run the script
main();
