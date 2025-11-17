/**
 * Documentation Content Registry
 *
 * Central registry for all documentation pages
 * Provides metadata for navigation, search, and rendering
 *
 * Uses React.lazy for code splitting and performance optimization
 */

import { lazy } from 'react';

// Lazy load all documentation components
const QuickStart = lazy(() => import('./getting-started/QuickStart'));
const Installation = lazy(() => import('./getting-started/Installation'));
const WindowsInstallation = lazy(() => import('./getting-started/WindowsInstallation'));
const DockerSetup = lazy(() => import('./getting-started/DockerSetup'));
const Configuration = lazy(() => import('./user-guide/Configuration'));
const WebInterface = lazy(() => import('./user-guide/WebInterface'));
const Troubleshooting = lazy(() => import('./user-guide/Troubleshooting'));
const ApiOverview = lazy(() => import('./api/Overview'));
const ApiEndpoints = lazy(() => import('./api/Endpoints'));
const ApiAuthentication = lazy(() => import('./api/Authentication'));
const ApiErrors = lazy(() => import('./api/Errors'));
const ComponentsOverview = lazy(() => import('./components/Overview'));
const DeveloperOverview = lazy(() => import('./developer/Overview'));
const BackendDevelopment = lazy(() => import('./developer/Backend'));
const FrontendDevelopment = lazy(() => import('./developer/Frontend'));
const ArchitectureOverview = lazy(() => import('./architecture/Overview'));
const ProductionGuide = lazy(() => import('./deployment/ProductionGuide'));

// Import metadata synchronously (metadata is lightweight)
export { metadata as quickStartMeta } from './getting-started/QuickStart';
export { metadata as installationMeta } from './getting-started/Installation';
export { metadata as windowsInstallationMeta } from './getting-started/WindowsInstallation';
export { metadata as dockerSetupMeta } from './getting-started/DockerSetup';
export { metadata as configurationMeta } from './user-guide/Configuration';
export { metadata as webInterfaceMeta } from './user-guide/WebInterface';
export { metadata as troubleshootingMeta } from './user-guide/Troubleshooting';
export { metadata as apiOverviewMeta } from './api/Overview';
export { metadata as apiEndpointsMeta } from './api/Endpoints';
export { metadata as apiAuthenticationMeta } from './api/Authentication';
export { metadata as apiErrorsMeta } from './api/Errors';
export { metadata as componentsOverviewMeta } from './components/Overview';
export { metadata as developerOverviewMeta } from './developer/Overview';
export { metadata as backendDevelopmentMeta } from './developer/Backend';
export { metadata as frontendDevelopmentMeta } from './developer/Frontend';
export { metadata as architectureOverviewMeta } from './architecture/Overview';
export { metadata as productionGuideMeta } from './deployment/ProductionGuide';

// Import metadata for registry
import { metadata as quickStartMeta } from './getting-started/QuickStart';
import { metadata as installationMeta } from './getting-started/Installation';
import { metadata as windowsInstallationMeta } from './getting-started/WindowsInstallation';
import { metadata as dockerSetupMeta } from './getting-started/DockerSetup';
import { metadata as configurationMeta } from './user-guide/Configuration';
import { metadata as webInterfaceMeta } from './user-guide/WebInterface';
import { metadata as troubleshootingMeta } from './user-guide/Troubleshooting';
import { metadata as apiOverviewMeta } from './api/Overview';
import { metadata as apiEndpointsMeta } from './api/Endpoints';
import { metadata as apiAuthenticationMeta } from './api/Authentication';
import { metadata as apiErrorsMeta } from './api/Errors';
import { metadata as componentsOverviewMeta } from './components/Overview';
import { metadata as developerOverviewMeta } from './developer/Overview';
import { metadata as backendDevelopmentMeta } from './developer/Backend';
import { metadata as frontendDevelopmentMeta } from './developer/Frontend';
import { metadata as architectureOverviewMeta } from './architecture/Overview';
import { metadata as productionGuideMeta } from './deployment/ProductionGuide';

