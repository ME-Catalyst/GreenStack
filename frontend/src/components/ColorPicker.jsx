import React, { useState } from 'react';
import { Lock } from 'lucide-react';
import { Input, Label } from './ui';

/**
 * ColorPicker Component
 *
 * A color picker with visual preview and hex input
 * Supports locked colors (like brand green) that cannot be changed
 */
const ColorPicker = ({
  label,
  value,
  onChange,
  locked = false,
  description = null,
  showContrast = false,
  backgroundColor = '#ffffff'
}) => {
  const [hexValue, setHexValue] = useState(value);

  const handleColorChange = (e) => {
    const newColor = e.target.value;
    setHexValue(newColor);
    if (!locked) {
      onChange(newColor);
    }
  };

  const handleHexInputChange = (e) => {
    let newHex = e.target.value;

    // Ensure it starts with #
    if (!newHex.startsWith('#')) {
      newHex = '#' + newHex;
    }

    setHexValue(newHex);

    // Validate hex format (3 or 6 digit hex)
    if (/^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(newHex)) {
      if (!locked) {
        onChange(newHex);
      }
    }
  };

  // Calculate contrast ratio for accessibility
  const getContrastRatio = (color1, color2) => {
    const getLuminance = (color) => {
      const hex = color.replace('#', '');
      const r = parseInt(hex.substr(0, 2), 16) / 255;
      const g = parseInt(hex.substr(2, 2), 16) / 255;
      const b = parseInt(hex.substr(4, 2), 16) / 255;

      const [rs, gs, bs] = [r, g, b].map(c => {
        return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
      });

      return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
    };

    const l1 = getLuminance(color1);
    const l2 = getLuminance(color2);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);

    return (lighter + 0.05) / (darker + 0.05);
  };

  const contrastRatio = showContrast ? getContrastRatio(value, backgroundColor) : 0;
  const passesWCAG_AA = contrastRatio >= 4.5;
  const passesWCAG_AAA = contrastRatio >= 7;

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <Label className="text-sm font-medium text-foreground flex items-center gap-2">
          {label}
          {locked && (
            <Lock className="w-3 h-3 text-warning" title="Brand color is locked and cannot be changed" />
          )}
        </Label>
        {locked && (
          <span className="text-xs text-warning">Immutable</span>
        )}
      </div>

      {description && (
        <p className="text-xs text-muted-foreground">{description}</p>
      )}

      <div className="flex gap-3 items-center">
        {/* Visual Color Picker */}
        <div className="relative">
          <input
            type="color"
            value={value}
            onChange={handleColorChange}
            disabled={locked}
            className={`w-16 h-16 rounded-lg border-2 cursor-pointer ${
              locked
                ? 'border-warning opacity-60 cursor-not-allowed'
                : 'border-border hover:border-primary'
            }`}
            style={{
              backgroundColor: value,
            }}
          />
          {locked && (
            <div className="absolute inset-0 flex items-center justify-center bg-black/40 rounded-lg pointer-events-none">
              <Lock className="w-6 h-6 text-white" />
            </div>
          )}
        </div>

        {/* Hex Input */}
        <div className="flex-1">
          <Input
            type="text"
            value={hexValue}
            onChange={handleHexInputChange}
            disabled={locked}
            placeholder="#000000"
            maxLength={7}
            className={`font-mono uppercase ${locked ? 'bg-muted cursor-not-allowed' : ''}`}
          />
        </div>

        {/* Color Preview */}
        <div
          className="w-16 h-16 rounded-lg border-2 border-border"
          style={{ backgroundColor: value }}
          title={`Preview: ${value}`}
        />
      </div>

      {/* Contrast Checker */}
      {showContrast && (
        <div className="mt-2 p-3 bg-secondary/30 rounded-lg border border-border">
          <div className="flex items-center justify-between text-xs">
            <span className="text-muted-foreground">Contrast Ratio:</span>
            <span className="font-mono text-foreground">{contrastRatio.toFixed(2)}:1</span>
          </div>
          <div className="flex gap-2 mt-2">
            <div className={`px-2 py-1 rounded text-xs ${
              passesWCAG_AA ? 'bg-success/20 text-success' : 'bg-error/20 text-error'
            }`}>
              WCAG AA {passesWCAG_AA ? '✓' : '✗'}
            </div>
            <div className={`px-2 py-1 rounded text-xs ${
              passesWCAG_AAA ? 'bg-success/20 text-success' : 'bg-error/20 text-error'
            }`}>
              WCAG AAA {passesWCAG_AAA ? '✓' : '✗'}
            </div>
          </div>
        </div>
      )}

      {locked && (
        <p className="text-xs text-warning mt-2">
          This is the Greenstack brand color and cannot be modified.
        </p>
      )}
    </div>
  );
};

export default ColorPicker;
