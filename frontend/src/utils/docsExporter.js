/**
 * Documentation Export Utility
 *
 * Exports the entire documentation system as a standalone, offline HTML package.
 * Creates a ZIP file containing all documentation pages with embedded styles and navigation.
 */

import JSZip from 'jszip';
import { docsRegistry } from '../content/docs/index';
import { BRAND_GREEN } from '../config/themes';

/**
 * Extract all computed CSS from the document
 */
function extractInlineStyles() {
  const styles = [];

  // Get all stylesheets
  for (const sheet of document.styleSheets) {
    try {
      if (sheet.cssRules) {
        for (const rule of sheet.cssRules) {
          styles.push(rule.cssText);
        }
      }
    } catch (e) {
      // Cross-origin stylesheets may throw errors
      console.warn('Could not access stylesheet:', e);
    }
  }

  return styles.join('\n');
}

/**
 * Calculate relative path from one page to another
 * @param {string} fromPath - Current page path (e.g., "getting-started/quick-start")
 * @param {string} toPath - Target page path (e.g., "api/overview" or "index")
 * @returns {string} Relative path (e.g., "../api/overview.html" or "installation.html")
 */
function calculateRelativePath(fromPath, toPath) {
  // Handle index page
  if (toPath === 'index') {
    const depth = fromPath.split('/').length;
    return depth === 1 ? 'index.html' : '../'.repeat(depth - 1) + 'index.html';
  }

  const fromParts = fromPath.split('/');
  const toParts = toPath.split('/');

  // Same directory
  if (fromParts.length === toParts.length && fromParts[0] === toParts[0]) {
    return toParts[toParts.length - 1] + '.html';
  }

  // Different directory
  const depth = fromParts.length - 1; // -1 because we don't count the file itself
  const upPath = depth > 0 ? '../'.repeat(depth) : '';
  return upPath + toPath + '.html';
}

/**
 * Generate standalone HTML template
 */
