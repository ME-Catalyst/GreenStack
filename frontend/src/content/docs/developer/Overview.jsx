import React from 'react';
import { Code, Book, Wrench, Rocket } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsList, DocsLink } from '../../../components/docs/DocsText';

export const metadata = {
  id: 'developer/overview',
  title: 'Developer Guide',
  description: 'Complete developer guide for building with and contributing to Greenstack',
  category: 'developer',
  order: 1,
  keywords: ['developer', 'development', 'api', 'contributing', 'architecture', 'best practices'],
  lastUpdated: '2025-01-17',
};

export default function DeveloperOverview({ onNavigate }) {
  return (
    <DocsPage>
      <DocsHero
        title="Developer Guide"
        description="Everything you need to build with and contribute to Greenstack"
        icon={<Code className="w-12 h-12 text-brand-green" />}
      />

      <DocsSection title="Welcome Developers">
        <DocsParagraph>
          Whether you're building on top of Greenstack, integrating it into your systems, or contributing to the
          project, this guide will help you get started quickly and follow best practices.
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
          <div className="border border-border rounded-lg p-4">
            <Book className="w-8 h-8 text-brand-green mb-3" />
            <h4 className="font-semibold text-foreground mb-1">API Documentation</h4>
            <p className="text-sm text-muted-foreground mb-3">
              Complete REST API reference with 142 endpoints, request/response examples, and interactive testing.
            </p>
            <DocsLink href="/docs/api/overview" external={false} className="text-sm text-brand-green hover:underline">
              View API Docs →
            </DocsLink>
          </div>

          <div className="border border-border rounded-lg p-4">
            <Wrench className="w-8 h-8 text-brand-green mb-3" />
            <h4 className="font-semibold text-foreground mb-1">Architecture</h4>
            <p className="text-sm text-muted-foreground mb-3">
              System architecture, technology stack, data flow, and design patterns explained in detail.
            </p>
            <DocsLink href="/docs/architecture/overview" external={false} className="text-sm text-brand-green hover:underline">
              View Architecture →
            </DocsLink>
          </div>

          <div className="border border-border rounded-lg p-4">
            <Rocket className="w-8 h-8 text-brand-green mb-3" />
            <h4 className="font-semibold text-foreground mb-1">Deployment</h4>
            <p className="text-sm text-muted-foreground mb-3">
              Production deployment guides for Docker, manual installation, and cloud platforms.
            </p>
            <DocsLink href="/docs/deployment/production-guide" external={false} className="text-sm text-brand-green hover:underline">
              View Deployment →
            </DocsLink>
          </div>

          <div className="border border-border rounded-lg p-4">
            <Code className="w-8 h-8 text-brand-green mb-3" />
            <h4 className="font-semibold text-foreground mb-1">Component Library</h4>
            <p className="text-sm text-muted-foreground mb-3">
              35+ React components with live examples, props documentation, and usage guidelines.
            </p>
            <DocsLink href="/docs/components/overview" external={false} className="text-sm text-brand-green hover:underline">
              View Components →
            </DocsLink>
          </div>
        </div>
      </DocsSection>

      <DocsSection title="Quick Start for Developers">
        <DocsParagraph>
          Get started with Greenstack development in minutes:
        </DocsParagraph>

        <div className="space-y-4 my-6">
          <div className="border-l-4 border-brand-green pl-4 py-2">
            <h5 className="font-semibold text-foreground mb-1">1. Clone and Setup</h5>
            <p className="text-sm text-muted-foreground">
              Clone the repository and install dependencies for both backend and frontend.
            </p>
          </div>

          <div className="border-l-4 border-brand-green pl-4 py-2">
            <h5 className="font-semibold text-foreground mb-1">2. Start Development Servers</h5>
            <p className="text-sm text-muted-foreground">
              Run <code>python start.py</code> to launch both API (port 8000) and frontend (port 3000).
            </p>
          </div>

          <div className="border-l-4 border-brand-green pl-4 py-2">
            <h5 className="font-semibold text-foreground mb-1">3. Explore the API</h5>
            <p className="text-sm text-muted-foreground">
              Visit <code>http://localhost:8000/docs</code> for interactive API documentation.
            </p>
          </div>

          <div className="border-l-4 border-brand-green pl-4 py-2">
            <h5 className="font-semibold text-foreground mb-1">4. Build Something Great</h5>
            <p className="text-sm text-muted-foreground">
              Use the REST API to integrate Greenstack into your applications or contribute improvements.
            </p>
          </div>
        </div>

        <DocsCallout type="tip" title="Development Mode">
          <DocsParagraph>
            Development mode includes auto-reload, detailed error messages, and API documentation at /docs.
            Perfect for rapid development and testing.
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      <DocsSection title="Core Concepts">
        <DocsParagraph>
          Understanding these core concepts will help you work effectively with Greenstack:
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
          <div className="border border-border rounded-lg p-4">
            <h5 className="font-semibold text-foreground mb-2">IODD Files</h5>
            <p className="text-sm text-muted-foreground">
              IO-Link Device Description XML files containing device metadata, parameters, process data, and UI menus.
              Greenstack parses and stores this data for management and configuration.
            </p>
          </div>

          <div className="border border-border rounded-lg p-4">
            <h5 className="font-semibold text-foreground mb-2">REST API</h5>
            <p className="text-sm text-muted-foreground">
              FastAPI-based REST API with automatic validation, OpenAPI documentation, and async support.
              All operations are available via HTTP endpoints.
            </p>
          </div>

          <div className="border border-border rounded-lg p-4">
            <h5 className="font-semibold text-foreground mb-2">Config Schema</h5>
            <p className="text-sm text-muted-foreground">
              Enriched menu structure combining IODD menus with parameter details. Used by the frontend to
              render interactive configuration interfaces.
            </p>
          </div>

          <div className="border border-border rounded-lg p-4">
            <h5 className="font-semibold text-foreground mb-2">Standard Variables</h5>
            <p className="text-sm text-muted-foreground">
              IO-Link defines 19+ standard variables (V_VendorName, V_ProductName, etc.). Greenstack automatically
              enriches these with metadata from the IO-Link specification.
            </p>
          </div>
        </div>
      </DocsSection>

      <DocsSection title="Development Resources">
        <DocsParagraph>
          Comprehensive resources for developers:
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 my-6">
          <DocsLink href="/docs/api/overview" external={false} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">API Reference</h5>
            <p className="text-sm text-muted-foreground">Complete API documentation</p>
          </DocsLink>

          <DocsLink href="/docs/architecture/overview" external={false} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Architecture</h5>
            <p className="text-sm text-muted-foreground">System design and patterns</p>
          </DocsLink>

          <DocsLink href="/docs/components/overview" external={false} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Components</h5>
            <p className="text-sm text-muted-foreground">UI component library</p>
          </DocsLink>

          <DocsLink href="/docs/user-guide/configuration" external={false} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Configuration</h5>
            <p className="text-sm text-muted-foreground">Environment setup</p>
          </DocsLink>

          <DocsLink href="/docs/deployment/production-guide" external={false} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Deployment</h5>
            <p className="text-sm text-muted-foreground">Production deployment</p>
          </DocsLink>

          <DocsLink href="https://github.com/ME-Catalyst/greenstack" external className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">GitHub</h5>
            <p className="text-sm text-muted-foreground">Source code repository</p>
          </DocsLink>
        </div>
      </DocsSection>

      <DocsSection title="Contributing">
        <DocsParagraph>
          We welcome contributions from the community! Here's how you can help:
        </DocsParagraph>

        <DocsCallout type="success" title="Ways to Contribute">
          <DocsList
            items={[
              'Report bugs and issues on GitHub',
              'Suggest new features and enhancements',
              'Improve documentation',
              'Submit pull requests with fixes or features',
              'Share your use cases and success stories',
            ]}
          />
        </DocsCallout>

        <div className="mt-4">
          <DocsLink href="https://github.com/ME-Catalyst/greenstack/issues" external className="text-brand-green hover:underline">
            View open issues on GitHub →
          </DocsLink>
        </div>
      </DocsSection>

      <DocsSection title="Support">
        <DocsParagraph>
          Need help or have questions? We're here to assist:
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
          <div className="border border-border rounded-lg p-4">
            <h5 className="font-semibold text-foreground mb-2">Documentation</h5>
            <p className="text-sm text-muted-foreground mb-3">
              Browse our comprehensive documentation for answers to common questions.
            </p>
            <DocsLink href="/docs/user-guide/troubleshooting" external={false} className="text-sm text-brand-green hover:underline">
              Troubleshooting Guide →
            </DocsLink>
          </div>

          <div className="border border-border rounded-lg p-4">
            <h5 className="font-semibold text-foreground mb-2">GitHub Issues</h5>
            <p className="text-sm text-muted-foreground mb-3">
              Report bugs, request features, or ask technical questions.
            </p>
            <DocsLink href="https://github.com/ME-Catalyst/greenstack/issues" external className="text-sm text-brand-green hover:underline">
              Open an Issue →
            </DocsLink>
          </div>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
