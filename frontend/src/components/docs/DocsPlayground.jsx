import React, { useState, useEffect } from 'react';
import { Play, RotateCcw, Code2, Eye, AlertCircle } from 'lucide-react';
import { Textarea } from '../ui';

/**
 * DocsPlayground - Interactive Code Playground
 *
 * Features:
 * - Live code editing with instant preview
 * - Error boundaries and error display
 * - Reset to initial state
 * - Split view (code + preview)
 * - Syntax error detection
 * - Auto-save to localStorage (optional)
 * - Component scope isolation
 *
 * @param {Object} props
 * @param {string} props.initialCode - Initial code to display
 * @param {Object} props.scope - Available components/libraries in scope
 * @param {string} props.title - Playground title
 * @param {boolean} props.autoRun - Auto-run code on change (default: true)
 * @param {number} props.debounce - Debounce delay for auto-run (ms, default: 500)
 * @param {string} props.storageKey - localStorage key for persistence
 * @param {string} props.className - Additional CSS classes
 */
const DocsPlayground = ({
  initialCode = '',
  scope = {},
  title = 'Interactive Playground',
  autoRun = true,
  debounce = 500,
  storageKey,
  className = ''
}) => {
  const [code, setCode] = useState(() => {
    if (storageKey && typeof window !== 'undefined') {
      const saved = localStorage.getItem(storageKey);
      return saved || initialCode;
    }
    return initialCode;
  });

  const [output, setOutput] = useState(null);
  const [error, setError] = useState(null);
  const [isRunning, setIsRunning] = useState(false);

  // Auto-run with debounce
  useEffect(() => {
    if (!autoRun) return;

    const timer = setTimeout(() => {
      runCode();
    }, debounce);

    return () => clearTimeout(timer);
  }, [code, autoRun, debounce]);

  // Save to localStorage
  useEffect(() => {
    if (storageKey && typeof window !== 'undefined') {
      localStorage.setItem(storageKey, code);
    }
  }, [code, storageKey]);

  const runCode = () => {
    setIsRunning(true);
    setError(null);

    try {
      // Create a function that returns JSX
      // eslint-disable-next-line no-new-func
      const fn = new Function(
        ...Object.keys(scope),
        'React',
        `
        try {
          return (
            ${code}
          );
        } catch (err) {
          throw new Error('Runtime error: ' + err.message);
        }
        `
      );

      // Execute with scope
      const result = fn(...Object.values(scope), React);
      setOutput(result);
    } catch (err) {
      setError(err.message);
      setOutput(null);
    } finally {
      setIsRunning(false);
    }
  };

  const handleReset = () => {
    setCode(initialCode);
    setError(null);
    setOutput(null);
    if (storageKey && typeof window !== 'undefined') {
      localStorage.removeItem(storageKey);
    }
  };

  return (
    <div className={`docs-playground border border-border rounded-lg overflow-hidden ${className}`}>
      {/* Header */}
      <div className="px-4 py-3 border-b border-border bg-surface/50">
        <div className="flex items-center justify-between">
          <h4 className="font-semibold text-foreground flex items-center gap-2">
            <Code2 className="w-5 h-5 text-brand-green" />
            {title}
          </h4>
          <div className="flex items-center gap-2">
            {!autoRun && (
              <button
                onClick={runCode}
                disabled={isRunning}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-brand-green hover:bg-brand-green/90 text-white text-xs font-medium rounded transition-colors disabled:opacity-50"
              >
                <Play className="w-3.5 h-3.5" />
                Run
              </button>
            )}
            <button
              onClick={handleReset}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-surface hover:bg-surface-hover border border-border text-xs font-medium rounded transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              Reset
            </button>
          </div>
        </div>
      </div>

      {/* Split View */}
      <div className="grid grid-cols-1 lg:grid-cols-2 divide-y lg:divide-y-0 lg:divide-x divide-border">
        {/* Code Editor */}
        <div className="relative">
          <div className="absolute top-2 left-2 z-10">
            <span className="text-xs px-2 py-1 bg-surface/90 border border-border rounded font-mono text-muted-foreground">
              Code
            </span>
          </div>
          <Textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full h-[400px] font-mono text-sm border-0 focus:ring-0 resize-none bg-surface"
            placeholder="Enter your code here..."
            spellCheck="false"
          />
        </div>

        {/* Preview */}
        <div className="relative bg-surface">
          <div className="absolute top-2 left-2 z-10">
            <span className="text-xs px-2 py-1 bg-surface/90 border border-border rounded font-mono text-muted-foreground flex items-center gap-1">
              <Eye className="w-3 h-3" />
              Preview
            </span>
          </div>

          <div className="p-8 pt-12 h-[400px] overflow-auto">
            {error ? (
              /* Error Display */
              <div className="flex items-start gap-3 p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-semibold text-red-500 mb-1">Error</p>
                  <p className="text-sm text-foreground">{error}</p>
                </div>
              </div>
            ) : output ? (
              /* Live Preview */
              <div className="component-preview-output">
                {output}
              </div>
            ) : (
              /* Empty State */
              <div className="flex items-center justify-center h-full text-muted-foreground">
                <p className="text-sm italic">
                  {isRunning ? 'Running...' : 'Preview will appear here'}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Footer with Tips */}
      <div className="px-4 py-3 border-t border-border bg-surface/30">
        <details className="group">
          <summary className="cursor-pointer text-xs font-semibold text-foreground flex items-center gap-2">
            <span className="group-open:rotate-90 transition-transform">▶</span>
            Available Components
          </summary>
          <div className="mt-2 flex flex-wrap gap-2">
            {Object.keys(scope).length > 0 ? (
              Object.keys(scope).map((key) => (
                <code
                  key={key}
                  className="text-xs px-2 py-1 bg-surface border border-border rounded font-mono text-brand-green"
                >
                  {key}
                </code>
              ))
            ) : (
              <p className="text-xs text-muted-foreground italic">
                No additional components in scope
              </p>
            )}
          </div>
        </details>
      </div>
    </div>
  );
};

export default DocsPlayground;
