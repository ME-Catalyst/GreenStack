import React, { useState, useEffect } from 'react';
import { Save, X, RotateCcw, Eye, Palette } from 'lucide-react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  Button,
  Input,
  Label,
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
  Alert,
  AlertTitle,
  AlertDescription
} from './ui';
import ColorPicker from './ColorPicker';
import { useTheme } from '../contexts/ThemeContext';

/**
 * ThemeEditor Component
 *
 * Comprehensive theme customization interface
 * Allows editing of semantic colors with live preview
 * Brand green is locked and cannot be modified
 */
const ThemeEditor = ({ baseTheme, onSave, onCancel }) => {
  const { brandGreen, applyTheme } = useTheme();
  const [themeName, setThemeName] = useState(baseTheme?.name || 'Custom Theme');
  const [themeDescription, setThemeDescription] = useState(baseTheme?.description || '');
  const [colors, setColors] = useState(baseTheme?.colors || {});
  const [previewMode, setPreviewMode] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);

  useEffect(() => {
    if (baseTheme) {
      setColors(baseTheme.colors);
      setThemeName(baseTheme.name);
      setThemeDescription(baseTheme.description || '');
    }
  }, [baseTheme]);

  const handleColorChange = (colorKey, newValue) => {
    setColors(prev => ({
      ...prev,
      [colorKey]: newValue
    }));
    setHasChanges(true);
  };

  const handlePreview = () => {
    if (!previewMode) {
      // Apply preview
      const previewTheme = {
        ...baseTheme,
        colors: colors
      };
      applyTheme(previewTheme);
      setPreviewMode(true);
    } else {
      // Restore original theme
      applyTheme(baseTheme);
      setPreviewMode(false);
    }
  };

  const handleReset = () => {
    if (confirm('Reset all changes to original theme colors?')) {
      setColors(baseTheme.colors);
      setThemeName(baseTheme.name);
      setThemeDescription(baseTheme.description || '');
      setHasChanges(false);
      if (previewMode) {
        applyTheme(baseTheme);
      }
    }
  };

  const handleSave = () => {
    const customTheme = {
      name: themeName,
      description: themeDescription,
      mode: baseTheme?.mode || 'dark',
      colors: {
        ...colors,
        brand: brandGreen // Ensure brand is always locked
      }
    };

    onSave(customTheme);
  };

  const handleCancel = () => {
    if (previewMode) {
      applyTheme(baseTheme);
    }
    onCancel();
  };

  // Color groups for organization
  const colorGroups = {
    primary: {
      title: 'Primary Colors',
      description: 'Main interactive elements and buttons',
      colors: [
        { key: 'primary', label: 'Primary', description: 'Main brand color for buttons and links' },
        { key: 'primaryHover', label: 'Primary Hover', description: 'Hover state for primary elements' },
        { key: 'primaryActive', label: 'Primary Active', description: 'Active state for primary elements' },
      ]
    },
    secondary: {
      title: 'Secondary Colors',
      description: 'Supporting UI elements',
      colors: [
        { key: 'secondary', label: 'Secondary', description: 'Secondary UI elements' },
        { key: 'secondaryHover', label: 'Secondary Hover', description: 'Hover state' },
        { key: 'secondaryActive', label: 'Secondary Active', description: 'Active state' },
      ]
    },
    accent: {
      title: 'Accent Colors',
      description: 'Highlights and special elements',
      colors: [
        { key: 'accent', label: 'Accent', description: 'Accent color for highlights' },
        { key: 'accentHover', label: 'Accent Hover', description: 'Hover state' },
        { key: 'accentActive', label: 'Accent Active', description: 'Active state' },
      ]
    },
    semantic: {
      title: 'Semantic Colors',
      description: 'Status and feedback colors',
      colors: [
        { key: 'success', label: 'Success', description: 'Success messages and positive actions' },
        { key: 'warning', label: 'Warning', description: 'Warning messages and caution' },
        { key: 'error', label: 'Error', description: 'Error messages and destructive actions' },
        { key: 'info', label: 'Info', description: 'Informational messages' },
      ]
    },
    surfaces: {
      title: 'Surface Colors',
      description: 'Backgrounds and containers',
      colors: [
        { key: 'background', label: 'Background', description: 'Main background color' },
        { key: 'backgroundSecondary', label: 'Background Secondary', description: 'Secondary background' },
        { key: 'surface', label: 'Surface', description: 'Card and panel backgrounds' },
        { key: 'surfaceHover', label: 'Surface Hover', description: 'Hover state for surfaces' },
        { key: 'surfaceActive', label: 'Surface Active', description: 'Active state for surfaces' },
      ]
    },
    borders: {
      title: 'Border Colors',
      description: 'Lines and dividers',
      colors: [
        { key: 'border', label: 'Border', description: 'Default border color' },
        { key: 'borderSubtle', label: 'Border Subtle', description: 'Subtle borders' },
        { key: 'borderStrong', label: 'Border Strong', description: 'Strong emphasis borders' },
      ]
    },
    text: {
      title: 'Text Colors',
      description: 'Typography and content',
      colors: [
        { key: 'foreground', label: 'Foreground', description: 'Primary text color' },
        { key: 'foregroundSecondary', label: 'Foreground Secondary', description: 'Secondary text' },
        { key: 'foregroundMuted', label: 'Foreground Muted', description: 'Muted text and hints' },
        { key: 'foregroundInverse', label: 'Foreground Inverse', description: 'Text on dark backgrounds' },
      ]
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-foreground flex items-center gap-2">
            <Palette className="w-6 h-6 text-brand-green" />
            Theme Editor
          </h2>
          <p className="text-muted-foreground mt-1">
            Customize your theme colors. Brand green is locked and cannot be changed.
          </p>
        </div>
        <div className="flex gap-2">
          <Button onClick={handlePreview} variant="outline">
            <Eye className="w-4 h-4 mr-2" />
            {previewMode ? 'End Preview' : 'Preview'}
          </Button>
          <Button onClick={handleReset} variant="outline" disabled={!hasChanges}>
            <RotateCcw className="w-4 h-4 mr-2" />
            Reset
          </Button>
          <Button onClick={handleCancel} variant="outline">
            <X className="w-4 h-4 mr-2" />
            Cancel
          </Button>
          <Button onClick={handleSave} disabled={!hasChanges}>
            <Save className="w-4 h-4 mr-2" />
            Save Theme
          </Button>
        </div>
      </div>

      {/* Preview Mode Alert */}
      {previewMode && (
        <Alert className="bg-primary/10 border-primary/50">
          <Eye className="w-4 h-4 text-primary" />
          <AlertTitle className="text-primary">Preview Mode Active</AlertTitle>
          <AlertDescription className="text-foreground">
            You are previewing the theme changes. Click "End Preview" to restore the original theme.
          </AlertDescription>
        </Alert>
      )}

      {/* Theme Info */}
      <Card>
        <CardHeader>
          <CardTitle>Theme Information</CardTitle>
          <CardDescription>Name and describe your custom theme</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label>Theme Name</Label>
            <Input
              value={themeName}
              onChange={(e) => {
                setThemeName(e.target.value);
                setHasChanges(true);
              }}
              placeholder="My Custom Theme"
            />
          </div>
          <div>
            <Label>Description</Label>
            <Input
              value={themeDescription}
              onChange={(e) => {
                setThemeDescription(e.target.value);
                setHasChanges(true);
              }}
              placeholder="A brief description of your theme"
            />
          </div>
        </CardContent>
      </Card>

      {/* Brand Color (Locked) */}
      <Card>
        <CardHeader>
          <CardTitle>Brand Identity</CardTitle>
          <CardDescription>Immutable brand color</CardDescription>
        </CardHeader>
        <CardContent>
          <ColorPicker
            label="Brand Green"
            value={brandGreen}
            onChange={() => {}}
            locked={true}
            description="This is the Greenstack brand color and is locked across all themes"
          />
        </CardContent>
      </Card>

      {/* Color Groups */}
      <Tabs defaultValue="primary">
        <TabsList className="grid grid-cols-4 lg:grid-cols-7 gap-2">
          <TabsTrigger value="primary">Primary</TabsTrigger>
          <TabsTrigger value="secondary">Secondary</TabsTrigger>
          <TabsTrigger value="accent">Accent</TabsTrigger>
          <TabsTrigger value="semantic">Semantic</TabsTrigger>
          <TabsTrigger value="surfaces">Surfaces</TabsTrigger>
          <TabsTrigger value="borders">Borders</TabsTrigger>
          <TabsTrigger value="text">Text</TabsTrigger>
        </TabsList>

        {Object.entries(colorGroups).map(([groupKey, group]) => (
          <TabsContent key={groupKey} value={groupKey}>
            <Card>
              <CardHeader>
                <CardTitle>{group.title}</CardTitle>
                <CardDescription>{group.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 gap-6">
                  {group.colors.map(({ key, label, description }) => (
                    <ColorPicker
                      key={key}
                      label={label}
                      value={colors[key] || '#000000'}
                      onChange={(newValue) => handleColorChange(key, newValue)}
                      description={description}
                      showContrast={groupKey === 'text'}
                      backgroundColor={colors.background || '#0a0e27'}
                    />
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        ))}
      </Tabs>

      {/* Action Buttons (Bottom) */}
      <div className="flex justify-end gap-2 pt-4 border-t border-border">
        <Button onClick={handleCancel} variant="outline">
          <X className="w-4 h-4 mr-2" />
          Cancel
        </Button>
        <Button onClick={handleSave} disabled={!hasChanges}>
          <Save className="w-4 h-4 mr-2" />
          Save Theme
        </Button>
      </div>
    </div>
  );
};

export default ThemeEditor;
