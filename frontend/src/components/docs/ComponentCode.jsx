import React, { useState } from 'react';
import { Code2, Copy, Check, Download, Eye, EyeOff } from 'lucide-react';
import DocsCodeBlock from './DocsCodeBlock';

/**
 * ComponentCode - Component Source Code Display
 *
 * Features:
 * - Display component source code with syntax highlighting
 * - Multiple file/section support (component, styles, types, tests)
 * - Copy and download functionality
 * - Collapsible sections
 * - Line highlighting
 * - Import path display
 *
 * @param {Object} props
 * @param {string} props.code - Main component source code
 * @param {string} props.componentName - Component name
 * @param {string} props.importPath - Import path for the component
 * @param {Object} props.additionalFiles - Additional files {filename: code}
 * @param {Array} props.highlightLines - Lines to highlight
 * @param {boolean} props.showLineNumbers - Show line numbers (default: true)
 * @param {boolean} props.collapsible - Make sections collapsible (default: true)
 * @param {string} props.className - Additional CSS classes
 */
const ComponentCode = ({
  code,
  componentName,
  importPath,
  additionalFiles = {},
  highlightLines = [],
  showLineNumbers = true,
  collapsible = true,
  className = ''
}) => {
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState('component');
  const [collapsedSections, setCollapsedSections] = useState(new Set());

  const handleCopy = async () => {
    const currentCode = activeTab === 'component' ? code : additionalFiles[activeTab];
    if (!currentCode) return;

    try {
      await navigator.clipboard.writeText(currentCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  const handleDownload = () => {
    const currentCode = activeTab === 'component' ? code : additionalFiles[activeTab];
    if (!currentCode) return;

    const extension = activeTab.includes('style') ? '.css' : activeTab.includes('test') ? '.test.jsx' : '.jsx';
    const filename = `${componentName || 'component'}${extension}`;

    const blob = new Blob([currentCode], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  };

  const toggleSection = (section) => {
    const newCollapsed = new Set(collapsedSections);
    if (newCollapsed.has(section)) {
      newCollapsed.delete(section);
    } else {
      newCollapsed.add(section);
    }
    setCollapsedSections(newCollapsed);
  };

  const tabs = [
    { id: 'component', label: 'Component', code },
    ...Object.entries(additionalFiles).map(([name, fileCode]) => ({
      id: name,
      label: name.charAt(0).toUpperCase() + name.slice(1),
      code: fileCode
    }))
  ];

  const currentCode = activeTab === 'component' ? code : additionalFiles[activeTab];

  return (
    <div className={`component-code border border-border rounded-lg overflow-hidden ${className}`}>
      {/* Header */}
      <div className="px-4 py-3 border-b border-border bg-surface/50">
        <div className="flex items-center justify-between">
          <h4 className="font-semibold text-foreground flex items-center gap-2">
            <Code2 className="w-5 h-5 text-brand-green" />
            {componentName ? `${componentName} Source` : 'Source Code'}
          </h4>
          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="p-1.5 hover:bg-surface-hover rounded transition-colors"
              title="Copy code"
            >
              {copied ? (
                <Check className="w-4 h-4 text-brand-green" />
              ) : (
                <Copy className="w-4 h-4 text-muted-foreground" />
              )}
            </button>
            <button
              onClick={handleDownload}
              className="p-1.5 hover:bg-surface-hover rounded transition-colors"
              title="Download file"
            >
              <Download className="w-4 h-4 text-muted-foreground" />
            </button>
          </div>
        </div>

        {/* Import Path */}
        {importPath && (
          <div className="mt-2">
            <code className="text-xs font-mono text-muted-foreground bg-surface px-2 py-1 rounded">
              import {`{${componentName}}`} from '{importPath}'
            </code>
          </div>
        )}
      </div>

      {/* Tabs (if multiple files) */}
      {tabs.length > 1 && (
        <div className="flex items-center gap-1 px-4 py-2 border-b border-border bg-surface/30 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3 py-1.5 text-xs font-medium rounded transition-colors whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-brand-green text-white'
                  : 'bg-surface hover:bg-surface-hover text-foreground'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      )}

      {/* Code Display */}
      <div className="p-4 bg-surface">
        {currentCode ? (
          <DocsCodeBlock
            language="jsx"
            copy={false}
            lineNumbers={showLineNumbers}
          >
            {currentCode}
          </DocsCodeBlock>
        ) : (
          <p className="text-sm text-muted-foreground italic">No code available</p>
        )}
      </div>

      {/* Additional Info */}
      {collapsible && (
        <div className="border-t border-border">
          {/* Usage Example */}
          <details className="group">
            <summary className="px-4 py-3 bg-surface/30 cursor-pointer flex items-center gap-2 hover:bg-surface-hover transition-colors">
              <span className="text-xs font-semibold text-foreground">Usage Example</span>
            </summary>
            <div className="px-4 py-3 border-t border-border">
              <DocsCodeBlock language="jsx" copy>
                {generateUsageExample(componentName, importPath)}
              </DocsCodeBlock>
            </div>
          </details>

          {/* File Structure */}
          <details className="group">
            <summary className="px-4 py-3 bg-surface/30 cursor-pointer flex items-center gap-2 hover:bg-surface-hover transition-colors border-t border-border">
              <span className="text-xs font-semibold text-foreground">File Structure</span>
            </summary>
            <div className="px-4 py-3 border-t border-border">
              <pre className="text-xs font-mono text-foreground">
                {generateFileStructure(componentName, additionalFiles)}
              </pre>
            </div>
          </details>
        </div>
      )}
    </div>
  );
};

/**
 * Generate a basic usage example
 */
function generateUsageExample(componentName, importPath) {
  if (!componentName) return '// No component name provided';

  return `import ${componentName} from '${importPath || `./components/${componentName}`}';

function MyApp() {
  return (
    <${componentName}>
      {/* Your content here */}
    </${componentName}>
  );
}`;
}

/**
 * Generate file structure tree
 */
function generateFileStructure(componentName, additionalFiles) {
  const name = componentName || 'Component';
  const files = [
    `📁 ${name}/`,
    `  📄 ${name}.jsx`,
    ...Object.keys(additionalFiles).map(f => {
      const ext = f.includes('style') ? '.css' : f.includes('test') ? '.test.js' : '.js';
      return `  📄 ${name}${ext}`;
    })
  ];
  return files.join('\n');
}

export default ComponentCode;
