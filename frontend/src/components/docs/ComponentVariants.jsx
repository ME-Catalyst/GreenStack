import React, { useState } from 'react';
import { Layers, Grid3x3 } from 'lucide-react';

/**
 * ComponentVariants - Component Variations Showcase
 *
 * Features:
 * - Display multiple component variations
 * - Grid or list layout
 * - Variant labels and descriptions
 * - Code snippets for each variant
 * - Interactive variant selection
 * - Responsive grid layout
 *
 * @param {Object} props
 * @param {Array} props.variants - Variants array [{label, description, component, code}]
 * @param {string} props.layout - Layout style: 'grid' | 'list'
 * @param {number} props.columns - Number of columns for grid layout (default: 2)
 * @param {string} props.title - Variants section title
 * @param {string} props.className - Additional CSS classes
 */
const ComponentVariants = ({
  variants = [],
  layout = 'grid',
  columns = 2,
  title = 'Variants',
  className = ''
}) => {
  const [selectedVariant, setSelectedVariant] = useState(null);

  if (!variants || variants.length === 0) {
    return null;
  }

  const gridCols = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4'
  };

  return (
    <div className={`component-variants ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h4 className="font-semibold text-foreground flex items-center gap-2">
          <Layers className="w-5 h-5 text-brand-green" />
          {title}
        </h4>
        {variants.length > 1 && (
          <span className="text-xs text-muted-foreground">
            {variants.length} variant{variants.length > 1 ? 's' : ''}
          </span>
        )}
      </div>

      {/* Variants Grid/List */}
      <div
        className={
          layout === 'grid'
            ? `grid ${gridCols[columns] || gridCols[2]} gap-4`
            : 'space-y-4'
        }
      >
        {variants.map((variant, index) => (
          <div
            key={index}
            className="border border-border rounded-lg overflow-hidden hover:border-brand-green transition-colors cursor-pointer"
            onClick={() => setSelectedVariant(selectedVariant === index ? null : index)}
          >
            {/* Variant Preview */}
            <div className="p-6 bg-surface flex items-center justify-center min-h-[120px]">
              {variant.component}
            </div>

            {/* Variant Info */}
            <div className="px-4 py-3 border-t border-border bg-surface/50">
              {variant.label && (
                <h5 className="font-semibold text-sm text-foreground mb-1">
                  {variant.label}
                </h5>
              )}
              {variant.description && (
                <p className="text-xs text-muted-foreground">
                  {variant.description}
                </p>
              )}
            </div>

            {/* Variant Code (Expandable) */}
            {selectedVariant === index && variant.code && (
              <div className="border-t border-border bg-surface-hover">
                <div className="px-4 py-3">
                  <p className="text-xs font-semibold text-foreground mb-2">
                    Code:
                  </p>
                  <pre className="text-xs font-mono text-foreground bg-surface p-3 rounded border border-border overflow-x-auto">
                    <code>{variant.code}</code>
                  </pre>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Quick Comparison View (for grid layout with 2+ variants) */}
      {layout === 'grid' && variants.length >= 2 && (
        <details className="mt-6 border border-border rounded-lg">
          <summary className="px-4 py-3 bg-surface/50 cursor-pointer font-semibold text-sm text-foreground flex items-center gap-2 hover:bg-surface-hover transition-colors">
            <Grid3x3 className="w-4 h-4 text-brand-green" />
            Quick Comparison
          </summary>
          <div className="p-4 border-t border-border">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-2 px-3 font-semibold text-foreground">
                      Variant
                    </th>
                    <th className="text-left py-2 px-3 font-semibold text-foreground">
                      Description
                    </th>
                    <th className="text-left py-2 px-3 font-semibold text-foreground">
                      Use Case
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {variants.map((variant, index) => (
                    <tr key={index} className="border-b border-border last:border-0">
                      <td className="py-2 px-3 font-medium text-foreground">
                        {variant.label || `Variant ${index + 1}`}
                      </td>
                      <td className="py-2 px-3 text-muted-foreground">
                        {variant.description || '-'}
                      </td>
                      <td className="py-2 px-3 text-muted-foreground">
                        {variant.useCase || '-'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </details>
      )}
    </div>
  );
};

export default ComponentVariants;
