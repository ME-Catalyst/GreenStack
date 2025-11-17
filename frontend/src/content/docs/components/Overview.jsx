import React from 'react';
import { Package, Palette, Layout, Sparkles } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import { Button } from '../../../components/ui';
import ComponentPreview from '../../../components/docs/ComponentPreview';
import ComponentProps from '../../../components/docs/ComponentProps';
import ComponentVariants from '../../../components/docs/ComponentVariants';

export const metadata = {
  id: 'components/overview',
  title: 'Component Gallery',
  description: 'Comprehensive catalog of all Greenstack UI components with live examples and documentation',
  category: 'components',
  order: 1,
  keywords: ['components', 'ui', 'library', 'design system', 'react'],
  lastUpdated: '2025-01-17',
};

export default function ComponentGalleryOverview() {
  return (
    <DocsPage>
      <DocsHero
        title="Component Gallery"
        description="Comprehensive catalog of all Greenstack UI components with live examples and documentation"
        icon={<Package className="w-12 h-12 text-brand-green" />}
      />

      <DocsSection title="Introduction">
        <DocsParagraph>
          Greenstack includes a comprehensive library of 35+ React components built with modern best practices.
          All components are theme-aware, accessible, and fully customizable to match your needs.
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 my-6">
          <div className="border border-border rounded-lg p-4">
            <Palette className="w-8 h-8 text-brand-green mb-3" />
            <h4 className="font-semibold text-foreground mb-1">Theme System</h4>
            <p className="text-sm text-muted-foreground">
              All components support dark/light modes with the brand green (#3DB60F) color system
            </p>
          </div>

          <div className="border border-border rounded-lg p-4">
            <Layout className="w-8 h-8 text-brand-green mb-3" />
            <h4 className="font-semibold text-foreground mb-1">Responsive Design</h4>
            <p className="text-sm text-muted-foreground">
              Mobile-first design with Tailwind CSS for all screen sizes
            </p>
          </div>

          <div className="border border-border rounded-lg p-4">
            <Sparkles className="w-8 h-8 text-brand-green mb-3" />
            <h4 className="font-semibold text-foreground mb-1">Accessible</h4>
            <p className="text-sm text-muted-foreground">
              ARIA labels, keyboard navigation, and semantic HTML throughout
            </p>
          </div>
        </div>
      </DocsSection>

      <DocsSection title="Component Categories">
        <DocsParagraph>
          Our component library is organized into the following categories:
        </DocsParagraph>

        <div className="space-y-4 my-6">
          {/* Base UI Components */}
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h4 className="font-semibold text-foreground mb-1">Base UI Components</h4>
                <code className="text-xs text-muted-foreground">ui.jsx</code>
              </div>
              <span className="text-xs px-2 py-1 bg-brand-green/10 text-brand-green rounded">24 components</span>
            </div>
            <p className="text-sm text-muted-foreground mb-3">
              Foundational UI elements including buttons, inputs, dialogs, cards, and more
            </p>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Button</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Input</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Card</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Dialog</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Table</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Tabs</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Badge</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">+17 more</span>
            </div>
          </div>

          {/* Theme Components */}
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h4 className="font-semibold text-foreground mb-1">Theme Components</h4>
                <code className="text-xs text-muted-foreground">Theme*.jsx</code>
              </div>
              <span className="text-xs px-2 py-1 bg-brand-green/10 text-brand-green rounded">4 components</span>
            </div>
            <p className="text-sm text-muted-foreground mb-3">
              Theme customization and management components
            </p>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">ThemeToggle</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">ThemeManager</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">ThemeEditor</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">ColorPicker</span>
            </div>
          </div>

          {/* Documentation Components */}
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h4 className="font-semibold text-foreground mb-1">Documentation Components</h4>
                <code className="text-xs text-muted-foreground">components/docs/</code>
              </div>
              <span className="text-xs px-2 py-1 bg-brand-green/10 text-brand-green rounded">22 components</span>
            </div>
            <p className="text-sm text-muted-foreground mb-3">
              Specialized components for creating rich documentation experiences
            </p>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">DocsPage</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">ComponentPreview</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">DocsApiEndpoint</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">DocsCodeBlock</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">+18 more</span>
            </div>
          </div>

          {/* Feature Components */}
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h4 className="font-semibold text-foreground mb-1">Feature Components</h4>
                <code className="text-xs text-muted-foreground">components/</code>
              </div>
              <span className="text-xs px-2 py-1 bg-brand-green/10 text-brand-green rounded">11 components</span>
            </div>
            <p className="text-sm text-muted-foreground mb-3">
              Application-specific feature components for EDS, services, analytics, and more
            </p>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">AnalyticsDashboard</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">EDSDetailsView</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">MqttManager</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">GrafanaManager</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">+7 more</span>
            </div>
          </div>
        </div>
      </DocsSection>

      <DocsSection title="Interactive Example">
        <DocsParagraph>
          Here's a live example of the Button component using our documentation system:
        </DocsParagraph>

        <ComponentPreview
          title="Button Component"
          description="Primary action button with brand green styling"
          code={`<Button className="bg-brand-green hover:bg-brand-green/90 text-white">
  Click Me
</Button>`}
        >
          <Button className="bg-brand-green hover:bg-brand-green/90 text-white">
            Click Me
          </Button>
        </ComponentPreview>

        <ComponentProps
          componentName="Button"
          props={[
            {
              name: 'children',
              type: 'React.ReactNode',
              required: true,
              description: 'Button content'
            },
            {
              name: 'variant',
              type: "'default' | 'outline' | 'ghost' | 'destructive'",
              required: false,
              default: 'default',
              description: 'Button style variant',
              values: ['default', 'outline', 'ghost', 'destructive']
            },
            {
              name: 'size',
              type: "'sm' | 'md' | 'lg'",
              required: false,
              default: 'md',
              description: 'Button size',
              values: ['sm', 'md', 'lg']
            },
            {
              name: 'disabled',
              type: 'boolean',
              required: false,
              default: false,
              description: 'Disable the button'
            },
            {
              name: 'onClick',
              type: '(event: MouseEvent) => void',
              required: false,
              description: 'Click handler function'
            },
            {
              name: 'className',
              type: 'string',
              required: false,
              description: 'Additional CSS classes'
            }
          ]}
        />

        <ComponentVariants
          title="Button Variants"
          layout="grid"
          columns={2}
          variants={[
            {
              label: 'Default',
              description: 'Standard button with brand green background',
              component: <Button className="bg-brand-green hover:bg-brand-green/90 text-white">Default</Button>,
              code: '<Button className="bg-brand-green">Default</Button>',
              useCase: 'Primary actions'
            },
            {
              label: 'Outline',
              description: 'Button with border and no background',
              component: <Button className="border border-brand-green text-brand-green hover:bg-brand-green/10">Outline</Button>,
              code: '<Button className="border border-brand-green text-brand-green">Outline</Button>',
              useCase: 'Secondary actions'
            },
            {
              label: 'Small',
              description: 'Compact button size',
              component: <Button className="bg-brand-green hover:bg-brand-green/90 text-white text-xs px-3 py-1.5">Small</Button>,
              code: '<Button className="text-xs px-3 py-1.5">Small</Button>',
              useCase: 'Compact layouts'
            },
            {
              label: 'Disabled',
              description: 'Non-interactive disabled state',
              component: <Button className="bg-brand-green text-white" disabled>Disabled</Button>,
              code: '<Button disabled>Disabled</Button>',
              useCase: 'Unavailable actions'
            }
          ]}
        />
      </DocsSection>

      <DocsSection title="Design Principles">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
          <DocsCallout type="tip" title="Consistency">
            <DocsParagraph>
              All components follow consistent naming conventions, prop patterns, and styling approaches.
            </DocsParagraph>
          </DocsCallout>

          <DocsCallout type="tip" title="Composability">
            <DocsParagraph>
              Components are designed to work together seamlessly, allowing complex UIs from simple building blocks.
            </DocsParagraph>
          </DocsCallout>

          <DocsCallout type="tip" title="Flexibility">
            <DocsParagraph>
              Extensive customization through props and className support for tailored experiences.
            </DocsParagraph>
          </DocsCallout>

          <DocsCallout type="tip" title="Performance">
            <DocsParagraph>
              Optimized with React best practices including memoization and lazy loading where appropriate.
            </DocsParagraph>
          </DocsCallout>
        </div>
      </DocsSection>

      <DocsSection title="Browse Components">
        <DocsParagraph>
          Explore detailed documentation for each component:
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-6">
          <DocsLink href="/docs/components/button" external={false} className="block border border-border rounded-lg p-3 hover:border-brand-green transition-colors">
            <h4 className="font-semibold text-foreground mb-1">Button</h4>
            <p className="text-sm text-muted-foreground">Interactive button component with variants</p>
          </DocsLink>

          <DocsLink href="/docs/components/card" external={false} className="block border border-border rounded-lg p-3 hover:border-brand-green transition-colors">
            <h4 className="font-semibold text-foreground mb-1">Card</h4>
            <p className="text-sm text-muted-foreground">Container for grouped content</p>
          </DocsLink>

          <DocsLink href="/docs/components/dialog" external={false} className="block border border-border rounded-lg p-3 hover:border-brand-green transition-colors">
            <h4 className="font-semibold text-foreground mb-1">Dialog</h4>
            <p className="text-sm text-muted-foreground">Modal dialog component</p>
          </DocsLink>

          <DocsLink href="/docs/components/theme-manager" external={false} className="block border border-border rounded-lg p-3 hover:border-brand-green transition-colors">
            <h4 className="font-semibold text-foreground mb-1">Theme Manager</h4>
            <p className="text-sm text-muted-foreground">Theme customization interface</p>
          </DocsLink>
        </div>
      </DocsSection>

      <DocsSection title="Usage Guidelines">
        <DocsParagraph>
          When using Greenstack components in your application:
        </DocsParagraph>

        <ol className="list-decimal list-inside space-y-2 text-sm text-foreground my-4">
          <li>Import components from their respective paths</li>
          <li>Always include the ThemeContext provider at your app root</li>
          <li>Use the brand green color (#3DB60F) for primary actions</li>
          <li>Test components in both light and dark themes</li>
          <li>Ensure keyboard navigation works for all interactive elements</li>
          <li>Provide appropriate ARIA labels for accessibility</li>
        </ol>

        <DocsCallout type="info" title="Getting Started">
          <DocsParagraph>
            New to Greenstack components? Start with the <DocsLink href="/docs/getting-started/quick-start" external={false}>Quick Start Guide</DocsLink> to
            learn the basics.
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>
    </DocsPage>
  );
}
