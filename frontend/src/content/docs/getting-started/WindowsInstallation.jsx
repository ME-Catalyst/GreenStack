import React from 'react';
import { Terminal, CheckCircle, AlertTriangle, Package, Play, Folder, Code } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsList, DocsLink } from '../../../components/docs/DocsText';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import DocsSteps from '../../../components/docs/DocsSteps';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../../components/ui';

export const metadata = {
  id: 'getting-started/windows-installation',
  title: 'Windows Installation',
  description: 'Step-by-step guide to installing and running Greenstack on Windows',
  category: 'getting-started',
  order: 3,
  keywords: ['windows', 'install', 'setup', 'setup.bat', 'windows 10', 'windows 11'],
  lastUpdated: '2025-01-17',
};

export default function WindowsInstallation({ onNavigate }) {
  return (
    <DocsPage>
      <DocsHero
        title="Windows Installation"
        description="Complete guide to installing and running Greenstack on Windows 10 and Windows 11"
        icon={<Terminal className="w-12 h-12 text-brand-green" />}
      />

      {/* Quick Start */}
      <DocsSection title="Quick Start" icon={<Play />}>
        <DocsParagraph>
          Getting Greenstack running on Windows is incredibly simple with our automated setup script.
          Just follow these three steps:
        </DocsParagraph>

        <DocsSteps
          steps={[
            {
              title: 'Download or Clone Repository',
              content: (
                <div>
                  <DocsParagraph>
                    Download the latest release or clone the repository:
                  </DocsParagraph>
                  <DocsCodeBlock language="bash">
{`git clone https://github.com/ME-Catalyst/greenstack.git
cd greenstack`}
                  </DocsCodeBlock>
                </div>
              )
            },
            {
              title: 'Run Setup Script',
              content: (
                <div>
                  <DocsParagraph>
                    Simply double-click <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">setup.bat</code> in the project root, or run from command line:
                  </DocsParagraph>
                  <DocsCodeBlock language="bash">
{`setup.bat`}
                  </DocsCodeBlock>
                  <DocsParagraph className="mt-4">
                    The script will automatically:
                  </DocsParagraph>
                  <ul className="list-disc list-inside space-y-2 text-foreground ml-4">
                    <li>Check for Python 3.10+ and Node.js 18+</li>
                    <li>Install all Python dependencies</li>
                    <li>Install frontend dependencies</li>
                    <li>Start both backend and frontend servers</li>
                    <li>Open your browser to the application</li>
                  </ul>
                </div>
              )
            },
            {
              title: 'Access the Application',
              content: (
                <div>
                  <DocsParagraph>
                    Once the setup completes, the application will automatically open in your default browser:
                  </DocsParagraph>
                  <Card className="mt-4">
                    <CardContent className="pt-6">
                      <div className="space-y-2">
                        <div className="flex items-center gap-2">
                          <CheckCircle className="w-5 h-5 text-brand-green" />
                          <strong>Web Interface:</strong>{' '}
                          <code>http://localhost:6173</code>{' '}
                          <span className="text-sm text-muted-foreground">
                            (auto-detects the next open port in the 6000 range)
                          </span>
                        </div>
                        <div className="flex items-center gap-2">
                          <CheckCircle className="w-5 h-5 text-brand-green" />
                          <strong>API Docs:</strong> <code>http://localhost:8000/docs</code>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )
            }
          ]}
        />
      </DocsSection>

      {/* Prerequisites */}
      <DocsSection title="Prerequisites" icon={<Package />}>
        <DocsParagraph>
          Before running Greenstack, ensure you have the following installed on your Windows system:
        </DocsParagraph>

        <div className="grid gap-4 md:grid-cols-2 my-6">
          {/* Python Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Code className="w-5 h-5 text-brand-green" />
                Python 3.10+
              </CardTitle>
              <CardDescription>Required for backend API</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsParagraph>
                Download from <DocsLink href="https://www.python.org/downloads/" external>python.org</DocsLink>
              </DocsParagraph>
              <DocsCallout type="warning" title="Important">
                <DocsParagraph>
                  During installation, make sure to check "Add Python to PATH"
                </DocsParagraph>
              </DocsCallout>
              <DocsParagraph className="mt-4">
                Verify installation:
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`python --version
# Should show: Python 3.10.x or higher`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          {/* Node.js Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Terminal className="w-5 h-5 text-brand-green" />
                Node.js 18+
              </CardTitle>
              <CardDescription>Required for frontend development</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsParagraph>
                Download from <DocsLink href="https://nodejs.org/" external>nodejs.org</DocsLink> (LTS version recommended)
              </DocsParagraph>
              <DocsParagraph className="mt-4">
                Verify installation:
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`node --version
npm --version`}
              </DocsCodeBlock>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* What setup.bat Does */}
      <DocsSection title="What setup.bat Does" icon={<Folder />}>
        <DocsParagraph>
          The setup script automates the entire installation and startup process. Here's what happens
          behind the scenes:
        </DocsParagraph>

        <Card className="my-6">
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  1
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Dependency Check</h4>
                  <p className="text-sm text-muted-foreground">
                    Verifies Python and Node.js are installed and meet minimum version requirements
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  2
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Backend Setup</h4>
                  <p className="text-sm text-muted-foreground">
                    Installs Python packages from requirements.txt using pip
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  3
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Frontend Setup</h4>
                  <p className="text-sm text-muted-foreground">
                    Navigates to frontend directory and runs npm install
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  4
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Start Servers</h4>
                  <p className="text-sm text-muted-foreground">
                    Launches the Python backend API (port 8000) and the Vite frontend dev server
                    starting at port 6173 (auto-selects the next open port in the 6000s if needed)
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  5
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Health Check</h4>
                  <p className="text-sm text-muted-foreground">
                    Verifies both servers are running and responsive
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  6
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Open Browser</h4>
                  <p className="text-sm text-muted-foreground">
                    Automatically opens the detected frontend port (starting at http://localhost:6173) in your default browser
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Troubleshooting */}
      <DocsSection title="Troubleshooting" icon={<AlertTriangle />}>
        <DocsCallout type="warning" title="Common Issues">
          <div className="space-y-4">
            <div>
              <h4 className="font-semibold text-foreground mb-2">Python not found</h4>
              <DocsParagraph>
                If you see "Python is not recognized", you need to add Python to your PATH:
              </DocsParagraph>
              <ol className="list-decimal list-inside space-y-2 text-foreground ml-4">
                <li>Reinstall Python and check "Add Python to PATH"</li>
                <li>Or manually add Python installation directory to system PATH</li>
                <li>Restart your terminal/command prompt</li>
              </ol>
            </div>

            <div>
              <h4 className="font-semibold text-foreground mb-2">Port already in use</h4>
              <DocsParagraph>
                If ports are already in use, the launcher now rolls to the next open port in the 6000 range automatically.
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F`}
              </DocsCodeBlock>
            </div>

            <div>
              <h4 className="font-semibold text-foreground mb-2">Permission errors during pip install</h4>
              <DocsParagraph>
                Run command prompt as Administrator or use:
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`pip install --user -r requirements.txt`}
              </DocsCodeBlock>
            </div>

            <div>
              <h4 className="font-semibold text-foreground mb-2">Frontend build errors</h4>
              <DocsParagraph>
                Clear npm cache and reinstall:
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`cd frontend
npm cache clean --force
rd /s /q node_modules
npm install`}
              </DocsCodeBlock>
            </div>
          </div>
        </DocsCallout>

        <DocsParagraph className="mt-6">
          For more troubleshooting help, see the <DocsLink href="/docs/user-guide/troubleshooting" external={false} onNavigate={onNavigate}>
          Troubleshooting Guide</DocsLink>.
        </DocsParagraph>
      </DocsSection>

      {/* Manual Installation */}
      <DocsSection title="Manual Installation (Advanced)" icon={<Code />}>
        <DocsParagraph>
          If you prefer to run commands manually or need more control:
        </DocsParagraph>

        <DocsSteps
          steps={[
            {
              title: 'Install Backend Dependencies',
              content: (
                <DocsCodeBlock language="bash">
{`# From project root
pip install -r requirements.txt`}
                </DocsCodeBlock>
              )
            },
            {
              title: 'Install Frontend Dependencies',
              content: (
                <DocsCodeBlock language="bash">
{`cd frontend
npm install
cd ..`}
                </DocsCodeBlock>
              )
            },
            {
              title: 'Start Backend Server',
              content: (
                <DocsCodeBlock language="bash">
{`# Terminal 1
python -m src.start`}
                </DocsCodeBlock>
              )
            },
            {
              title: 'Start Frontend Server',
              content: (
                <DocsCodeBlock language="bash">
{`# Terminal 2
cd frontend
npm run dev`}
                </DocsCodeBlock>
              )
            }
          ]}
        />
      </DocsSection>

      {/* Next Steps */}
      <DocsSection title="Next Steps">
        <DocsParagraph>
          Now that Greenstack is installed and running, here's what to do next:
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-6">
          <DocsLink href="/docs/getting-started/quick-start" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Quick Start Guide</h5>
            <p className="text-sm text-muted-foreground">Learn the basics in 5 minutes</p>
          </DocsLink>

          <DocsLink href="/docs/user-guide/web-interface" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Web Interface Guide</h5>
            <p className="text-sm text-muted-foreground">Explore the dashboard features</p>
          </DocsLink>

          <DocsLink href="/docs/user-guide/configuration" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Configuration</h5>
            <p className="text-sm text-muted-foreground">Customize settings for your environment</p>
          </DocsLink>

          <DocsLink href="/docs/api/overview" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">API Documentation</h5>
            <p className="text-sm text-muted-foreground">Explore the REST API</p>
          </DocsLink>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
