import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Info } from 'lucide-react';

/**
 * ComponentProps - Component Props Documentation Table
 *
 * Features:
 * - Comprehensive props documentation
 * - Type information with syntax highlighting
 * - Required/optional indicators
 * - Default values
 * - Description and examples
 * - Expandable for additional details
 * - TypeScript-style type definitions
 *
 * @param {Object} props
 * @param {Array} props.props - Props array [{name, type, required, default, description, example}]
 * @param {string} props.componentName - Component name for context
 * @param {string} props.className - Additional CSS classes
 */
const ComponentProps = ({ props: propsList = [], componentName, className = '' }) => {
  const [expandedProps, setExpandedProps] = useState(new Set());

  if (!propsList || propsList.length === 0) {
    return (
      <div className={`component-props border border-border rounded-lg p-4 ${className}`}>
        <p className="text-sm text-muted-foreground italic">No props documented</p>
      </div>
    );
  }

  const toggleProp = (propName) => {
    const newExpanded = new Set(expandedProps);
    if (newExpanded.has(propName)) {
      newExpanded.delete(propName);
    } else {
      newExpanded.add(propName);
    }
    setExpandedProps(newExpanded);
  };

  const getTypeColor = (type) => {
    const lowerType = type?.toLowerCase() || '';
    if (lowerType.includes('string')) return 'text-blue-500';
    if (lowerType.includes('number') || lowerType.includes('integer')) return 'text-purple-500';
    if (lowerType.includes('boolean') || lowerType.includes('bool')) return 'text-green-500';
    if (lowerType.includes('function') || lowerType.includes('=>')) return 'text-yellow-500';
    if (lowerType.includes('object') || lowerType.includes('{')) return 'text-orange-500';
    if (lowerType.includes('array') || lowerType.includes('[]')) return 'text-pink-500';
    if (lowerType.includes('node') || lowerType.includes('element')) return 'text-cyan-500';
    return 'text-foreground';
  };

  return (
    <div className={`component-props border border-border rounded-lg overflow-hidden ${className}`}>
      {/* Header */}
      <div className="px-4 py-3 border-b border-border bg-surface/50">
        <h4 className="font-semibold text-foreground flex items-center gap-2">
          <Info className="w-4 h-4 text-brand-green" />
          {componentName ? `${componentName} Props` : 'Props'}
        </h4>
      </div>

      {/* Props List */}
      <div className="divide-y divide-border">
        {propsList.map((prop, index) => {
          const isExpanded = expandedProps.has(prop.name);
          const hasDetails = prop.example || prop.values || prop.notes;

          return (
            <div key={index} className="hover:bg-surface-hover transition-colors">
              {/* Main Row */}
              <div className="px-4 py-3">
                <div className="flex items-start justify-between gap-4">
                  {/* Prop Name & Type */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <code className="text-sm font-mono font-semibold text-brand-green">
                        {prop.name}
                      </code>
                      {prop.required && (
                        <span className="text-xs px-1.5 py-0.5 bg-red-500/10 text-red-500 rounded font-medium">
                          required
                        </span>
                      )}
                      {prop.deprecated && (
                        <span className="text-xs px-1.5 py-0.5 bg-yellow-500/10 text-yellow-500 rounded font-medium">
                          deprecated
                        </span>
                      )}
                    </div>

                    <div className="flex items-center gap-2 mb-2">
                      <code className={`text-xs font-mono ${getTypeColor(prop.type)}`}>
                        {prop.type || 'any'}
                      </code>
                      {prop.default !== undefined && (
                        <>
                          <span className="text-xs text-muted-foreground">•</span>
                          <span className="text-xs text-muted-foreground">
                            default:{' '}
                            <code className="text-brand-green bg-surface px-1 py-0.5 rounded">
                              {typeof prop.default === 'object'
                                ? JSON.stringify(prop.default)
                                : String(prop.default)}
                            </code>
                          </span>
                        </>
                      )}
                    </div>

                    {prop.description && (
                      <p className="text-sm text-muted-foreground">
                        {prop.description}
                      </p>
                    )}
                  </div>

                  {/* Expand Button */}
                  {hasDetails && (
                    <button
                      onClick={() => toggleProp(prop.name)}
                      className="p-1 hover:bg-surface rounded transition-colors flex-shrink-0"
                    >
                      {isExpanded ? (
                        <ChevronDown className="w-4 h-4 text-muted-foreground" />
                      ) : (
                        <ChevronRight className="w-4 h-4 text-muted-foreground" />
                      )}
                    </button>
                  )}
                </div>

                {/* Expanded Details */}
                {isExpanded && hasDetails && (
                  <div className="mt-3 pt-3 border-t border-border space-y-2">
                    {/* Allowed Values */}
                    {prop.values && (
                      <div>
                        <span className="text-xs font-semibold text-foreground">
                          Allowed values:
                        </span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {prop.values.map((value, i) => (
                            <code
                              key={i}
                              className="text-xs text-brand-green bg-surface px-1.5 py-0.5 rounded border border-border"
                            >
                              {String(value)}
                            </code>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Example */}
                    {prop.example && (
                      <div>
                        <span className="text-xs font-semibold text-foreground">
                          Example:
                        </span>
                        <pre className="mt-1 text-xs font-mono text-foreground bg-surface p-2 rounded border border-border overflow-x-auto">
                          <code>{prop.example}</code>
                        </pre>
                      </div>
                    )}

                    {/* Additional Notes */}
                    {prop.notes && (
                      <div>
                        <span className="text-xs font-semibold text-foreground">
                          Notes:
                        </span>
                        <p className="text-xs text-muted-foreground mt-1">
                          {prop.notes}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* TypeScript Interface (Optional) */}
      {componentName && (
        <div className="px-4 py-3 border-t border-border bg-surface/30">
          <details className="group">
            <summary className="cursor-pointer text-xs font-semibold text-foreground flex items-center gap-2">
              <ChevronRight className="w-3 h-3 transition-transform group-open:rotate-90" />
              TypeScript Interface
            </summary>
            <pre className="mt-2 text-xs font-mono text-foreground bg-surface p-3 rounded border border-border overflow-x-auto">
              <code>{generateTypeScriptInterface(componentName, propsList)}</code>
            </pre>
          </details>
        </div>
      )}
    </div>
  );
};

/**
 * Generate TypeScript interface from props list
 */
function generateTypeScriptInterface(componentName, propsList) {
  const lines = [`interface ${componentName}Props {`];

  propsList.forEach(prop => {
    const optional = prop.required ? '' : '?';
    const comment = prop.description ? `  /** ${prop.description} */\n` : '';
    lines.push(`${comment}  ${prop.name}${optional}: ${prop.type || 'any'};`);
  });

  lines.push('}');
  return lines.join('\n');
}

export default ComponentProps;
