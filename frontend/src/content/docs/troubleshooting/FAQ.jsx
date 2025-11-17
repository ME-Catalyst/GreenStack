import React from 'react';
import { HelpCircle, Search, Book, MessageCircle, Zap } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import { Card, CardContent, CardHeader, CardTitle, Badge } from '../../../components/ui';

export const metadata = {
  id: 'troubleshooting/faq',
  title: 'Frequently Asked Questions',
  description: 'Common questions and answers about Greenstack installation, usage, and troubleshooting',
  category: 'troubleshooting',
  order: 3,
  keywords: ['faq', 'questions', 'answers', 'help', 'support', 'common'],
  lastUpdated: '2025-01-17',
};

export default function FAQ({ onNavigate }) {
  const faqCategories = [
    {
      title: 'General',
      icon: <Book className="w-4 h-4" />,
      questions: [
        {
          q: 'What is Greenstack?',
          a: 'Greenstack is a modern web-based tool for managing IO-Link device descriptions (IODDs). It provides intelligent parsing of IODD/EDS XML files, a searchable database, API access, and a beautiful user interface for exploring device capabilities and parameters.'
        },
        {
          q: 'What file formats does Greenstack support?',
          a: 'Greenstack supports IODD (IO-Link Device Description) XML files and EDS (Electronic Data Sheet) files. The system can parse and validate these XML formats, extracting device metadata, parameters, and configurations.'
        },
        {
          q: 'Is Greenstack free to use?',
          a: 'Yes! Greenstack is open-source software licensed under the MIT License. You can use it freely for personal, commercial, or educational purposes. Contributions to the project are welcome!'
        },
        {
          q: 'What technologies power Greenstack?',
          a: 'Greenstack uses a modern tech stack: React + Vite for the frontend, FastAPI (Python) for the backend API, SQLAlchemy for database ORM, and SQLite/PostgreSQL for data storage. The UI is built with Tailwind CSS and Radix UI components.'
        },
        {
          q: 'Can I use Greenstack offline?',
          a: 'Yes! Greenstack can run completely offline once installed. It uses a local database (SQLite by default) and doesn\'t require an internet connection for core functionality. However, some features like automatic updates or external integrations may need connectivity.'
        }
      ]
    },
    {
      title: 'Installation & Setup',
      icon: <Zap className="w-4 h-4" />,
      questions: [
        {
          q: 'What are the system requirements?',
          a: <>
            <strong>Minimum:</strong> Python 3.10+, Node.js 18+, 4GB RAM, 2GB disk space
            <br />
            <strong>Recommended:</strong> Python 3.11+, Node.js 20+, 8GB RAM, 10GB disk space for production
          </>
        },
        {
          q: 'How do I install Greenstack on Windows?',
          a: <>
            See the <DocsLink href="/docs/getting-started/windows-installation" external={false} onNavigate={onNavigate}>Windows Installation Guide</DocsLink> for detailed step-by-step instructions. Quick version: install Python, Node.js, clone the repo, install dependencies, and run the start scripts.
          </>
        },
        {
          q: 'Can I deploy Greenstack with Docker?',
          a: <>
            Yes! Greenstack includes Docker Compose configuration for easy deployment. See the <DocsLink href="/docs/deployment/docker" external={false} onNavigate={onNavigate}>Docker Deployment Guide</DocsLink> for complete instructions.
          </>
        },
        {
          q: 'How do I update Greenstack to the latest version?',
          a: <>
            <DocsParagraph>For git installations, pull the latest changes and reinstall dependencies:</DocsParagraph>
            <DocsCodeBlock language="bash">
{`git pull origin main
pip install -r requirements.txt
cd frontend && npm install && npm run build`}
            </DocsCodeBlock>
          </>
        },
        {
          q: 'Which database should I use: SQLite or PostgreSQL?',
          a: 'SQLite is perfect for development and small deployments (< 1000 devices). PostgreSQL is recommended for production environments, high concurrency, or large datasets (> 1000 devices). The application works identically with both.'
        }
      ]
    },
    {
      title: 'Usage & Features',
      icon: <Search className="w-4 h-4" />,
      questions: [
        {
          q: 'How do I upload an IODD file?',
          a: <>
            <DocsParagraph>Use the web interface or API:</DocsParagraph>
            <strong>Web Interface:</strong> Click "Upload IODD" button, select your XML file, and submit.
            <br />
            <strong>API:</strong>
            <DocsCodeBlock language="bash">
{`curl -X POST http://localhost:8000/api/iodds/upload \\
  -F "file=@device.xml"`}
            </DocsCodeBlock>
          </>
        },
        {
          q: 'Can I search for devices by vendor or parameter?',
          a: 'Yes! The search functionality supports full-text search across vendor names, product names, device IDs, parameter names, and descriptions. Use the search bar in the web interface or the /api/search endpoint.'
        },
        {
          q: 'How do I export device data?',
          a: 'Device data can be exported as JSON via the API. Each device has a dedicated endpoint that returns complete information including all parameters, modules, and metadata in structured JSON format.'
        },
        {
          q: 'Does Greenstack support bulk uploads?',
          a: 'Currently, files must be uploaded individually. However, you can use the API in a script to automate bulk uploads. A drag-and-drop bulk upload feature is planned for a future release.'
        },
        {
          q: 'Can I customize the theme?',
          a: <>
            Yes! Greenstack includes a theme system with preset themes (Forest, Ocean, Sunset, Midnight) and support for custom themes. See the <DocsLink href="/docs/components/theme-system" external={false} onNavigate={onNavigate}>Theme System Guide</DocsLink> for details.
          </>
        }
      ]
    },
    {
      title: 'API & Integration',
      icon: <MessageCircle className="w-4 h-4" />,
      questions: [
        {
          q: 'How do I access the API documentation?',
          a: <>
            Start the backend server and visit <code>http://localhost:8000/docs</code> for interactive Swagger UI documentation, or <code>http://localhost:8000/redoc</code> for ReDoc-style documentation.
          </>
        },
        {
          q: 'Does the API require authentication?',
          a: 'By default, the API is open for development. For production deployments, you can enable authentication by configuring API keys or OAuth2. See the API Authentication documentation for setup instructions.'
        },
        {
          q: 'What response format does the API use?',
          a: 'All API endpoints return JSON responses with consistent structure. Successful responses include the requested data, while errors return HTTP status codes with detailed error messages and codes.'
        },
        {
          q: 'Can I integrate Greenstack with other systems?',
          a: 'Yes! The REST API allows integration with any system that can make HTTP requests. Common integrations include PLCs, SCADA systems, device management platforms, and custom automation tools.'
        },
        {
          q: 'Is there a rate limit on API requests?',
          a: 'By default, there are no rate limits for development. Production deployments should implement rate limiting based on their needs using reverse proxy configuration (Nginx, Traefik) or API gateway.'
        }
      ]
    },
    {
      title: 'Troubleshooting',
      icon: <HelpCircle className="w-4 h-4" />,
      questions: [
        {
          q: 'The frontend shows "Cannot connect to backend"',
          a: <>
            <DocsParagraph>This usually means the backend server isn\'t running. Verify:</DocsParagraph>
            <ul className="list-disc ml-6 space-y-1 text-sm">
              <li>Backend is running on <code>http://localhost:8000</code></li>
              <li>Check backend logs for errors</li>
              <li>Verify <code>VITE_API_URL</code> in <code>.env</code> matches backend URL</li>
              <li>Check for firewall/antivirus blocking connections</li>
            </ul>
          </>
        },
        {
          q: 'IODD upload fails with "Invalid XML" error',
          a: <>
            <DocsParagraph>Common causes:</DocsParagraph>
            <ul className="list-disc ml-6 space-y-1 text-sm">
              <li>File is not valid XML (check for syntax errors)</li>
              <li>File is not an IODD/EDS file (wrong schema)</li>
              <li>File is corrupted or incomplete</li>
              <li>File encoding is not UTF-8</li>
            </ul>
            <DocsParagraph className="mt-2">Validate your XML file using an XML validator before uploading.</DocsParagraph>
          </>
        },
        {
          q: 'Port 8000 is already in use',
          a: <>
            <DocsParagraph>Another application is using port 8000. Options:</DocsParagraph>
            <DocsParagraph>1. Change the port in backend config:</DocsParagraph>
            <DocsCodeBlock language="bash">
{`uvicorn src.api:app --host 0.0.0.0 --port 8001`}
            </DocsCodeBlock>
            <DocsParagraph>2. Or stop the other application using port 8000:</DocsParagraph>
            <DocsCodeBlock language="bash">
{`# Windows
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9`}
            </DocsCodeBlock>
          </>
        },
        {
          q: 'Database migration errors',
          a: <>
            <DocsParagraph>If you see Alembic migration errors:</DocsParagraph>
            <DocsCodeBlock language="bash">
{`# Check current migration status
alembic current

# Reset database (WARNING: deletes all data)
rm greenstack.db
alembic upgrade head

# Or run migrations manually
alembic upgrade head`}
            </DocsCodeBlock>
          </>
        },
        {
          q: 'Frontend build fails with memory error',
          a: <>
            <DocsParagraph>Increase Node.js memory limit:</DocsParagraph>
            <DocsCodeBlock language="bash">
{`# Windows (PowerShell)
$env:NODE_OPTIONS="--max-old-space-size=4096"
npm run build

# Linux/Mac
NODE_OPTIONS="--max-old-space-size=4096" npm run build`}
            </DocsCodeBlock>
          </>
        }
      ]
    },
    {
      title: 'Development & Contributing',
      icon: <MessageCircle className="w-4 h-4" />,
      questions: [
        {
          q: 'How can I contribute to Greenstack?',
          a: <>
            We welcome contributions! See the <DocsLink href="/docs/developer/contributing" external={false} onNavigate={onNavigate}>Contributing Guide</DocsLink> for detailed instructions on setting up your development environment, code style guidelines, and the pull request process.
          </>
        },
        {
          q: 'Where do I report bugs?',
          a: <>
            Report bugs on the <DocsLink href="https://github.com/ME-Catalyst/greenstack/issues" external>GitHub Issues</DocsLink> page. Please include:
            <ul className="list-disc ml-6 space-y-1 text-sm mt-2">
              <li>Greenstack version</li>
              <li>Operating system</li>
              <li>Steps to reproduce</li>
              <li>Expected vs actual behavior</li>
              <li>Error logs (if applicable)</li>
            </ul>
          </>
        },
        {
          q: 'How do I run tests?',
          a: <>
            <DocsParagraph>Backend tests use pytest:</DocsParagraph>
            <DocsCodeBlock language="bash">
{`# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_api.py`}
            </DocsCodeBlock>
            <DocsParagraph>See the <DocsLink href="/docs/developer/testing" external={false} onNavigate={onNavigate}>Testing Guide</DocsLink> for more details.</DocsParagraph>
          </>
        },
        {
          q: 'What code style should I follow?',
          a: <>
            <strong>Python:</strong> Black formatting, Ruff linting, type hints required
            <br />
            <strong>JavaScript/React:</strong> Prettier formatting, ESLint, functional components with hooks
            <br />
            <DocsParagraph className="mt-2">Run <code>make format</code> to auto-format all code.</DocsParagraph>
          </>
        },
        {
          q: 'How do I add a new API endpoint?',
          a: <>
            <DocsParagraph>1. Add route in <code>src/api/routes/</code></DocsParagraph>
            <DocsParagraph>2. Implement business logic in <code>src/services/</code></DocsParagraph>
            <DocsParagraph>3. Add database operations in <code>src/storage/</code></DocsParagraph>
            <DocsParagraph>4. Write tests in <code>tests/</code></DocsParagraph>
            <DocsParagraph>5. Update API documentation</DocsParagraph>
            <br />
            <DocsParagraph>See the <DocsLink href="/docs/developer/backend" external={false} onNavigate={onNavigate}>Backend Development Guide</DocsLink> for architecture details.</DocsParagraph>
          </>
        }
      ]
    }
  ];

  return (
    <DocsPage>
      <DocsHero
        title="Frequently Asked Questions"
        description="Find quick answers to common questions about Greenstack"
        icon={<HelpCircle className="w-12 h-12 text-brand-green" />}
      />

      {/* Quick Links */}
      <DocsSection>
        <div className="grid gap-4 md:grid-cols-3 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Book className="w-4 h-4 text-brand-green" />
                Documentation
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Browse comprehensive guides and tutorials
              </p>
              <DocsLink href="/docs/getting-started/quick-start" external={false} onNavigate={onNavigate}>
                Get Started →
              </DocsLink>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <HelpCircle className="w-4 h-4 text-brand-green" />
                Common Issues
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Solutions to frequently encountered problems
              </p>
              <DocsLink href="/docs/troubleshooting/common-issues" external={false} onNavigate={onNavigate}>
                View Issues →
              </DocsLink>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <MessageCircle className="w-4 h-4 text-brand-green" />
                Get Support
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Ask questions on GitHub Discussions
              </p>
              <DocsLink href="https://github.com/ME-Catalyst/greenstack/discussions" external>
                Ask Question →
              </DocsLink>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* FAQ Categories */}
      {faqCategories.map((category, categoryIndex) => (
        <DocsSection
          key={categoryIndex}
          title={category.title}
          icon={category.icon}
        >
          <div className="space-y-4 my-6">
            {category.questions.map((item, itemIndex) => (
              <Card key={itemIndex}>
                <CardHeader>
                  <CardTitle className="text-base flex items-start gap-3">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green text-xs font-bold">
                      Q
                    </span>
                    <span>{item.q}</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-start gap-3">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-400 text-xs font-bold">
                      A
                    </span>
                    <div className="text-sm text-muted-foreground">
                      {typeof item.a === 'string' ? <DocsParagraph>{item.a}</DocsParagraph> : item.a}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </DocsSection>
      ))}

      {/* Still Need Help */}
      <DocsSection title="Still Need Help?">
        <DocsParagraph>
          If you couldn't find the answer to your question, here are more resources:
        </DocsParagraph>

        <div className="grid gap-4 md:grid-cols-2 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">GitHub Discussions</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Ask questions, share ideas, and get help from the community
              </p>
              <DocsLink href="https://github.com/ME-Catalyst/greenstack/discussions" external>
                Join Discussion →
              </DocsLink>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">GitHub Issues</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Report bugs or request new features
              </p>
              <DocsLink href="https://github.com/ME-Catalyst/greenstack/issues" external>
                Open Issue →
              </DocsLink>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Debugging Guide</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Learn how to debug and troubleshoot issues
              </p>
              <DocsLink href="/docs/troubleshooting/debugging" external={false} onNavigate={onNavigate}>
                Debug Guide →
              </DocsLink>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">API Documentation</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Explore the complete API reference
              </p>
              <DocsLink href="/docs/api/overview" external={false} onNavigate={onNavigate}>
                View API Docs →
              </DocsLink>
            </CardContent>
          </Card>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