function generateHTMLTemplate(title, content, currentPageId = null) {
  const navigation = Object.entries(docsRegistry)
    .map(([id, page]) => {
      const href = currentPageId ? calculateRelativePath(currentPageId, id) : `${id}.html`;
      return `
      <li class="${currentPageId === id ? 'active' : ''}">
        <a href="${href}">${page.metadata.title}</a>
      </li>
    `;
    }).join('');

  const homeLink = currentPageId ? calculateRelativePath(currentPageId, 'index') : 'index.html';

  return `<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} - Greenstack Documentation</title>
  <style>
    /* Reset and Base Styles */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    :root {
      --brand-green: ${BRAND_GREEN};
      --background: #0a0e27;
      --background-secondary: #151935;
      --surface: #1a1f3a;
      --surface-hover: #2a3050;
      --border: #2a3050;
      --foreground: #e5e7eb;
      --foreground-secondary: #9ca3af;
      --foreground-muted: #6b7280;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      background: var(--background);
      color: var(--foreground);
      line-height: 1.6;
    }

    /* Layout */
    .docs-container {
      display: grid;
      grid-template-columns: 280px 1fr;
      min-height: 100vh;
      max-width: 1800px;
      margin: 0 auto;
    }

    /* Sidebar */
    .docs-sidebar {
      background: var(--background-secondary);
      border-right: 1px solid var(--border);
      padding: 2rem 1rem;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
    }

    .docs-sidebar h2 {
      color: var(--brand-green);
      font-size: 1.5rem;
      margin-bottom: 2rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .docs-sidebar nav ul {
      list-style: none;
    }

    .docs-sidebar nav li {
      margin-bottom: 0.5rem;
    }

    .docs-sidebar nav a {
      color: var(--foreground-secondary);
      text-decoration: none;
      display: block;
      padding: 0.5rem 0.75rem;
      border-radius: 0.375rem;
      transition: all 0.2s;
      font-size: 0.875rem;
    }

    .docs-sidebar nav a:hover {
      color: var(--foreground);
      background: var(--surface-hover);
    }

    .docs-sidebar nav li.active a {
      color: var(--brand-green);
      background: rgba(61, 182, 15, 0.1);
      font-weight: 500;
    }

    /* Content */
    .docs-content {
      padding: 3rem;
      max-width: 900px;
    }

    .docs-content h1 {
      font-size: 2.5rem;
      color: var(--foreground);
      margin-bottom: 0.5rem;
    }

    .docs-content h2 {
      font-size: 1.875rem;
      color: var(--foreground);
      margin-top: 3rem;
      margin-bottom: 1rem;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid var(--border);
    }

    .docs-content h3 {
      font-size: 1.5rem;
      color: var(--foreground);
      margin-top: 2rem;
      margin-bottom: 1rem;
    }

    .docs-content p {
      margin-bottom: 1rem;
      color: var(--foreground-secondary);
    }

    .docs-content code {
      background: var(--surface);
      padding: 0.2rem 0.4rem;
      border-radius: 0.25rem;
      font-family: 'Courier New', monospace;
      font-size: 0.875rem;
      color: var(--brand-green);
    }

    .docs-content pre {
      background: var(--surface);
      padding: 1rem;
      border-radius: 0.5rem;
      overflow-x: auto;
      margin: 1rem 0;
      border: 1px solid var(--border);
    }

    .docs-content pre code {
      background: none;
      padding: 0;
      color: var(--foreground);
    }

    .docs-content ul, .docs-content ol {
      margin-left: 1.5rem;
      margin-bottom: 1rem;
      color: var(--foreground-secondary);
    }

    .docs-content li {
      margin-bottom: 0.5rem;
    }

    .docs-content a {
      color: var(--brand-green);
      text-decoration: none;
    }

    .docs-content a:hover {
      text-decoration: underline;
    }

    .docs-content table {
      width: 100%;
      border-collapse: collapse;
      margin: 1rem 0;
    }

    .docs-content th,
    .docs-content td {
      padding: 0.75rem;
      text-align: left;
      border: 1px solid var(--border);
    }

    .docs-content th {
      background: var(--surface);
      font-weight: 600;
    }

    .docs-hero {
      background: linear-gradient(135deg, rgba(61, 182, 15, 0.1) 0%, rgba(10, 14, 39, 0.5) 100%);
      padding: 2rem;
      border-radius: 0.75rem;
      margin-bottom: 2rem;
      border: 1px solid var(--border);
    }

    .docs-hero-title {
      font-size: 2.5rem;
      margin-bottom: 0.5rem;
      color: var(--foreground);
    }

    .docs-hero-description {
      color: var(--foreground-secondary);
      font-size: 1.125rem;
    }

    .docs-section {
      margin-bottom: 3rem;
    }

    .docs-callout {
      padding: 1rem 1.25rem;
      border-radius: 0.5rem;
      margin: 1.5rem 0;
      border-left: 4px solid;
    }

    .docs-callout.info {
      background: rgba(0, 157, 255, 0.1);
      border-color: #009dff;
    }

    .docs-callout.success {
      background: rgba(61, 182, 15, 0.1);
      border-color: var(--brand-green);
    }

    .docs-callout.warning {
      background: rgba(255, 212, 59, 0.1);
      border-color: #ffd43b;
    }

    .docs-callout.error {
      background: rgba(255, 107, 107, 0.1);
      border-color: #ff6b6b;
    }

    /* Cards */
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 0.5rem;
      padding: 1.5rem;
      margin-bottom: 1rem;
    }

    .card-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 1rem;
      margin: 1rem 0;
    }

    /* Badge */
    .badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
      background: var(--brand-green);
      color: #000;
    }

    /* Navigation Footer */
    .docs-navigation {
      display: flex;
      justify-content: space-between;
      margin-top: 4rem;
      padding-top: 2rem;
      border-top: 1px solid var(--border);
    }

    .docs-navigation a {
      display: flex;
      flex-direction: column;
      padding: 1rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 0.5rem;
      text-decoration: none;
      transition: all 0.2s;
      max-width: 45%;
    }

    .docs-navigation a:hover {
      border-color: var(--brand-green);
    }

    .docs-navigation .nav-label {
      font-size: 0.75rem;
      color: var(--foreground-muted);
      text-transform: uppercase;
      margin-bottom: 0.25rem;
    }

    .docs-navigation .nav-title {
      color: var(--foreground);
      font-weight: 500;
    }

    /* Footer */
    .docs-footer {
      margin-top: 4rem;
      padding-top: 2rem;
      border-top: 1px solid var(--border);
      text-align: center;
      color: var(--foreground-muted);
      font-size: 0.875rem;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
      width: 8px;
    }

    ::-webkit-scrollbar-track {
      background: var(--background);
    }

    ::-webkit-scrollbar-thumb {
      background: var(--border);
      border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
      background: var(--surface-hover);
    }

    /* Print Styles */
    @media print {
      .docs-sidebar {
        display: none;
      }

      .docs-container {
        grid-template-columns: 1fr;
      }

      .docs-content {
        max-width: 100%;
      }
    }

    /* Responsive */
    @media (max-width: 768px) {
      .docs-container {
        grid-template-columns: 1fr;
      }

      .docs-sidebar {
        position: static;
        height: auto;
        border-right: none;
        border-bottom: 1px solid var(--border);
      }

      .docs-content {
        padding: 1.5rem;
      }
    }
  </style>
</head>
<body>
  <div class="docs-container">
    <aside class="docs-sidebar">
      <h2>
        <span style="color: var(--brand-green);">📚</span>
        Greenstack Docs
      </h2>
      <nav>
        <ul>
          ${navigation}
        </ul>
      </nav>
      <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--border);">
        <p style="font-size: 0.75rem; color: var(--foreground-muted);">
          Offline Documentation<br/>
          Version 1.0.0
        </p>
      </div>
    </aside>
    <main class="docs-content">
      ${content}
      <footer class="docs-footer">
        <p>Greenstack Documentation • Generated with ❤️ by Claude Code</p>
        <p style="margin-top: 0.5rem;">
          <a href="https://github.com/ME-Catalyst/greenstack" target="_blank">GitHub</a> •
          <a href="${homeLink}">Documentation Home</a>
        </p>
      </footer>
    </main>
  </div>
</body>
</html>`;
}

