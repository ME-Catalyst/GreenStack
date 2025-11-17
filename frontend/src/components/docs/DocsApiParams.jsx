import React from 'react';
import { CheckCircle, XCircle } from 'lucide-react';

/**
 * DocsApiParams - API Parameter Table Component
 *
 * Features:
 * - Responsive parameter table
 * - Type badges with color coding
 * - Required/optional indicators
 * - Default values
 * - Descriptions and constraints
 * - Enum values display
 *
 * @param {Object} props
 * @param {Array} props.params - Parameter array [{name, type, required, description, default, enum, min, max}]
 * @param {string} props.className - Additional CSS classes
 */
const DocsApiParams = ({ params = [], className = '' }) => {
  if (!params || params.length === 0) {
    return null;
  }

  const getTypeColor = (type) => {
    const colors = {
      string: 'bg-blue-500/10 text-blue-500 border-blue-500/30',
      number: 'bg-purple-500/10 text-purple-500 border-purple-500/30',
      integer: 'bg-purple-500/10 text-purple-500 border-purple-500/30',
      boolean: 'bg-green-500/10 text-green-500 border-green-500/30',
      object: 'bg-yellow-500/10 text-yellow-500 border-yellow-500/30',
      array: 'bg-orange-500/10 text-orange-500 border-orange-500/30',
      file: 'bg-pink-500/10 text-pink-500 border-pink-500/30'
    };
    return colors[type?.toLowerCase()] || 'bg-gray-500/10 text-gray-500 border-gray-500/30';
  };

  return (
    <div className={`docs-api-params overflow-x-auto ${className}`}>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border">
            <th className="text-left py-2 px-3 font-semibold text-foreground">
              Name
            </th>
            <th className="text-left py-2 px-3 font-semibold text-foreground">
              Type
            </th>
            <th className="text-left py-2 px-3 font-semibold text-foreground">
              Required
            </th>
            <th className="text-left py-2 px-3 font-semibold text-foreground">
              Description
            </th>
          </tr>
        </thead>
        <tbody>
          {params.map((param, index) => (
            <tr
              key={index}
              className="border-b border-border last:border-0 hover:bg-surface-hover transition-colors"
            >
              {/* Parameter Name */}
              <td className="py-3 px-3 align-top">
                <code className="text-xs font-mono text-brand-green bg-surface px-1.5 py-0.5 rounded">
                  {param.name}
                </code>
              </td>

              {/* Parameter Type */}
              <td className="py-3 px-3 align-top">
                <span
                  className={`inline-flex items-center px-2 py-0.5 text-xs font-semibold rounded border ${getTypeColor(
                    param.type
                  )}`}
                >
                  {param.type || 'any'}
                </span>
                {param.format && (
                  <span className="ml-1 text-xs text-muted-foreground">
                    ({param.format})
                  </span>
                )}
              </td>

              {/* Required Indicator */}
              <td className="py-3 px-3 align-top">
                {param.required ? (
                  <span className="inline-flex items-center gap-1 text-red-500">
                    <CheckCircle className="w-4 h-4" />
                    <span className="text-xs font-semibold">Yes</span>
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 text-muted-foreground">
                    <XCircle className="w-4 h-4" />
                    <span className="text-xs">No</span>
                  </span>
                )}
              </td>

              {/* Description */}
              <td className="py-3 px-3 align-top">
                <div className="space-y-1">
                  {param.description && (
                    <p className="text-muted-foreground">{param.description}</p>
                  )}

                  {/* Default Value */}
                  {param.default !== undefined && (
                    <div className="text-xs">
                      <span className="text-muted-foreground">Default: </span>
                      <code className="text-brand-green bg-surface px-1 py-0.5 rounded">
                        {typeof param.default === 'object'
                          ? JSON.stringify(param.default)
                          : String(param.default)}
                      </code>
                    </div>
                  )}

                  {/* Enum Values */}
                  {param.enum && param.enum.length > 0 && (
                    <div className="text-xs">
                      <span className="text-muted-foreground">Allowed values: </span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {param.enum.map((value, i) => (
                          <code
                            key={i}
                            className="text-brand-green bg-surface px-1.5 py-0.5 rounded border border-border"
                          >
                            {String(value)}
                          </code>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Min/Max Values */}
                  {(param.min !== undefined || param.max !== undefined) && (
                    <div className="text-xs text-muted-foreground">
                      {param.min !== undefined && (
                        <span>Min: {param.min}</span>
                      )}
                      {param.min !== undefined && param.max !== undefined && (
                        <span className="mx-1">•</span>
                      )}
                      {param.max !== undefined && (
                        <span>Max: {param.max}</span>
                      )}
                    </div>
                  )}

                  {/* Pattern */}
                  {param.pattern && (
                    <div className="text-xs">
                      <span className="text-muted-foreground">Pattern: </span>
                      <code className="text-brand-green bg-surface px-1 py-0.5 rounded">
                        {param.pattern}
                      </code>
                    </div>
                  )}

                  {/* Example */}
                  {param.example !== undefined && (
                    <div className="text-xs">
                      <span className="text-muted-foreground">Example: </span>
                      <code className="text-brand-green bg-surface px-1 py-0.5 rounded">
                        {typeof param.example === 'object'
                          ? JSON.stringify(param.example)
                          : String(param.example)}
                      </code>
                    </div>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DocsApiParams;
