import React from 'react';
import { Palette, Lock, Download, Upload, Sparkles, Moon, Sun, Edit, Check } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, Badge } from '../../../components/ui';

export const metadata = {
  id: 'components/theme-system',
  title: 'Theme System',
  description: 'Customize Greenstack appearance with themes, create custom color schemes, and manage your visual preferences',
  category: 'components',
  order: 2,
  keywords: ['theme', 'colors', 'customization', 'branding', 'dark-mode', 'light-mode', 'appearance'],
  lastUpdated: '2025-01-17',
};

export default function ThemeSystem({ onNavigate }) {
  return (
    <DocsPage>
      <DocsHero
        title="Theme System"
        description="Customize Greenstack's appearance with built-in themes and create your own color schemes"
        icon={<Palette className="w-12 h-12 text-brand-green" />}
      />

      {/* Overview */}
      <DocsSection title="Overview" icon={<Palette />}>
        <DocsParagraph>
          Greenstack features a powerful theme system that allows you to customize the application's
          appearance while maintaining brand identity. You can choose from preset themes or create
          your own custom color schemes.
        </DocsParagraph>

        <div className="grid gap-4 md:grid-cols-2 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Palette className="w-4 h-4 text-brand-green" />
                Preset Themes
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-brand-green flex-shrink-0" />
                  <span>Greenstack (Official Dark)</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-brand-green flex-shrink-0" />
                  <span>Greenstack Light</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-brand-green flex-shrink-0" />
                  <span>Midnight Forest (Dark Blue-Green)</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-brand-green flex-shrink-0" />
                  <span>Emerald Dreams (Light Green)</span>
                </li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-brand-green" />
                Custom Themes
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-brand-green flex-shrink-0" />
                  <span>Create unlimited custom themes</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-brand-green flex-shrink-0" />
                  <span>Real-time preview while editing</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-brand-green flex-shrink-0" />
                  <span>Import/Export theme files</span>
                </li>
                <li className="flex items-center gap-2">
                  <Check className="w-4 h-4 text-brand-green flex-shrink-0" />
                  <span>Based on any preset theme</span>
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Brand Identity */}
      <DocsSection title="Brand Identity Protection" icon={<Lock />}>
        <DocsCallout type="warning" title="Locked Brand Color">
          <DocsParagraph>
            The Greenstack brand green (<code>#3DB60F</code>) is <strong>locked across all themes</strong> and
            cannot be modified. This ensures consistent brand identity throughout the application,
            regardless of which theme is active.
          </DocsParagraph>
        </DocsCallout>

        <DocsParagraph className="mt-4">
          While the brand green is immutable, you have full control over:
        </DocsParagraph>

        <div className="grid gap-4 md:grid-cols-3 my-6">
          <Card>
            <CardContent className="pt-6">
              <h4 className="font-semibold text-foreground mb-2">Surface Colors</h4>
              <p className="text-sm text-muted-foreground">
                Background, surface, and container colors for the UI layout
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <h4 className="font-semibold text-foreground mb-2">Accent Colors</h4>
              <p className="text-sm text-muted-foreground">
                Secondary and accent colors for highlights and emphasis
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <h4 className="font-semibold text-foreground mb-2">State Colors</h4>
              <p className="text-sm text-muted-foreground">
                Success, warning, error, and info colors for feedback
              </p>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Accessing Theme Manager */}
      <DocsSection title="Accessing Theme Manager">
        <DocsParagraph>
          The Theme Manager can be accessed from the settings menu in the Greenstack dashboard:
        </DocsParagraph>

        <Card className="my-6">
          <CardContent className="pt-6">
            <ol className="space-y-3">
              <li className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  1
                </div>
                <div>
                  <p className="text-foreground font-medium">Navigate to Settings</p>
                  <p className="text-sm text-muted-foreground">
                    Click the <strong>Settings</strong> icon in the left sidebar
                  </p>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  2
                </div>
                <div>
                  <p className="text-foreground font-medium">Select Appearance Tab</p>
                  <p className="text-sm text-muted-foreground">
                    Click the <strong>Appearance</strong> tab in settings
                  </p>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  3
                </div>
                <div>
                  <p className="text-foreground font-medium">Browse Themes</p>
                  <p className="text-sm text-muted-foreground">
                    View available themes, create custom themes, or import/export
                  </p>
                </div>
              </li>
            </ol>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Using Preset Themes */}
      <DocsSection title="Using Preset Themes" icon={<Palette />}>
        <DocsParagraph>
          Greenstack includes several carefully crafted preset themes that work out of the box:
        </DocsParagraph>

        <div className="space-y-4 my-6">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">Greenstack (Official)</CardTitle>
                <Badge variant="outline" className="border-brand-green text-brand-green">
                  <Moon className="w-3 h-3 mr-1" />
                  Dark
                </Badge>
              </div>
              <CardDescription>The official Greenstack brand theme</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex h-8 rounded-lg overflow-hidden">
                <div className="flex-1" style={{ backgroundColor: '#3DB60F' }} />
                <div className="flex-1" style={{ backgroundColor: '#2d5016' }} />
                <div className="flex-1" style={{ backgroundColor: '#51cf66' }} />
                <div className="flex-1" style={{ backgroundColor: '#0a0e27' }} />
              </div>
              <p className="text-sm text-muted-foreground mt-3">
                Dark mode with rich greens and deep backgrounds. Perfect for extended use.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-base">Greenstack Light</CardTitle>
                <Badge variant="outline">
                  <Sun className="w-3 h-3 mr-1" />
                  Light
                </Badge>
              </div>
              <CardDescription>Light mode variant of the official theme</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex h-8 rounded-lg overflow-hidden">
                <div className="flex-1" style={{ backgroundColor: '#3DB60F' }} />
                <div className="flex-1" style={{ backgroundColor: '#e8f5e9' }} />
                <div className="flex-1" style={{ backgroundColor: '#51cf66' }} />
                <div className="flex-1" style={{ backgroundColor: '#ffffff' }} />
              </div>
              <p className="text-sm text-muted-foreground mt-3">
                Bright and clean design with excellent readability in daylight.
              </p>
            </CardContent>
          </Card>
        </div>

        <DocsParagraph>
          To activate a preset theme:
        </DocsParagraph>

        <ol className="list-decimal list-inside space-y-2 text-foreground ml-4 my-4">
          <li>Browse the available themes in Theme Manager</li>
          <li>Preview the theme by examining the color preview bar</li>
          <li>Click the <strong>Activate</strong> button on your preferred theme</li>
          <li>Theme applies immediately across the entire application</li>
        </ol>
      </DocsSection>

      {/* Creating Custom Themes */}
      <DocsSection title="Creating Custom Themes" icon={<Sparkles />}>
        <DocsParagraph>
          Create your own custom theme to match your preferences or organizational branding:
        </DocsParagraph>

        <Card className="my-6">
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  1
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Create New Theme</h4>
                  <p className="text-sm text-muted-foreground">
                    Click <strong>Create Custom Theme</strong> button in Theme Manager
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  2
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Select Base Theme</h4>
                  <p className="text-sm text-muted-foreground">
                    Choose a preset theme to use as your starting point (Greenstack by default)
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  3
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Customize Colors</h4>
                  <p className="text-sm text-muted-foreground">
                    Use the Theme Editor to adjust colors. Changes preview in real-time.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  4
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Name & Describe</h4>
                  <p className="text-sm text-muted-foreground">
                    Give your theme a descriptive name and add notes about its purpose
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  5
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Save & Activate</h4>
                  <p className="text-sm text-muted-foreground">
                    Save your custom theme and activate it immediately or later
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <DocsCallout type="info" title="Theme Editor Features">
          <ul className="list-disc list-inside space-y-2 text-foreground">
            <li>Color pickers for all customizable colors</li>
            <li>Real-time preview as you make changes</li>
            <li>Light/Dark mode toggle</li>
            <li>Reset to base theme option</li>
            <li>Validation to ensure readable color contrast</li>
          </ul>
        </DocsCallout>
      </DocsSection>

      {/* Import & Export */}
      <DocsSection title="Import & Export Themes" icon={<Download />}>
        <DocsParagraph>
          Share themes with others or backup your custom themes by exporting them as JSON files:
        </DocsParagraph>

        <div className="grid gap-4 md:grid-cols-2 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Download className="w-4 h-4 text-brand-green" />
                Export Theme
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ol className="space-y-2 text-sm text-muted-foreground">
                <li>1. Find the theme you want to export</li>
                <li>2. Click the download icon on the theme card</li>
                <li>3. Theme downloads as <code>.json</code> file</li>
                <li>4. Share or backup the file</li>
              </ol>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Upload className="w-4 h-4 text-brand-green" />
                Import Theme
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ol className="space-y-2 text-sm text-muted-foreground">
                <li>1. Click the <strong>Import</strong> button</li>
                <li>2. Select a theme <code>.json</code> file</li>
                <li>3. Theme is validated and imported</li>
                <li>4. Appears in your custom themes list</li>
              </ol>
            </CardContent>
          </Card>
        </div>

        <DocsParagraph>
          Example theme JSON structure:
        </DocsParagraph>

        <DocsCodeBlock language="json">
{`{
  "name": "My Custom Theme",
  "description": "A personalized theme for my organization",
  "preset_id": "greenstack",
  "mode": "dark",
  "colors": {
    "brand": "#3DB60F",
    "primary": "#3DB60F",
    "secondary": "#2d5016",
    "accent": "#51cf66",
    "background": "#0a0e27",
    "surface": "#1a1f3a",
    "foreground": "#ffffff",
    "success": "#51cf66",
    "warning": "#ffd43b",
    "error": "#ff6b6b",
    "info": "#00d4ff"
  }
}`}
        </DocsCodeBlock>

        <DocsCallout type="warning" title="Import Validation">
          <DocsParagraph>
            When importing a theme, Greenstack automatically validates the brand green color.
            If the imported theme has an incorrect brand color, it will be corrected to the
            official Greenstack green (<code>#3DB60F</code>).
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      {/* Programmatic Usage */}
      <DocsSection title="Programmatic Theme Access" icon={<Edit />}>
        <DocsParagraph>
          Developers can access theme information programmatically through the ThemeContext:
        </DocsParagraph>

        <DocsCodeBlock language="javascript">
{`import { useTheme } from '../contexts/ThemeContext';

function MyComponent() {
  const {
    currentTheme,        // Current active theme object
    setThemePreset,      // Switch to a preset theme
    setCustomTheme,      // Apply custom theme
    availablePresets,    // Array of preset themes
    brandGreen          // Locked brand green color
  } = useTheme();

  const switchToDark = () => {
    setThemePreset('greenstack');
  };

  const switchToLight = () => {
    setThemePreset('greenstack-light');
  };

  return (
    <div>
      <p>Current theme: {currentTheme.name}</p>
      <p>Mode: {currentTheme.mode}</p>
      <button onClick={switchToDark}>Dark Mode</button>
      <button onClick={switchToLight}>Light Mode</button>
    </div>
  );
}`}
        </DocsCodeBlock>
      </DocsSection>

      {/* API Endpoints */}
      <DocsSection title="Theme API Endpoints">
        <DocsParagraph>
          Themes can be managed programmatically through the REST API:
        </DocsParagraph>

        <div className="space-y-4 my-6">
          <Card>
            <CardContent className="pt-6">
              <div className="font-mono text-sm mb-2">
                <Badge variant="outline" className="mr-2">GET</Badge>
                <code>/api/themes</code>
              </div>
              <p className="text-sm text-muted-foreground">
                List all available themes (presets and custom)
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="font-mono text-sm mb-2">
                <Badge variant="outline" className="mr-2">GET</Badge>
                <code>/api/themes/active</code>
              </div>
              <p className="text-sm text-muted-foreground">
                Get currently active theme
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="font-mono text-sm mb-2">
                <Badge variant="outline" className="mr-2">POST</Badge>
                <code>/api/themes/:id/activate</code>
              </div>
              <p className="text-sm text-muted-foreground">
                Activate a specific theme
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="font-mono text-sm mb-2">
                <Badge variant="outline" className="mr-2">POST</Badge>
                <code>/api/themes</code>
              </div>
              <p className="text-sm text-muted-foreground">
                Create a new custom theme
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="font-mono text-sm mb-2">
                <Badge variant="outline" className="mr-2">PUT</Badge>
                <code>/api/themes/:id</code>
              </div>
              <p className="text-sm text-muted-foreground">
                Update an existing custom theme
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="font-mono text-sm mb-2">
                <Badge variant="outline" className="mr-2">DELETE</Badge>
                <code>/api/themes/:id</code>
              </div>
              <p className="text-sm text-muted-foreground">
                Delete a custom theme (presets cannot be deleted)
              </p>
            </CardContent>
          </Card>
        </div>

        <DocsParagraph>
          For full API documentation, see the <DocsLink href="/docs/api/endpoints" external={false} onNavigate={onNavigate}>
          API Endpoints Reference</DocsLink>.
        </DocsParagraph>
      </DocsSection>

      {/* Related Resources */}
      <DocsSection title="Related Resources">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-6">
          <DocsLink href="/docs/components/overview" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Component Gallery</h5>
            <p className="text-sm text-muted-foreground">Explore all UI components</p>
          </DocsLink>

          <DocsLink href="/docs/components/ui-components" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">UI Components</h5>
            <p className="text-sm text-muted-foreground">Component reference and usage</p>
          </DocsLink>

          <DocsLink href="/docs/user-guide/configuration" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Configuration</h5>
            <p className="text-sm text-muted-foreground">Configure application settings</p>
          </DocsLink>

          <DocsLink href="/docs/api/endpoints" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">API Endpoints</h5>
            <p className="text-sm text-muted-foreground">Theme API documentation</p>
          </DocsLink>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