/**
 * Get enhanced content for specific popular pages
 */
function getEnhancedContent(pageId, metadata) {
  const category = metadata.category || 'general';

  // Enhanced content templates for different page types
  const enhancedTemplates = {
    'api/overview': `
      <div class="docs-section">
        <h2>API Categories</h2>
        <p>The Greenstack API is organized into the following categories:</p>
        <div class="card-grid">
          <div class="card">
            <h3 style="color: var(--brand-green); margin-bottom: 0.5rem;">EDS Files</h3>
            <code style="font-size: 0.75rem; opacity: 0.7;">/api/eds</code>
            <p style="margin-top: 0.5rem; font-size: 0.875rem;">Manage EDS (Electronic Data Sheet) files for EtherNet/IP devices including upload, parsing, and package management.</p>
            <div style="margin-top: 0.5rem;">
              <span class="badge">18 endpoints</span>
            </div>
          </div>
          <div class="card">
            <h3 style="color: var(--brand-green); margin-bottom: 0.5rem;">IODD Files</h3>
            <code style="font-size: 0.75rem; opacity: 0.7;">/api/iodd</code>
            <p style="margin-top: 0.5rem; font-size: 0.875rem;">Upload and manage IODD (IO Device Description) files for IO-Link devices with comprehensive parsing and validation.</p>
            <div style="margin-top: 0.5rem;">
              <span class="badge">24 endpoints</span>
            </div>
          </div>
          <div class="card">
            <h3 style="color: var(--brand-green); margin-bottom: 0.5rem;">Devices</h3>
            <code style="font-size: 0.75rem; opacity: 0.7;">/api/devices</code>
            <p style="margin-top: 0.5rem; font-size: 0.875rem;">Search, filter, and manage device catalog with advanced querying capabilities.</p>
            <div style="margin-top: 0.5rem;">
              <span class="badge">12 endpoints</span>
            </div>
          </div>
          <div class="card">
            <h3 style="color: var(--brand-green); margin-bottom: 0.5rem;">Vendors</h3>
            <code style="font-size: 0.75rem; opacity: 0.7;">/api/vendors</code>
            <p style="margin-top: 0.5rem; font-size: 0.875rem;">Access vendor information, logos, and associated devices.</p>
            <div style="margin-top: 0.5rem;">
              <span class="badge">8 endpoints</span>
            </div>
          </div>
          <div class="card">
            <h3 style="color: var(--brand-green); margin-bottom: 0.5rem;">Admin & Health</h3>
            <code style="font-size: 0.75rem; opacity: 0.7;">/api/admin</code>
            <p style="margin-top: 0.5rem; font-size: 0.875rem;">System administration, health checks, database management, and diagnostics.</p>
            <div style="margin-top: 0.5rem;">
              <span class="badge">32 endpoints</span>
            </div>
          </div>
          <div class="card">
            <h3 style="color: var(--brand-green); margin-bottom: 0.5rem;">Exports</h3>
            <code style="font-size: 0.75rem; opacity: 0.7;">/api/export</code>
            <p style="margin-top: 0.5rem; font-size: 0.875rem;">Export device data to various formats including ESI, DCF, and custom formats.</p>
            <div style="margin-top: 0.5rem;">
              <span class="badge">16 endpoints</span>
            </div>
          </div>
        </div>
      </div>

      <div class="docs-section">
        <h2>Base URL</h2>
        <p>All API endpoints are relative to your Greenstack installation base URL:</p>
        <pre><code># Development
http://localhost:8000

# Production
https://greenstack.yourdomain.com</code></pre>
      </div>

      <div class="docs-section">
        <h2>Response Format</h2>
        <p>All API responses use JSON format with consistent structure:</p>
        <pre><code>{
  "status": "success",
  "data": { ... },
  "message": "Operation completed successfully"
}</code></pre>
      </div>

      <div class="docs-callout info">
        <h3>📖 Interactive Documentation</h3>
        <p>Visit <code>/docs</code> on your Greenstack instance for interactive Swagger UI documentation with live API testing.</p>
      </div>
    `,
    'getting-started/quick-start': `
      <div class="docs-section">
        <h2>Installation</h2>
        <p>Get Greenstack up and running in just a few minutes:</p>

        <h3>Using pip (Recommended)</h3>
        <pre><code># Install Greenstack
pip install greenstack

# Run the application
greenstack start</code></pre>

        <h3>Using Docker</h3>
        <pre><code># Pull and run
docker run -p 8000:8000 greenstack/greenstack:latest

# Access at http://localhost:8000</code></pre>
      </div>

      <div class="docs-section">
        <h2>First Steps</h2>
        <ol>
          <li><strong>Access the Web Interface</strong> - Navigate to <code>http://localhost:8000</code></li>
          <li><strong>Upload Device Files</strong> - Import IODD or EDS files from the Devices page</li>
          <li><strong>Browse the Catalog</strong> - Explore your device catalog with search and filters</li>
          <li><strong>Export Configurations</strong> - Generate ESI, DCF, or custom configuration files</li>
        </ol>
      </div>

      <div class="docs-callout success">
        <h3>✅ You're Ready!</h3>
        <p>Greenstack is now running. Check out the Features Overview to learn about all capabilities.</p>
      </div>
    `,
    'user-guide/features': `
      <div class="docs-section">
        <h2>Core Features</h2>

        <div class="card">
          <h3 style="color: var(--brand-green); margin-bottom: 0.75rem;">🔌 IO-Link Device Support (IODD)</h3>
          <ul style="margin-left: 1.5rem;">
            <li>Upload and parse IODD XML files with comprehensive validation</li>
            <li>Extract device parameters, datatypes, and communication settings</li>
            <li>Support for IO-Link specifications versions 1.0 through 1.1</li>
            <li>Automatic parameter extraction and indexing</li>
          </ul>
        </div>

        <div class="card">
          <h3 style="color: var(--brand-green); margin-bottom: 0.75rem;">🌐 EtherNet/IP Support (EDS)</h3>
          <ul style="margin-left: 1.5rem;">
            <li>Parse EDS files for Allen-Bradley and ODVA-compliant devices</li>
            <li>Extract assembly information, connection paths, and parameters</li>
            <li>Support for CIP object models and data types</li>
            <li>Module configuration and port mapping</li>
          </ul>
        </div>

        <div class="card">
          <h3 style="color: var(--brand-green); margin-bottom: 0.75rem;">📊 Advanced Search & Filtering</h3>
          <ul style="margin-left: 1.5rem;">
            <li>Full-text search across device names, descriptions, and parameters</li>
            <li>Filter by vendor, device type, protocol, and specifications</li>
            <li>Saved search queries and custom filters</li>
            <li>Sort by relevance, date, or custom criteria</li>
          </ul>
        </div>

        <div class="card">
          <h3 style="color: var(--brand-green); margin-bottom: 0.75rem;">📦 Multi-Format Export</h3>
          <ul style="margin-left: 1.5rem;">
            <li>ESI (EtherCAT Slave Information) file generation</li>
            <li>DCF (Device Configuration File) export for CANopen</li>
            <li>Custom JSON/XML export formats</li>
            <li>Batch export capabilities</li>
          </ul>
        </div>
      </div>

      <div class="docs-section">
        <h2>Web Interface Features</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
          <div class="card">
            <h4 style="color: var(--brand-green);">🎨 Modern Design</h4>
            <p style="font-size: 0.875rem;">Clean, responsive interface with dark mode support and smooth animations</p>
          </div>
          <div class="card">
            <h4 style="color: var(--brand-green);">📱 Mobile Ready</h4>
            <p style="font-size: 0.875rem;">Fully responsive design works on desktop, tablet, and mobile devices</p>
          </div>
          <div class="card">
            <h4 style="color: var(--brand-green);">⚡ Real-time Updates</h4>
            <p style="font-size: 0.875rem;">Live progress tracking for uploads, parsing, and exports</p>
          </div>
          <div class="card">
            <h4 style="color: var(--brand-green);">📈 Analytics Dashboard</h4>
            <p style="font-size: 0.875rem;">Visualize device statistics, parsing success rates, and system health</p>
          </div>
        </div>
      </div>
    `,
    'user-guide/web-interface': `
      <div class="docs-section">
        <h2>Interface Overview</h2>
        <p>The Greenstack web interface provides an intuitive, modern experience for managing your industrial device catalog.</p>

        <div class="card">
          <h3 style="color: var(--brand-green); margin-bottom: 0.75rem;">Main Navigation</h3>
          <ul style="margin-left: 1.5rem;">
            <li><strong>Dashboard</strong> - Overview of system status, recent activity, and key metrics</li>
            <li><strong>Devices</strong> - Browse and search your complete device catalog</li>
            <li><strong>Upload</strong> - Import new IODD and EDS files</li>
            <li><strong>Export</strong> - Generate configuration files in various formats</li>
            <li><strong>Admin</strong> - System administration and diagnostics</li>
            <li><strong>Docs</strong> - Complete documentation and API reference</li>
          </ul>
        </div>

        <div class="card">
          <h3 style="color: var(--brand-green); margin-bottom: 0.75rem;">Device Catalog</h3>
          <p>The device catalog provides powerful search and filtering capabilities:</p>
          <ul style="margin-left: 1.5rem; margin-top: 0.5rem;">
            <li>Grid and list view modes with customizable columns</li>
            <li>Advanced filtering by vendor, protocol, and device type</li>
            <li>Full-text search across all device metadata</li>
            <li>Sortable columns with persistent user preferences</li>
            <li>Quick actions for export, details, and file management</li>
          </ul>
        </div>

        <div class="card">
          <h3 style="color: var(--brand-green); margin-bottom: 0.75rem;">File Upload</h3>
          <p>Drag-and-drop interface for importing device files:</p>
          <ul style="margin-left: 1.5rem; margin-top: 0.5rem;">
            <li>Multi-file upload with progress tracking</li>
            <li>Automatic file type detection (IODD/EDS)</li>
            <li>Real-time parsing status and error reporting</li>
            <li>Batch operations for multiple files</li>
          </ul>
        </div>
      </div>
    `,
    'user-guide/configuration': `
      <div class="docs-section">
        <h2>Environment Variables</h2>
        <p>Configure Greenstack using environment variables in a <code>.env</code> file:</p>

        <h3>Database Configuration</h3>
        <pre><code># Database path (SQLite)
DATABASE_URL=greenstack.db

# Enable debug logging
DEBUG=false</code></pre>

        <h3>Server Configuration</h3>
        <pre><code># Server host and port
HOST=0.0.0.0
PORT=8000

# CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173</code></pre>

        <h3>File Upload Settings</h3>
        <pre><code># Maximum file size (MB)
MAX_UPLOAD_SIZE=50

# Upload directory
UPLOAD_DIR=./uploads</code></pre>
      </div>

      <div class="docs-section">
        <h2>Configuration Examples</h2>

        <div class="card">
          <h3 style="color: var(--brand-green);">Development</h3>
          <pre><code>DEBUG=true
DATABASE_URL=dev.db
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=debug</code></pre>
        </div>

        <div class="card">
          <h3 style="color: var(--brand-green);">Production</h3>
          <pre><code>DEBUG=false
DATABASE_URL=/var/lib/greenstack/greenstack.db
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=info</code></pre>
        </div>
      </div>
    `
  };

  return enhancedTemplates[pageId] || '';
}

