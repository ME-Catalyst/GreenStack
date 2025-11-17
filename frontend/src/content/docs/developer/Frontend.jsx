import React from 'react';
import { Code, Palette, Layers, Zap, Layout, Component, Settings, Rocket } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import DocsTabs, { DocsTab } from '../../../components/docs/DocsTabs';
import DocsAccordion, { DocsAccordionItem } from '../../../components/docs/DocsAccordion';

export const metadata = {
  id: 'developer/frontend',
  title: 'Frontend Development Guide',
  description: 'Comprehensive guide to developing React components, contexts, and hooks for Greenstack',
  category: 'developer',
  order: 4,
  keywords: ['frontend', 'react', 'ui', 'development', 'components', 'hooks', 'context'],
  lastUpdated: '2025-01-17',
};

export default function FrontendDevelopment() {
  return (
    <DocsPage>
      <DocsHero
        title="Frontend Development Guide"
        description="Comprehensive guide to developing React components, contexts, and hooks for Greenstack"
        icon={<Code className="w-12 h-12 text-brand-green" />}
      />

      <DocsSection title="Frontend Architecture">
        <DocsParagraph>
          Greenstack's frontend is built with React 18.2 and follows modern React patterns including hooks,
          context, and functional components. The architecture emphasizes modularity and reusability.
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 my-6">
          <div className="border border-border rounded-lg p-4">
            <Layout className="w-6 h-6 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground">Pages</h4>
            <p className="text-sm text-muted-foreground mt-1">Top-level route components</p>
          </div>

          <div className="border border-border rounded-lg p-4">
            <Component className="w-6 h-6 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground">Components</h4>
            <p className="text-sm text-muted-foreground mt-1">Reusable UI components</p>
          </div>

          <div className="border border-border rounded-lg p-4">
            <Layers className="w-6 h-6 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground">Contexts</h4>
            <p className="text-sm text-muted-foreground mt-1">Global state management</p>
          </div>

          <div className="border border-border rounded-lg p-4">
            <Zap className="w-6 h-6 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground">Hooks</h4>
            <p className="text-sm text-muted-foreground mt-1">Reusable logic</p>
          </div>
        </div>

        <DocsCodeBlock language="plaintext">
{`frontend/src/
├── pages/                # Route-level components
│   ├── Overview.jsx
│   ├── DeviceList.jsx
│   ├── DeviceDetails.jsx
│   └── ...
├── components/          # Reusable components
│   ├── ui/             # Base UI components
│   │   ├── Button.jsx
│   │   ├── Card.jsx
│   │   ├── Dialog.jsx
│   │   └── ...
│   └── docs/           # Documentation components
│       ├── DocsPage.jsx
│       ├── DocsSection.jsx
│       └── ...
├── contexts/           # React contexts
│   └── ThemeContext.jsx
├── hooks/              # Custom hooks
│   └── useKeyboardShortcuts.js
├── config/             # Configuration
│   └── themes.js
└── App.jsx             # Main app component`}
        </DocsCodeBlock>
      </DocsSection>

      <DocsSection title="React Contexts">
        <DocsParagraph>
          Contexts provide global state management across the application without prop drilling.
        </DocsParagraph>

        <DocsAccordion>
          <DocsAccordionItem title="ThemeContext - Theme Management" defaultOpen>
            <DocsParagraph>
              The <code className="text-brand-green">ThemeContext</code> manages application theming including dark/light modes,
              custom themes, and color presets.
            </DocsParagraph>

            <div className="space-y-4 mt-4">
              <div>
                <h5 className="font-semibold text-foreground mb-2">Using ThemeContext</h5>
                <DocsCodeBlock language="jsx" copy>
{`import { useTheme } from '../contexts/ThemeContext';

function MyComponent() {
  const {
    theme,           // Current theme mode: 'light' or 'dark'
    toggleTheme,     // Toggle between light and dark
    currentTheme,    // Full theme object
    themePreset,     // Current preset ID
    setThemePreset,  // Change theme preset
    brandGreen,      // Brand color value
  } = useTheme();

  return (
    <div>
      <p>Current theme: {theme}</p>
      <p>Brand color: {brandGreen}</p>

      <button onClick={toggleTheme}>
        Toggle Theme
      </button>

      <button onClick={() => setThemePreset('ocean')}>
        Switch to Ocean Theme
      </button>
    </div>
  );
}`}
                </DocsCodeBlock>
              </div>

              <div>
                <h5 className="font-semibold text-foreground mb-2">Theme Context API</h5>
                <div className="space-y-2">
                  <div className="border border-border rounded-lg p-3">
                    <code className="text-brand-green font-semibold">theme</code>
                    <p className="text-sm text-muted-foreground mt-1">
                      Current theme mode ('light' or 'dark')
                    </p>
                  </div>

                  <div className="border border-border rounded-lg p-3">
                    <code className="text-brand-green font-semibold">toggleTheme()</code>
                    <p className="text-sm text-muted-foreground mt-1">
                      Toggle between light and dark modes
                    </p>
                  </div>

                  <div className="border border-border rounded-lg p-3">
                    <code className="text-brand-green font-semibold">setTheme(mode)</code>
                    <p className="text-sm text-muted-foreground mt-1">
                      Set theme mode explicitly ('light' or 'dark')
                    </p>
                  </div>

                  <div className="border border-border rounded-lg p-3">
                    <code className="text-brand-green font-semibold">currentTheme</code>
                    <p className="text-sm text-muted-foreground mt-1">
                      Full theme object with all color values
                    </p>
                  </div>

                  <div className="border border-border rounded-lg p-3">
                    <code className="text-brand-green font-semibold">themePreset</code>
                    <p className="text-sm text-muted-foreground mt-1">
                      Current theme preset ID ('greenstack', 'ocean', 'sunset', etc.)
                    </p>
                  </div>

                  <div className="border border-border rounded-lg p-3">
                    <code className="text-brand-green font-semibold">setThemePreset(presetId)</code>
                    <p className="text-sm text-muted-foreground mt-1">
                      Switch to a different theme preset
                    </p>
                  </div>

                  <div className="border border-border rounded-lg p-3">
                    <code className="text-brand-green font-semibold">customTheme</code>
                    <p className="text-sm text-muted-foreground mt-1">
                      User's custom theme (null if using preset)
                    </p>
                  </div>

                  <div className="border border-border rounded-lg p-3">
                    <code className="text-brand-green font-semibold">setCustomTheme(theme)</code>
                    <p className="text-sm text-muted-foreground mt-1">
                      Apply a custom theme configuration
                    </p>
                  </div>

                  <div className="border border-border rounded-lg p-3">
                    <code className="text-brand-green font-semibold">availablePresets</code>
                    <p className="text-sm text-muted-foreground mt-1">
                      Array of all available theme presets
                    </p>
                  </div>
                </div>
              </div>

              <div>
                <h5 className="font-semibold text-foreground mb-2">Creating Custom Themes</h5>
                <DocsCodeBlock language="jsx" copy>
{`import { useTheme } from '../contexts/ThemeContext';

function ThemeCustomizer() {
  const { setCustomTheme } = useTheme();

  const applyCustomTheme = () => {
    const customTheme = {
      id: 'my-theme',
      name: 'My Custom Theme',
      mode: 'dark',
      colors: {
        brand: '#10b981',      // Primary brand color
        background: '#0f172a', // Main background
        surface: '#1e293b',    // Card/panel background
        border: '#334155',     // Border color
        foreground: '#f1f5f9', // Primary text
        muted: '#94a3b8',      // Secondary text
        // ... more colors
      }
    };

    setCustomTheme(customTheme);
  };

  return (
    <button onClick={applyCustomTheme}>
      Apply Custom Theme
    </button>
  );
}`}
                </DocsCodeBlock>
              </div>

              <DocsCallout type="info" title="Theme Persistence">
                <DocsParagraph>
                  ThemeContext automatically saves the selected theme to localStorage and restores it on page load.
                  It also respects the system's color scheme preference if no theme is manually selected.
                </DocsParagraph>
              </DocsCallout>
            </div>
          </DocsAccordionItem>

          <DocsAccordionItem title="Creating New Contexts">
            <DocsParagraph>
              To create a new context for global state management:
            </DocsParagraph>

            <DocsCodeBlock language="jsx" copy>
{`import React, { createContext, useContext, useState, useEffect } from 'react';

// 1. Create the context
const MyContext = createContext({
  data: null,
  loading: false,
  error: null,
  updateData: () => {},
});

// 2. Create a custom hook for easy access
export const useMyContext = () => {
  const context = useContext(MyContext);
  if (!context) {
    throw new Error('useMyContext must be used within MyProvider');
  }
  return context;
};

// 3. Create the provider component
export const MyProvider = ({ children }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Initialize data, fetch from API, etc.
    const initializeData = async () => {
      setLoading(true);
      try {
        const response = await fetch('/api/data');
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    initializeData();
  }, []);

  const updateData = (newData) => {
    setData(newData);
  };

  const value = {
    data,
    loading,
    error,
    updateData,
  };

  return (
    <MyContext.Provider value={value}>
      {children}
    </MyContext.Provider>
  );
};

// 4. Usage in components
function MyComponent() {
  const { data, loading, updateData } = useMyContext();

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <pre>{JSON.stringify(data, null, 2)}</pre>
      <button onClick={() => updateData({ new: 'data' })}>
        Update
      </button>
    </div>
  );
}`}
            </DocsCodeBlock>
          </DocsAccordionItem>
        </DocsAccordion>
      </DocsSection>

      <DocsSection title="Custom Hooks">
        <DocsParagraph>
          Custom hooks encapsulate reusable logic and side effects.
        </DocsParagraph>

        <DocsAccordion>
          <DocsAccordionItem title="useKeyboardShortcuts - Keyboard Shortcuts" defaultOpen>
            <DocsParagraph>
              The <code className="text-brand-green">useKeyboardShortcuts</code> hook provides a centralized system
              for managing keyboard shortcuts across the application.
            </DocsParagraph>

            <DocsCodeBlock language="jsx" copy>
{`import { useKeyboardShortcuts } from '../hooks/useKeyboardShortcuts';

function MyComponent() {
  const shortcuts = [
    {
      key: 's',
      ctrl: true,
      description: 'Save',
      callback: () => {
        console.log('Saving...');
        // Handle save
      }
    },
    {
      key: 'Escape',
      description: 'Close',
      allowInInput: true,  // Allow in input fields
      callback: () => {
        console.log('Closing...');
        // Handle close
      }
    },
    {
      key: 'n',
      ctrl: true,
      shift: true,
      description: 'New Item',
      callback: () => {
        console.log('Creating new item...');
      }
    }
  ];

  // Enable shortcuts
  useKeyboardShortcuts(shortcuts);

  return <div>Press Ctrl+S to save</div>;
}`}
            </DocsCodeBlock>

            <div className="mt-4">
              <h5 className="font-semibold text-foreground mb-2">Shortcut Configuration</h5>
              <div className="space-y-2">
                <div className="border border-border rounded-lg p-3">
                  <code className="text-brand-green font-semibold">key</code>
                  <p className="text-sm text-muted-foreground mt-1">
                    The key to listen for (e.g., 's', 'Enter', 'Escape', 'ArrowUp')
                  </p>
                </div>

                <div className="border border-border rounded-lg p-3">
                  <code className="text-brand-green font-semibold">ctrl</code>
                  <p className="text-sm text-muted-foreground mt-1">
                    Require Ctrl key (or Cmd on Mac)
                  </p>
                </div>

                <div className="border border-border rounded-lg p-3">
                  <code className="text-brand-green font-semibold">shift</code>
                  <p className="text-sm text-muted-foreground mt-1">
                    Require Shift key
                  </p>
                </div>

                <div className="border border-border rounded-lg p-3">
                  <code className="text-brand-green font-semibold">alt</code>
                  <p className="text-sm text-muted-foreground mt-1">
                    Require Alt key
                  </p>
                </div>

                <div className="border border-border rounded-lg p-3">
                  <code className="text-brand-green font-semibold">callback</code>
                  <p className="text-sm text-muted-foreground mt-1">
                    Function to call when shortcut is triggered
                  </p>
                </div>

                <div className="border border-border rounded-lg p-3">
                  <code className="text-brand-green font-semibold">allowInInput</code>
                  <p className="text-sm text-muted-foreground mt-1">
                    Allow shortcut when typing in input fields (default: false)
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-4">
              <h5 className="font-semibold text-foreground mb-2">Predefined Shortcuts</h5>
              <DocsParagraph>
                Greenstack includes predefined shortcuts in <code>KEYBOARD_SHORTCUTS</code>:
              </DocsParagraph>

              <DocsCodeBlock language="jsx" copy>
{`import { KEYBOARD_SHORTCUTS, formatShortcut } from '../hooks/useKeyboardShortcuts';

// Display shortcut in UI
const shortcut = KEYBOARD_SHORTCUTS.TOGGLE_THEME;
console.log(formatShortcut(shortcut)); // "Ctrl + Shift + T"

// Use predefined shortcut
const shortcuts = [
  {
    ...KEYBOARD_SHORTCUTS.UPLOAD_FILE,
    callback: () => openUploadDialog()
  }
];`}
              </DocsCodeBlock>
            </div>
          </DocsAccordionItem>

          <DocsAccordionItem title="Creating Custom Hooks">
            <DocsParagraph>
              Follow these patterns when creating custom hooks:
            </DocsParagraph>

            <DocsCodeBlock language="jsx" copy>
{`import { useState, useEffect, useCallback } from 'react';

/**
 * Example: Hook to fetch data from API
 */
export const useApiData = (url) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(\`HTTP error! status: \${response.status}\`);
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
};

/**
 * Example: Hook for localStorage
 */
export const useLocalStorage = (key, initialValue) => {
  // Get initial value from localStorage or use default
  const [value, setValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error('Error reading from localStorage:', error);
      return initialValue;
    }
  });

  // Update localStorage when value changes
  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Error writing to localStorage:', error);
    }
  }, [key, value]);

  return [value, setValue];
};

// Usage
function MyComponent() {
  const { data, loading, error } = useApiData('/api/devices');
  const [theme, setTheme] = useLocalStorage('theme', 'dark');

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return <div>{/* Render data */}</div>;
}`}
            </DocsCodeBlock>
          </DocsAccordionItem>
        </DocsAccordion>
      </DocsSection>

      <DocsSection title="Component Development">
        <DocsParagraph>
          Learn how to create and structure React components following Greenstack's patterns.
        </DocsParagraph>

        <DocsTabs>
          <DocsTab label="Component Structure" icon={<Component className="w-4 h-4" />}>
            <DocsCodeBlock language="jsx" copy>
{`import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { Card, Button } from '../ui';

/**
 * MyComponent - Brief description
 *
 * Detailed description of what this component does,
 * its purpose, and any important usage notes.
 *
 * @param {string} title - Component title
 * @param {array} items - Array of items to display
 * @param {function} onAction - Callback when action is triggered
 */
export function MyComponent({ title, items = [], onAction }) {
  // State
  const [isExpanded, setIsExpanded] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);

  // Effects
  useEffect(() => {
    // Initialize or side effects
    console.log('Component mounted');

    return () => {
      // Cleanup
      console.log('Component unmounted');
    };
  }, []);

  // Event handlers
  const handleItemClick = (item) => {
    setSelectedItem(item);
    onAction?.(item);
  };

  const handleToggle = () => {
    setIsExpanded(!isExpanded);
  };

  // Render nothing if no items
  if (items.length === 0) {
    return (
      <Card>
        <p className="text-muted-foreground">No items available</p>
      </Card>
    );
  }

  // Main render
  return (
    <Card className="p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-semibold text-foreground">{title}</h3>
        <Button onClick={handleToggle}>
          {isExpanded ? 'Collapse' : 'Expand'}
        </Button>
      </div>

      {isExpanded && (
        <div className="space-y-2">
          {items.map((item) => (
            <div
              key={item.id}
              onClick={() => handleItemClick(item)}
              className={\`
                p-3 rounded-lg border cursor-pointer
                transition-colors hover:bg-surface-hover
                \${selectedItem?.id === item.id ? 'border-brand-green' : 'border-border'}
              \`}
            >
              <p className="font-medium text-foreground">{item.name}</p>
              <p className="text-sm text-muted-foreground">{item.description}</p>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}

// PropTypes for type checking
MyComponent.propTypes = {
  title: PropTypes.string.isRequired,
  items: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
    name: PropTypes.string.isRequired,
    description: PropTypes.string,
  })),
  onAction: PropTypes.func,
};

// Default props
MyComponent.defaultProps = {
  items: [],
  onAction: null,
};

export default MyComponent;`}
            </DocsCodeBlock>
          </DocsTab>

          <DocsTab label="Styling with Tailwind" icon={<Palette className="w-4 h-4" />}>
            <DocsParagraph>
              Greenstack uses Tailwind CSS with custom theme variables:
            </DocsParagraph>

            <DocsCodeBlock language="jsx" copy>
{`function MyStyledComponent() {
  return (
    <div>
      {/* Colors from theme */}
      <div className="bg-background text-foreground">
        Main background with primary text
      </div>

      <div className="bg-surface text-muted-foreground">
        Card/panel background with secondary text
      </div>

      <div className="border-brand-green text-brand-green">
        Brand color (adjusts with theme)
      </div>

      {/* Hover states */}
      <button className="bg-surface hover:bg-surface-hover transition-colors">
        Hover me
      </button>

      {/* Responsive design */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Responsive grid */}
      </div>

      {/* Custom spacing */}
      <div className="p-4 m-2 space-y-4">
        {/* Padding, margin, vertical spacing */}
      </div>

      {/* Conditional classes */}
      <div className={\`
        px-4 py-2 rounded-lg
        \${isActive ? 'bg-brand-green text-white' : 'bg-surface text-foreground'}
        \${isDisabled && 'opacity-50 cursor-not-allowed'}
      \`}>
        Conditional styling
      </div>
    </div>
  );
}`}
            </DocsCodeBlock>

            <DocsCallout type="info" title="Theme Variables">
              <DocsParagraph>
                Available theme color classes:
              </DocsParagraph>
              <ul className="list-disc list-inside space-y-1 text-sm mt-2">
                <li><code>brand-green</code> - Primary brand color</li>
                <li><code>background</code> - Main background</li>
                <li><code>surface</code> - Cards/panels</li>
                <li><code>surface-hover</code> - Surface hover state</li>
                <li><code>border</code> - Borders</li>
                <li><code>foreground</code> - Primary text</li>
                <li><code>muted-foreground</code> - Secondary text</li>
                <li><code>success</code>, <code>warning</code>, <code>destructive</code> - Status colors</li>
              </ul>
            </DocsCallout>
          </DocsTab>

          <DocsTab label="State Management" icon={<Settings className="w-4 h-4" />}>
            <DocsParagraph>
              Best practices for managing component state:
            </DocsParagraph>

            <DocsCodeBlock language="jsx" copy>
{`import { useState, useReducer, useCallback } from 'react';

// 1. Simple state with useState
function SimpleState() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>
        Count: {count}
      </button>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
    </div>
  );
}

// 2. Complex state with useReducer
const initialState = {
  items: [],
  loading: false,
  error: null,
  selectedId: null,
};

function reducer(state, action) {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };

    case 'SET_ITEMS':
      return { ...state, items: action.payload, loading: false };

    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };

    case 'SELECT_ITEM':
      return { ...state, selectedId: action.payload };

    case 'ADD_ITEM':
      return { ...state, items: [...state.items, action.payload] };

    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(item => item.id !== action.payload)
      };

    default:
      return state;
  }
}

function ComplexState() {
  const [state, dispatch] = useReducer(reducer, initialState);

  const loadItems = useCallback(async () => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const response = await fetch('/api/items');
      const items = await response.json();
      dispatch({ type: 'SET_ITEMS', payload: items });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
    }
  }, []);

  return (
    <div>
      {state.loading && <div>Loading...</div>}
      {state.error && <div>Error: {state.error}</div>}
      {state.items.map(item => (
        <div key={item.id} onClick={() => dispatch({ type: 'SELECT_ITEM', payload: item.id })}>
          {item.name}
        </div>
      ))}
    </div>
  );
}`}
            </DocsCodeBlock>
          </DocsTab>
        </DocsTabs>
      </DocsSection>

      <DocsSection title="API Integration">
        <DocsParagraph>
          Best practices for integrating with the backend API:
        </DocsParagraph>

        <DocsCodeBlock language="jsx" copy>
{`import { useState, useEffect } from 'react';

const API_BASE = 'http://localhost:8000';

function DeviceList() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch devices on mount
  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const response = await fetch(\`\${API_BASE}/api/eds\`);
        if (!response.ok) {
          throw new Error(\`HTTP error! status: \${response.status}\`);
        }
        const data = await response.json();
        setDevices(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDevices();
  }, []);

  // Upload file
  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(\`\${API_BASE}/api/eds/upload\`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(\`Upload failed: \${response.status}\`);
      }

      const result = await response.json();
      console.log('Upload successful:', result);

      // Refresh devices list
      // ...
    } catch (err) {
      console.error('Upload error:', err);
    }
  };

  // Delete device
  const handleDelete = async (id) => {
    try {
      const response = await fetch(\`\${API_BASE}/api/eds/\${id}\`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error(\`Delete failed: \${response.status}\`);
      }

      // Remove from state
      setDevices(devices.filter(d => d.id !== id));
    } catch (err) {
      console.error('Delete error:', err);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      {devices.map(device => (
        <div key={device.id}>
          <h3>{device.product_name}</h3>
          <button onClick={() => handleDelete(device.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
}`}
        </DocsCodeBlock>
      </DocsSection>

      <DocsSection title="Best Practices">
        <div className="space-y-4">
          <DocsCallout type="success" title="Code Organization">
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Keep components focused on a single responsibility</li>
              <li>Extract reusable logic into custom hooks</li>
              <li>Use PropTypes or TypeScript for type checking</li>
              <li>Write descriptive JSDoc comments for components</li>
              <li>Keep files under 300 lines - split if larger</li>
            </ul>
          </DocsCallout>

          <DocsCallout type="info" title="Performance">
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Use React.memo() for expensive components that render frequently</li>
              <li>Memoize callbacks with useCallback() to prevent unnecessary re-renders</li>
              <li>Memoize computed values with useMemo()</li>
              <li>Implement lazy loading for heavy components</li>
              <li>Debounce search inputs and API calls</li>
            </ul>
          </DocsCallout>

          <DocsCallout type="warning" title="Common Pitfalls">
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Always cleanup side effects in useEffect return function</li>
              <li>Don't forget dependency arrays in useEffect, useCallback, useMemo</li>
              <li>Avoid inline object/array creation in render (causes re-renders)</li>
              <li>Don't mutate state directly - always use setState functions</li>
              <li>Handle loading and error states for all async operations</li>
            </ul>
          </DocsCallout>
        </div>
      </DocsSection>

      <DocsSection title="Next Steps">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <a href="/docs/developer/backend" className="border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <Code className="w-8 h-8 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground mb-1">Backend Development</h4>
            <p className="text-sm text-muted-foreground">Learn backend API development</p>
          </a>

          <a href="/docs/components/overview" className="border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <Component className="w-8 h-8 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground mb-1">Component Gallery</h4>
            <p className="text-sm text-muted-foreground">Browse available components</p>
          </a>

          <a href="/docs/developer/contributing" className="border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <Rocket className="w-8 h-8 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground mb-1">Contributing</h4>
            <p className="text-sm text-muted-foreground">Contribute to Greenstack</p>
          </a>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