// Documentation Pages Registry
// Format: { 'page-id': { component, metadata, navigation } }
export const docsRegistry = {
  'getting-started/quick-start': {
    component: QuickStart,
    metadata: quickStartMeta,
    next: {
      id: 'getting-started/installation',
      title: 'Installation Guide'
    }
  },

  'getting-started/installation': {
    component: Installation,
    metadata: installationMeta,
    previous: {
      id: 'getting-started/quick-start',
      title: 'Quick Start'
    },
    next: {
      id: 'user-guide/web-interface',
      title: 'Web Interface Guide'
    }
  },

  'getting-started/windows-installation': {
    component: WindowsInstallation,
    metadata: windowsInstallationMeta,
    previous: {
      id: 'getting-started/installation',
      title: 'Installation Guide'
    },
    next: {
      id: 'getting-started/docker',
      title: 'Docker Setup'
    }
  },

  'getting-started/docker': {
    component: DockerSetup,
    metadata: dockerSetupMeta,
    previous: {
      id: 'getting-started/windows-installation',
      title: 'Windows Installation'
    }
  },

  'user-guide/web-interface': {
    component: WebInterface,
    metadata: webInterfaceMeta,
    previous: {
      id: 'getting-started/installation',
      title: 'Installation Guide'
    },
    next: {
      id: 'user-guide/configuration',
      title: 'Configuration Reference'
    }
  },

  'user-guide/configuration': {
    component: Configuration,
    metadata: configurationMeta,
    previous: {
      id: 'user-guide/web-interface',
      title: 'Web Interface Guide'
    },
    next: {
      id: 'user-guide/troubleshooting',
      title: 'Troubleshooting'
    }
  },

  'user-guide/troubleshooting': {
    component: Troubleshooting,
    metadata: troubleshootingMeta,
    previous: {
      id: 'user-guide/configuration',
      title: 'Configuration Reference'
    },
    next: {
      id: 'api/overview',
      title: 'API Overview'
    }
  },

  'api/overview': {
    component: ApiOverview,
    metadata: apiOverviewMeta,
    previous: {
      id: 'user-guide/troubleshooting',
      title: 'Troubleshooting'
    },
    next: {
      id: 'api/endpoints',
      title: 'API Endpoints Reference'
    }
  },

  'api/endpoints': {
    component: ApiEndpoints,
    metadata: apiEndpointsMeta,
    previous: {
      id: 'api/overview',
      title: 'API Overview'
    },
    next: {
      id: 'api/authentication',
      title: 'API Authentication'
    }
  },

  'api/authentication': {
    component: ApiAuthentication,
    metadata: apiAuthenticationMeta,
    previous: {
      id: 'api/endpoints',
      title: 'API Endpoints Reference'
    },
    next: {
      id: 'api/errors',
      title: 'Error Handling'
    }
  },

  'api/errors': {
    component: ApiErrors,
    metadata: apiErrorsMeta,
    previous: {
      id: 'api/authentication',
      title: 'API Authentication'
    },
    next: {
      id: 'components/overview',
      title: 'Component Gallery'
    }
  },

  'components/overview': {
    component: ComponentsOverview,
    metadata: componentsOverviewMeta,
    previous: {
      id: 'api/overview',
      title: 'API Overview'
    },
    next: {
      id: 'developer/overview',
      title: 'Developer Guide'
    }
  },

  'components/gallery': {
    component: null,
    metadata: {
      id: 'components/gallery',
      title: 'Component Gallery',
      description: 'Interactive showcase of all UI components',
      category: 'components',
      keywords: ['components', 'ui', 'library', 'showcase'],
    }
  },

  'components/theme-system': {
    component: null,
    metadata: {
      id: 'components/theme-system',
      title: 'Theme System',
      description: 'Customize Greenstack appearance with themes',
      category: 'components',
      keywords: ['theme', 'colors', 'customization', 'branding'],
    }
  },

  'components/ui-components': {
    component: null,
    metadata: {
      id: 'components/ui-components',
      title: 'UI Components',
      description: 'Reusable UI component reference',
      category: 'components',
      keywords: ['ui', 'components', 'button', 'card', 'dialog'],
    }
  },

  'developer/overview': {
    component: DeveloperOverview,
    metadata: developerOverviewMeta,
    previous: {
      id: 'components/overview',
      title: 'Component Gallery'
    },
    next: {
      id: 'developer/backend',
      title: 'Backend Development'
    }
  },

  'developer/architecture': {
    component: null,
    metadata: {
      id: 'developer/architecture',
      title: 'System Architecture',
      description: 'Greenstack architecture and design',
      category: 'developer',
      keywords: ['architecture', 'design', 'structure', 'system'],
    }
  },

  'developer/backend': {
    component: BackendDevelopment,
    metadata: backendDevelopmentMeta,
    previous: {
      id: 'developer/overview',
      title: 'Developer Guide'
    },
    next: {
      id: 'developer/frontend',
      title: 'Frontend Development'
    }
  },

  'developer/frontend': {
    component: FrontendDevelopment,
    metadata: frontendDevelopmentMeta,
    previous: {
      id: 'developer/backend',
      title: 'Backend Development'
    },
    next: {
      id: 'architecture/overview',
      title: 'System Architecture'
    }
  },

  'developer/testing': {
    component: null,
    metadata: {
      id: 'developer/testing',
      title: 'Testing Guide',
      description: 'Write and run tests for Greenstack',
      category: 'developer',
      keywords: ['testing', 'tests', 'pytest', 'qa'],
    }
  },

  'developer/contributing': {
    component: null,
    metadata: {
      id: 'developer/contributing',
      title: 'Contributing Guide',
      description: 'How to contribute to Greenstack',
      category: 'developer',
      keywords: ['contributing', 'contribute', 'development', 'pull-request'],
    }
  },

  'architecture/overview': {
    component: ArchitectureOverview,
    metadata: architectureOverviewMeta,
    previous: {
      id: 'developer/frontend',
      title: 'Frontend Development'
    },
    next: {
      id: 'deployment/production',
      title: 'Production Deployment'
    }
  },

  'deployment/production': {
    component: ProductionGuide,
    metadata: productionGuideMeta,
    previous: {
      id: 'architecture/overview',
      title: 'System Architecture'
    }
  },

  'deployment/docker': {
    component: null,
    metadata: {
      id: 'deployment/docker',
      title: 'Docker Deployment',
      description: 'Containerized deployment with Docker',
      category: 'deployment',
      keywords: ['docker', 'container', 'deployment', 'compose'],
    }
  },

  'deployment/monitoring': {
    component: null,
    metadata: {
      id: 'deployment/monitoring',
      title: 'Monitoring & Logging',
      description: 'Monitor and debug Greenstack in production',
      category: 'deployment',
      keywords: ['monitoring', 'logging', 'debugging', 'metrics'],
    }
  },

  'troubleshooting/common-issues': {
    component: null,
    metadata: {
      id: 'troubleshooting/common-issues',
      title: 'Common Issues',
      description: 'Solutions to common problems',
      category: 'troubleshooting',
      keywords: ['troubleshooting', 'issues', 'problems', 'solutions'],
    }
  },

  'troubleshooting/debugging': {
    component: null,
    metadata: {
      id: 'troubleshooting/debugging',
      title: 'Debugging Guide',
      description: 'How to debug Greenstack issues',
      category: 'troubleshooting',
      keywords: ['debugging', 'debug', 'troubleshoot', 'logs'],
    }
  },

  'troubleshooting/faq': {
    component: null,
    metadata: {
      id: 'troubleshooting/faq',
      title: 'FAQ',
      description: 'Frequently asked questions',
      category: 'troubleshooting',
      keywords: ['faq', 'questions', 'answers', 'help'],
    }
  },
};

// Export helper functions

/**
 * Get page by ID
 */
export const getPage = (pageId) => {
  return docsRegistry[pageId] || null;
};

/**
 * Get all pages in a category
 */
export const getPagesByCategory = (category) => {
  return Object.entries(docsRegistry)
    .filter(([_, page]) => page.metadata.category === category)
    .map(([id, page]) => ({ id, ...page }));
};

/**
 * Search pages
 */
export const searchPages = (query) => {
  const lowerQuery = query.toLowerCase();
  return Object.entries(docsRegistry)
    .filter(([_, page]) => {
      const { title, description, keywords = [] } = page.metadata;
      return (
        title.toLowerCase().includes(lowerQuery) ||
        description?.toLowerCase().includes(lowerQuery) ||
        keywords.some(k => k.toLowerCase().includes(lowerQuery))
      );
    })
    .map(([id, page]) => ({ id, ...page }));
};

/**
 * Get all categories
 */
export const getCategories = () => {
  const categories = new Set();
  Object.values(docsRegistry).forEach(page => {
    if (page.metadata.category) {
      categories.add(page.metadata.category);
    }
  });
  return Array.from(categories);
};

export default docsRegistry;