/**
 * Convert React component content to simplified HTML
 */
function componentToHTML(pageId, pageData) {
  const { metadata, next, previous } = pageData;
  const enhancedContent = getEnhancedContent(pageId, metadata);

  // Navigation buttons
  const navigationHTML = (next || previous) ? `
    <div class="docs-navigation">
      ${previous ? `
        <a href="${previous.id.split('/')[previous.id.split('/').length - 1]}.html" class="nav-prev">
          <span class="nav-label">Previous</span>
          <span class="nav-title">${previous.title}</span>
        </a>
      ` : '<div></div>'}

      ${next ? `
        <a href="${next.id.split('/')[next.id.split('/').length - 1]}.html" class="nav-next">
          <span class="nav-label">Next</span>
          <span class="nav-title">${next.title}</span>
        </a>
      ` : '<div></div>'}
    </div>
  ` : '';

  return `
    <div class="docs-hero">
      <h1 class="docs-hero-title">${metadata.title}</h1>
      <p class="docs-hero-description">${metadata.description}</p>
    </div>

    ${enhancedContent ? enhancedContent : `
      <div class="docs-callout info">
        <h3>📄 Documentation Page</h3>
        <p>This page contains comprehensive documentation about <strong>${metadata.title}</strong>. For the complete experience with interactive features, code highlighting, and live examples, please visit the Greenstack web application.</p>
      </div>
    `}

    <div class="docs-section">
      <h2>Page Information</h2>
      <div class="card">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
          <div>
            <p style="color: var(--foreground-muted); font-size: 0.875rem; margin-bottom: 0.25rem;">Category</p>
            <p style="font-weight: 600; text-transform: capitalize;">${metadata.category?.replace(/-/g, ' ')}</p>
          </div>
          <div>
            <p style="color: var(--foreground-muted); font-size: 0.875rem; margin-bottom: 0.25rem;">Last Updated</p>
            <p style="font-weight: 600;">${metadata.lastUpdated || 'Recently'}</p>
          </div>
          ${metadata.keywords ? `
            <div style="grid-column: 1 / -1;">
              <p style="color: var(--foreground-muted); font-size: 0.875rem; margin-bottom: 0.5rem;">Keywords</p>
              <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                ${metadata.keywords.map(kw => `<span class="badge">${kw}</span>`).join('')}
              </div>
            </div>
          ` : ''}
        </div>
      </div>
    </div>

    <div class="docs-callout warning">
      <h3>⚡ Interactive Features</h3>
      <p>This static export includes core documentation content. For the full experience, access the live application to enjoy:</p>
      <ul>
        <li>Syntax-highlighted code examples with copy buttons</li>
        <li>Interactive component galleries and demos</li>
        <li>Mermaid diagrams and architecture visualizations</li>
        <li>Real-time search across all documentation</li>
        <li>API endpoint testing with live requests</li>
      </ul>
    </div>

    ${navigationHTML}
  `;
}

