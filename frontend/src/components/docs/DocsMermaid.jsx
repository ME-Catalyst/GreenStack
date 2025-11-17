import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

/**
 * DocsMermaid - Render Mermaid diagrams in documentation
 *
 * Features:
 * - Renders beautiful, modern diagrams from Mermaid syntax
 * - Supports flowcharts, sequence diagrams, ER diagrams, etc.
 * - Theme-aware styling
 * - Responsive and interactive
 */

// Initialize mermaid with theme settings
mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  themeVariables: {
    primaryColor: '#3DB60F',
    primaryTextColor: '#fff',
    primaryBorderColor: '#3DB60F',
    lineColor: '#51cf66',
    secondaryColor: '#2d5016',
    tertiaryColor: '#0a0e27',
    background: '#1a1f3a',
    mainBkg: '#1a1f3a',
    secondBkg: '#2a3050',
    border1: '#3a4060',
    border2: '#4a5070',
    note: '#2d5016',
    noteBkg: '#2d5016',
    noteText: '#fff',
    noteBorder: '#3DB60F',
    fontSize: '16px',
    fontFamily: 'ui-sans-serif, system-ui, sans-serif',
  },
  flowchart: {
    curve: 'basis',
    padding: 20,
    nodeSpacing: 50,
    rankSpacing: 50,
  },
  sequence: {
    actorMargin: 50,
    boxMargin: 10,
    boxTextMargin: 5,
    noteMargin: 10,
    messageMargin: 35,
  },
  er: {
    layoutDirection: 'TB',
    minEntityWidth: 100,
    minEntityHeight: 75,
    entityPadding: 15,
    fontSize: 14,
  },
});

const DocsMermaid = ({ chart, className = '' }) => {
  const mermaidRef = useRef(null);
  const [svg, setSvg] = React.useState('');
  const [error, setError] = React.useState(null);

  useEffect(() => {
    const renderDiagram = async () => {
      if (!chart || !mermaidRef.current) return;

      try {
        // Generate unique ID for this diagram
        const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`;

        // Render the diagram
        const { svg } = await mermaid.render(id, chart);
        setSvg(svg);
        setError(null);
      } catch (err) {
        console.error('Mermaid rendering error:', err);
        setError(err.message);
      }
    };

    renderDiagram();
  }, [chart]);

  if (error) {
    return (
      <div className={`border border-error rounded-lg p-4 bg-error/10 ${className}`}>
        <p className="text-error text-sm font-mono">
          <strong>Diagram Error:</strong> {error}
        </p>
      </div>
    );
  }

  return (
    <div
      ref={mermaidRef}
      className={`mermaid-diagram bg-surface rounded-lg p-6 overflow-x-auto border border-border ${className}`}
      dangerouslySetInnerHTML={{ __html: svg }}
      style={{
        minHeight: svg ? 'auto' : '200px',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    />
  );
};

export default DocsMermaid;
