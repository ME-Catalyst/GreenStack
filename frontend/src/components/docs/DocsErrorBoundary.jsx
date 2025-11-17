import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button, Card, CardHeader, CardContent, CardTitle } from '../ui';

/**
 * DocsErrorBoundary - Error Boundary for Documentation Pages
 *
 * Catches and handles runtime errors in documentation components
 * Provides user-friendly error messages and recovery options
 */
class DocsErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log the error to console for debugging
    console.error('Documentation Error:', error, errorInfo);

    this.setState({
      error,
      errorInfo
    });
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null
    });

    // Navigate to quick start if provided
    if (this.props.onReset) {
      this.props.onReset();
    }
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center min-h-[400px] p-8">
          <Card className="max-w-2xl w-full border-warning">
            <CardHeader>
              <div className="flex items-center gap-3">
                <AlertTriangle className="w-8 h-8 text-warning" />
                <CardTitle className="text-2xl">Documentation Error</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-foreground">
                An error occurred while rendering this documentation page.
                This might be due to a malformed component or missing data.
              </p>

              {this.state.error && (
                <div className="p-4 bg-surface rounded-lg border border-border">
                  <p className="text-sm font-semibold text-foreground mb-2">
                    Error Details:
                  </p>
                  <p className="text-sm text-muted-foreground font-mono">
                    {this.state.error.toString()}
                  </p>
                </div>
              )}

              {process.env.NODE_ENV === 'development' && this.state.errorInfo && (
                <details className="p-4 bg-surface rounded-lg border border-border">
                  <summary className="text-sm font-semibold text-foreground cursor-pointer mb-2">
                    Component Stack Trace
                  </summary>
                  <pre className="text-xs text-muted-foreground font-mono overflow-x-auto mt-2">
                    {this.state.errorInfo.componentStack}
                  </pre>
                </details>
              )}

              <div className="flex gap-3 pt-4">
                <Button
                  onClick={this.handleReset}
                  className="flex items-center gap-2"
                >
                  <RefreshCw className="w-4 h-4" />
                  Try Again
                </Button>

                {this.props.onNavigateHome && (
                  <Button
                    variant="outline"
                    onClick={this.props.onNavigateHome}
                  >
                    Go to Quick Start
                  </Button>
                )}
              </div>

              <p className="text-sm text-muted-foreground">
                If this issue persists, please report it on our{' '}
                <a
                  href="https://github.com/ME-Catalyst/greenstack/issues"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-brand-green hover:underline"
                >
                  GitHub Issues page
                </a>.
              </p>
            </CardContent>
          </Card>
        </div>
      );
    }

    return this.props.children;
  }
}

export default DocsErrorBoundary;