/**
 * Generate index page with table of contents
 */
function generateIndexPage() {
  const categories = {};

  // Group pages by category
  Object.entries(docsRegistry).forEach(([id, page]) => {
    const category = page.metadata.category || 'Other';
    if (!categories[category]) {
      categories[category] = [];
    }
    categories[category].push({ id, ...page.metadata });
  });

  const categoryHTML = Object.entries(categories)
    .map(([category, pages]) => `
      <div class="card">
        <h2 style="color: var(--brand-green); margin-bottom: 1rem; text-transform: capitalize;">
          ${category.replace(/-/g, ' ')}
        </h2>
        <ul style="list-style: none; margin: 0;">
          ${pages.map(page => `
            <li style="margin-bottom: 0.75rem;">
              <a href="${page.id}.html" style="color: var(--foreground); font-weight: 500;">
                ${page.title}
              </a>
              <p style="color: var(--foreground-muted); font-size: 0.875rem; margin-top: 0.25rem;">
                ${page.description}
              </p>
            </li>
          `).join('')}
        </ul>
      </div>
    `).join('');

  const content = `
    <div class="docs-hero">
      <h1 class="docs-hero-title">📚 Greenstack Documentation</h1>
      <p class="docs-hero-description">
        Complete offline documentation for the Greenstack industrial device management platform.
        Explore comprehensive guides, API references, and tutorials.
      </p>
    </div>

    <div class="docs-callout info">
      <h3>🌐 Offline Documentation Package</h3>
      <p>You are viewing the static, offline version of Greenstack documentation. This package contains ${Object.keys(docsRegistry).length} documentation pages organized by category.</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div style="text-align: center;">
          <div style="font-size: 1.5rem; color: var(--brand-green); font-weight: bold;">${Object.keys(docsRegistry).length}</div>
          <div style="font-size: 0.75rem; opacity: 0.8;">Total Pages</div>
        </div>
        <div style="text-align: center;">
          <div style="font-size: 1.5rem; color: var(--brand-green); font-weight: bold;">${Object.keys(categories).length}</div>
          <div style="font-size: 0.75rem; opacity: 0.8;">Categories</div>
        </div>
        <div style="text-align: center;">
          <div style="font-size: 1.5rem; color: var(--brand-green); font-weight: bold;">100%</div>
          <div style="font-size: 0.75rem; opacity: 0.8;">Offline Ready</div>
        </div>
      </div>
      <p style="margin-top: 1rem; font-size: 0.875rem;"><strong>Generated:</strong> ${new Date().toLocaleString()}</p>
    </div>

    <div class="docs-section">
      <h2>Documentation Categories</h2>
      <div class="card-grid">
        ${categoryHTML}
      </div>
    </div>

    <div class="docs-section">
      <h2>How to Use This Documentation</h2>
      <div class="card">
        <h3>🔍 Navigation</h3>
        <p>Use the sidebar on the left to browse all documentation pages. Pages are organized by category for easy discovery.</p>
      </div>
      <div class="card">
        <h3>📄 Reading Offline</h3>
        <p>All documentation pages are fully functional offline. You can bookmark specific pages or search using your browser's search function (Ctrl+F).</p>
      </div>
      <div class="card">
        <h3>🖨️ Printing</h3>
        <p>Each page is optimized for printing. Use your browser's print function (Ctrl+P) to create PDF versions of individual pages.</p>
      </div>
    </div>

    <div class="docs-callout warning">
      <h3>⚠️ Limited Interactive Features</h3>
      <p>This static export does not include:</p>
      <ul>
        <li>Live code editors and interactive examples</li>
        <li>3D visualizations and animations</li>
        <li>Real-time API testing</li>
        <li>Search functionality</li>
      </ul>
      <p style="margin-top: 0.75rem;">For the full experience, run the Greenstack application locally or visit the live documentation.</p>
    </div>

    <div class="docs-section">
      <h2>Quick Start</h2>
      <div class="card">
        <h3>🚀 Getting Started</h3>
        <p>New to Greenstack? Start with these essential guides:</p>
        <ol>
          <li><a href="getting-started/quick-start.html">Quick Start Guide</a> - Get up and running in minutes</li>
          <li><a href="getting-started/installation.html">Installation</a> - Complete setup instructions</li>
          <li><a href="user-guide/web-interface.html">Web Interface Guide</a> - Learn the dashboard</li>
          <li><a href="api/overview.html">API Overview</a> - Explore the REST API</li>
        </ol>
      </div>
    </div>

    <div class="docs-section">
      <h2>About Greenstack</h2>
      <p>Greenstack is an intelligent device management platform built on a rock-solid Industrial IoT foundation. It provides comprehensive support for IO-Link (IODD) and EtherNet/IP (EDS) device configurations with a modern web interface.</p>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0;">
        <div style="text-align: center; padding: 1.5rem; background: var(--surface); border-radius: 0.5rem; border: 1px solid var(--border);">
          <div style="font-size: 2.5rem; color: var(--brand-green); margin-bottom: 0.5rem; font-weight: bold;">${Object.keys(docsRegistry).length}</div>
          <div style="color: var(--foreground-muted); font-size: 0.875rem;">Documentation Pages</div>
        </div>
        <div style="text-align: center; padding: 1.5rem; background: var(--surface); border-radius: 0.5rem; border: 1px solid var(--border);">
          <div style="font-size: 2.5rem; color: var(--brand-green); margin-bottom: 0.5rem; font-weight: bold;">142</div>
          <div style="color: var(--foreground-muted); font-size: 0.875rem;">API Endpoints</div>
        </div>
        <div style="text-align: center; padding: 1.5rem; background: var(--surface); border-radius: 0.5rem; border: 1px solid var(--border);">
          <div style="font-size: 2.5rem; color: var(--brand-green); margin-bottom: 0.5rem; font-weight: bold;">8</div>
          <div style="color: var(--foreground-muted); font-size: 0.875rem;">API Categories</div>
        </div>
        <div style="text-align: center; padding: 1.5rem; background: var(--surface); border-radius: 0.5rem; border: 1px solid var(--border);">
          <div style="font-size: 2.5rem; color: var(--brand-green); margin-bottom: 0.5rem; font-weight: bold;">MIT</div>
          <div style="color: var(--foreground-muted); font-size: 0.875rem;">Open Source License</div>
        </div>
      </div>

      <div class="card" style="margin-top: 2rem;">
        <h3 style="margin-bottom: 1rem;">Key Features</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
          <div>
            <p style="font-weight: 600; color: var(--brand-green); margin-bottom: 0.5rem;">📦 Device Management</p>
            <p style="font-size: 0.875rem; color: var(--foreground-secondary);">Upload, parse, and manage IODD and EDS device files with intelligent parsing</p>
          </div>
          <div>
            <p style="font-weight: 600; color: var(--brand-green); margin-bottom: 0.5rem;">🔄 Multi-Format Export</p>
            <p style="font-size: 0.875rem; color: var(--foreground-secondary);">Export to ESI, DCF, and custom configuration formats</p>
          </div>
          <div>
            <p style="font-weight: 600; color: var(--brand-green); margin-bottom: 0.5rem;">🎨 Modern Web UI</p>
            <p style="font-size: 0.875rem; color: var(--foreground-secondary);">Beautiful, responsive interface with dark mode and advanced visualizations</p>
          </div>
          <div>
            <p style="font-weight: 600; color: var(--brand-green); margin-bottom: 0.5rem;">⚡ FastAPI Backend</p>
            <p style="font-size: 0.875rem; color: var(--foreground-secondary);">High-performance async Python API with auto-generated docs</p>
          </div>
        </div>
      </div>
    </div>
  `;

  return generateHTMLTemplate('Documentation Home', content, 'index');
}

