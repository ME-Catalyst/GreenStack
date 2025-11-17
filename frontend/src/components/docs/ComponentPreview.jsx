import React, { useState } from 'react';
import { Eye, Code2, Maximize2, Copy, Check } from 'lucide-react';

/**
 * ComponentPreview - Live Component Preview with Code Toggle
 *
 * Features:
 * - Live rendered component preview
 * - Source code view toggle
 * - Fullscreen preview mode
 * - Copy code to clipboard
 * - Responsive preview container
 * - Theme-aware background
 * - Isolated rendering environment
 *
 * @param {Object} props
 * @param {React.ReactNode} props.children - The component to preview
 * @param {string} props.code - Source code for the component
 * @param {string} props.title - Preview title
 * @param {string} props.description - Preview description
 * @param {boolean} props.center - Center the preview content (default: true)
 * @param {string} props.background - Background style: 'default' | 'dots' | 'grid' | 'none'
 * @param {string} props.height - Preview container height (CSS value)
 * @param {string} props.className - Additional CSS classes
 */
const ComponentPreview = ({
  children,
  code,
  title,
  description,
  center = true,
  background = 'default',
  height = 'auto',
  className = ''
}) => {
  const [showCode, setShowCode] = useState(false);
  const [copied, setCopied] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const handleCopyCode = async () => {
    if (!code) return;

    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  const getBackgroundClass = () => {
    switch (background) {
      case 'dots':
        return 'bg-[radial-gradient(circle,_var(--color-border)_1px,_transparent_1px)] bg-[size:20px_20px]';
      case 'grid':
        return 'bg-[linear-gradient(var(--color-border)_1px,_transparent_1px),linear-gradient(90deg,_var(--color-border)_1px,_transparent_1px)] bg-[size:20px_20px]';
      case 'none':
        return '';
      default:
        return 'bg-surface';
    }
  };

  return (
    <div className={`component-preview border border-border rounded-lg overflow-hidden mb-6 ${className}`}>
      {/* Header */}
      {(title || description) && (
        <div className="px-4 py-3 border-b border-border bg-surface/50">
          {title && (
            <h4 className="font-semibold text-foreground mb-1">{title}</h4>
          )}
          {description && (
            <p className="text-sm text-muted-foreground">{description}</p>
          )}
        </div>
      )}

      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-border bg-surface/30">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowCode(!showCode)}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded transition-colors ${
              showCode
                ? 'bg-brand-green text-white'
                : 'bg-surface hover:bg-surface-hover text-foreground'
            }`}
          >
            {showCode ? (
              <>
                <Eye className="w-3.5 h-3.5" />
                Preview
              </>
            ) : (
              <>
                <Code2 className="w-3.5 h-3.5" />
                Code
              </>
            )}
          </button>
        </div>

        <div className="flex items-center gap-2">
          {code && (
            <button
              onClick={handleCopyCode}
              className="p-1.5 hover:bg-surface-hover rounded transition-colors"
              title="Copy code"
            >
              {copied ? (
                <Check className="w-4 h-4 text-brand-green" />
              ) : (
                <Copy className="w-4 h-4 text-muted-foreground" />
              )}
            </button>
          )}
          <button
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="p-1.5 hover:bg-surface-hover rounded transition-colors"
            title="Toggle fullscreen"
          >
            <Maximize2 className="w-4 h-4 text-muted-foreground" />
          </button>
        </div>
      </div>

      {/* Preview / Code View */}
      <div
        className={`${isFullscreen ? 'fixed inset-0 z-50 bg-background' : ''}`}
        style={{ height: isFullscreen ? '100vh' : height }}
      >
        {showCode ? (
          /* Code View */
          <div className="p-4 bg-surface overflow-auto" style={{ height: isFullscreen ? 'calc(100vh - 120px)' : height }}>
            <pre className="text-xs font-mono text-foreground">
              <code>{code}</code>
            </pre>
          </div>
        ) : (
          /* Live Preview */
          <div
            className={`p-8 ${getBackgroundClass()} ${
              center ? 'flex items-center justify-center' : ''
            }`}
            style={{ minHeight: height === 'auto' ? '200px' : height }}
          >
            <div className={isFullscreen ? 'w-full max-w-4xl' : ''}>
              {children}
            </div>
          </div>
        )}

        {/* Fullscreen Close Button */}
        {isFullscreen && (
          <div className="absolute top-4 right-4">
            <button
              onClick={() => setIsFullscreen(false)}
              className="px-4 py-2 bg-surface hover:bg-surface-hover border border-border rounded-lg text-sm font-medium transition-colors"
            >
              Exit Fullscreen
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ComponentPreview;