/**
 * Main export function
 * Creates a ZIP file with all documentation as standalone HTML
 */
export async function exportDocumentation(onProgress) {
  const zip = new JSZip();
  const totalPages = Object.keys(docsRegistry).length + 1; // +1 for index
  let processed = 0;

  try {
    // Report progress
    const updateProgress = (message) => {
      processed++;
      if (onProgress) {
        onProgress({
          current: processed,
          total: totalPages,
          percentage: Math.round((processed / totalPages) * 100),
          message
        });
      }
    };

    // Generate index.html
    const indexHTML = generateIndexPage();
    zip.file('index.html', indexHTML);
    updateProgress('Generated index page');

    // Generate README
    const readme = `# Greenstack Documentation - Offline Package

This package contains the complete Greenstack documentation exported as static HTML files.

## Contents

- ${Object.keys(docsRegistry).length} documentation pages
- Organized by category
- Fully styled and ready for offline viewing

## How to Use

1. Open \`index.html\` in any web browser
2. Navigate using the sidebar on the left
3. All pages work offline without internet connection

## Features

- ✅ Fully responsive design
- ✅ Dark theme optimized
- ✅ Print-friendly
- ✅ Mobile compatible
- ✅ No external dependencies

## About Greenstack

Greenstack is an intelligent device management platform for Industrial IoT.

- **GitHub**: https://github.com/ME-Catalyst/greenstack
- **Documentation**: Available in the web application
- **License**: MIT

Generated: ${new Date().toLocaleString()}
`;
    zip.file('README.md', readme);
    updateProgress('Generated README');

    // Generate each documentation page
    for (const [pageId, pageData] of Object.entries(docsRegistry)) {
      const pageContent = componentToHTML(pageId, pageData);
      const pageHTML = generateHTMLTemplate(
        pageData.metadata.title,
        pageContent,
        pageId
      );

      zip.file(`${pageId}.html`, pageHTML);
      updateProgress(`Generated ${pageData.metadata.title}`);
    }

    // Generate the ZIP file
    updateProgress('Creating ZIP archive...');
    const blob = await zip.generateAsync({
      type: 'blob',
      compression: 'DEFLATE',
      compressionOptions: { level: 9 }
    });

    // Create download link
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `greenstack-docs-${new Date().toISOString().split('T')[0]}.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    updateProgress('Download complete!');

    return {
      success: true,
      filename: link.download,
      pages: totalPages
    };

  } catch (error) {
    console.error('Error exporting documentation:', error);
    return {
      success: false,
      error: error.message
    };
  }
}

export default exportDocumentation;
