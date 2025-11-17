import React from 'react';
import { Layers, Database, Code, Network, Box, GitBranch, Zap } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import DocsMermaid from '../../../components/docs/DocsMermaid';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../../../components/ui';

export const metadata = {
  id: 'developer/architecture',
  title: 'System Architecture',
  description: 'Comprehensive overview of Greenstack system design, architecture layers, data flow, and component interactions',
  category: 'developer',
  order: 1,
  keywords: ['architecture', 'design', 'structure', 'system', 'layers', 'backend', 'frontend'],
  lastUpdated: '2025-01-17',
};

export default function Architecture({ onNavigate }) {
  return (
    <DocsPage>
      <DocsHero
        title="System Architecture"
        description="Comprehensive overview of Greenstack's design, layers, and data flow"
        icon={<Layers className="w-12 h-12 text-brand-green" />}
      />

      {/* High-Level Overview */}
      <DocsSection title="High-Level Architecture" icon={<Layers />}>
        <DocsParagraph>
          Greenstack is a modern full-stack application built with a clear separation between
          frontend and backend. It follows a three-tier architecture with presentation, application,
          and data layers.
        </DocsParagraph>

        <DocsMermaid
          chart={`
graph TB
    subgraph Client["🖥️ Client Browser"]
        UI["React Frontend<br/>(Vite Dev Server)<br/>Port 5173"]
        Components["UI Components<br/>Contexts<br/>Hooks"]
        UI --> Components
    end

    subgraph Backend["⚡ FastAPI Backend<br/>Port 8000"]
        API["API Routes<br/>(FastAPI)"]
        BL["Business Logic<br/>(Parsers & Services)"]
        ORM["Database Layer<br/>(SQLAlchemy)"]

        API --> BL
        BL --> ORM
    end

    subgraph Data["💾 Data Layer"]
        DB[(SQLite Database<br/>greenstack.db)]
    end

    Client -->|HTTP/REST API| Backend
    ORM -->|SQL Queries| DB

    style Client fill:#2d5016,stroke:#3DB60F,stroke-width:3px,color:#fff
    style Backend fill:#1a1f3a,stroke:#3DB60F,stroke-width:3px,color:#fff
    style Data fill:#0a0e27,stroke:#3DB60F,stroke-width:3px,color:#fff
    style UI fill:#3a4060,stroke:#51cf66,color:#fff
    style Components fill:#3a4060,stroke:#51cf66,color:#fff
    style API fill:#3a4060,stroke:#51cf66,color:#fff
    style BL fill:#3a4060,stroke:#51cf66,color:#fff
    style ORM fill:#3a4060,stroke:#51cf66,color:#fff
    style DB fill:#2d5016,stroke:#3DB60F,stroke-width:2px,color:#fff
          `}
        />

        <div className="grid gap-4 md:grid-cols-3 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Code className="w-4 h-4 text-brand-green" />
                Frontend Layer
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                React 18 with Vite, Tailwind CSS, Radix UI components, and theme system
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Zap className="w-4 h-4 text-brand-green" />
                Backend Layer
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                FastAPI with Python 3.10+, SQLAlchemy ORM, and XML parsing
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Database className="w-4 h-4 text-brand-green" />
                Data Layer
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                SQLite database with structured schema for IO-Link device data
              </p>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Backend Architecture */}
      <DocsSection title="Backend Architecture" icon={<Zap />}>
        <DocsParagraph>
          The backend is built with FastAPI and follows a modular route-based architecture.
          Each functional area has dedicated route handlers and business logic.
        </DocsParagraph>

        <DocsMermaid
          chart={`
graph TB
    Request["📨 HTTP Request"]

    subgraph Middleware["Middleware Layer"]
        CORS["CORS<br/>Origin Validation"]
        RateLimit["Rate Limiting<br/>10/min uploads<br/>100/min general"]
    end

    subgraph Routes["🛣️ Route Layer"]
        EDS["EDS Routes<br/>/api/iodds/*"]
        Admin["Admin Routes<br/>/api/admin/*"]
        Theme["Theme Routes<br/>/api/themes/*"]
        Search["Search Routes<br/>/api/search/*"]
        MQTT["MQTT Routes<br/>/api/mqtt/*"]
    end

    subgraph Logic["⚙️ Business Logic"]
        Parser["EDS Parser<br/>(XML Processing)"]
        Validator["Validation<br/>(Pydantic Models)"]
        Services["Services<br/>(MQTT, Grafana)"]
    end

    subgraph Data["💾 Data Access"]
        ORM["SQLAlchemy ORM"]
        DB[(SQLite DB)]
    end

    Response["📤 JSON Response"]

    Request --> CORS
    CORS --> RateLimit
    RateLimit --> Routes

    Routes --> Logic
    Logic --> ORM
    ORM --> DB

    DB --> ORM
    ORM --> Logic
    Logic --> Routes
    Routes --> Response

    style Request fill:#3DB60F,stroke:#51cf66,stroke-width:2px,color:#000
    style Response fill:#3DB60F,stroke:#51cf66,stroke-width:2px,color:#000
    style Middleware fill:#2d5016,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Routes fill:#1a1f3a,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Logic fill:#2a3050,stroke:#51cf66,color:#fff
    style Data fill:#0a0e27,stroke:#3DB60F,stroke-width:2px,color:#fff
          `}
        />

        <DocsCallout type="info" title="Route Organization">
          <DocsParagraph>
            Routes are organized by domain functionality. Each route file is responsible for
            a specific feature area and includes all related endpoints (GET, POST, PUT, DELETE).
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      {/* Frontend Architecture */}
      <DocsSection title="Frontend Architecture" icon={<Code />}>
        <DocsParagraph>
          The frontend uses React 18 with modern hooks, context providers for state management,
          and a component-based architecture with lazy loading for optimal performance.
        </DocsParagraph>

        <DocsMermaid
          chart={`
graph TB
    App["App.jsx<br/>(Root Component)"]

    subgraph Context["🔄 Context Providers"]
        ThemeCtx["ThemeContext<br/>(Global Theme State)"]
    end

    subgraph Router["🛣️ Router"]
        Routes["React Router<br/>(Page Navigation)"]
    end

    subgraph Pages["📄 Page Components"]
        Search["SearchPage<br/>(Device Search)"]
        Details["EDSDetailsView<br/>(Device Details)"]
        Admin["AdminConsole<br/>(System Admin)"]
        Docs["DocsViewer<br/>(Documentation)"]
    end

    subgraph Components["🧩 Shared Components"]
        UI["UI Components<br/>(Button, Card, etc)"]
        Theme["ThemeManager<br/>(Theme UI)"]
        Editors["Editors & Forms"]
    end

    subgraph Data["📊 Data Management"]
        API["API Calls<br/>(axios)"]
        LocalState["Local State<br/>(useState)"]
    end

    App --> Context
    Context --> Router
    Router --> Pages
    Pages --> Components
    Pages --> Data
    Components --> UI
    Data --> API

    style App fill:#3DB60F,stroke:#51cf66,stroke-width:3px,color:#000
    style Context fill:#2d5016,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Router fill:#2d5016,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Pages fill:#1a1f3a,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Components fill:#2a3050,stroke:#51cf66,color:#fff
    style Data fill:#0a0e27,stroke:#3DB60F,stroke-width:2px,color:#fff
          `}
        />

        <div className="grid gap-4 md:grid-cols-2 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">State Management</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• <strong>ThemeContext:</strong> Global theme state</li>
                <li>• <strong>Local useState:</strong> Component-specific state</li>
                <li>• <strong>URL params:</strong> Navigation state</li>
                <li>• <strong>API responses:</strong> Server data caching</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Performance Optimizations</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• <strong>Lazy loading:</strong> Code splitting per route</li>
                <li>• <strong>Memoization:</strong> React.memo for heavy components</li>
                <li>• <strong>Virtual scrolling:</strong> Large lists optimization</li>
                <li>• <strong>Image optimization:</strong> Lazy image loading</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Data Flow */}
      <DocsSection title="Data Flow: IODD Upload Example" icon={<Network />}>
        <DocsParagraph>
          This sequence diagram shows how data flows through the system when a user uploads
          an IODD file.
        </DocsParagraph>

        <DocsMermaid
          chart={`
sequenceDiagram
    actor User
    participant UI as React UI
    participant API as FastAPI Backend
    participant Parser as EDS Parser
    participant DB as Database

    User->>UI: Upload IODD file
    UI->>UI: Validate file type & size

    UI->>API: POST /api/iodds/upload
    Note over UI,API: multipart/form-data

    API->>API: Check rate limit
    API->>API: Validate file format

    API->>Parser: Parse XML content
    Parser->>Parser: Extract metadata
    Parser->>Parser: Parse parameters
    Parser->>Parser: Decode data types

    Parser-->>API: Parsed device data

    API->>DB: Check for duplicates
    DB-->>API: No conflicts

    API->>DB: Create device record
    API->>DB: Create parameter records
    API->>DB: Commit transaction

    DB-->>API: Device ID: 123

    API-->>UI: 201 Created<br/>{id: 123, name: "Device"}

    UI->>UI: Update device list
    UI->>UI: Show success message
    UI->>User: Navigate to device details

    Note over User,DB: ✅ Complete in ~500ms
          `}
        />
      </DocsSection>

      {/* Database Schema */}
      <DocsSection title="Database Schema" icon={<Database />}>
        <DocsParagraph>
          Greenstack uses SQLite with a normalized schema designed for IO-Link device data.
          All queries use SQLAlchemy ORM for type safety and SQL injection prevention.
        </DocsParagraph>

        <DocsMermaid
          chart={`
erDiagram
    DEVICES ||--o{ PARAMETERS : has
    DEVICES ||--o{ MODULES : contains
    TICKETS ||--o{ ATTACHMENTS : includes

    DEVICES {
        int id PK
        int vendor_id
        int device_id
        string product_name
        string vendor_name
        string product_text
        string device_function
        string hardware_rev
        string firmware_rev
        string iodd_version
        json process_data_in
        json process_data_out
        datetime created_at
    }

    PARAMETERS {
        int id PK
        int device_id FK
        int index
        int subindex
        string name
        string description
        string data_type
        string access_rights
        string default_value
        string min_value
        string max_value
        string unit
        string category
    }

    MODULES {
        int id PK
        int device_id FK
        string name
        string description
        string type
    }

    THEMES {
        int id PK
        string name
        string description
        string preset_id
        json colors
        datetime created_at
        datetime updated_at
    }

    TICKETS {
        int id PK
        string title
        string description
        string status
        string priority
        string assignee
        datetime created_at
        datetime updated_at
    }

    ATTACHMENTS {
        int id PK
        int ticket_id FK
        string filename
        string file_path
        string mime_type
        datetime uploaded_at
    }

    MQTT_LOGS {
        int id PK
        datetime timestamp
        string topic
        string payload
        int qos
    }
          `}
        />

        <DocsCallout type="info" title="Database Management">
          <DocsParagraph>
            The database uses SQLite by default for simplicity. For production deployments with
            high concurrency, PostgreSQL is recommended. Connection management is centralized
            in <code>src/database.py</code> for easy switching.
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      {/* API Structure */}
      <DocsSection title="API Endpoint Structure">
        <DocsParagraph>
          The REST API follows RESTful conventions with consistent response formats.
        </DocsParagraph>

        <DocsMermaid
          chart={`
graph TB
    API["/api"]

    subgraph IODD["📦 IODD Management"]
        I1["/iodds<br/>GET - List all"]
        I2["/iodds/upload<br/>POST - Upload file"]
        I3["/iodds/:id<br/>GET - Get details"]
        I4["/iodds/:id<br/>DELETE - Remove"]
    end

    subgraph Search["🔍 Search & Filter"]
        S1["/search<br/>GET - Full-text search"]
        S2["/search/filters<br/>GET - Get filters"]
    end

    subgraph Themes["🎨 Theme System"]
        T1["/themes<br/>GET - List themes"]
        T2["/themes<br/>POST - Create custom"]
        T3["/themes/active<br/>GET - Active theme"]
        T4["/themes/:id/activate<br/>POST - Switch theme"]
    end

    subgraph Admin["⚙️ Admin Console"]
        A1["/admin/stats<br/>GET - Statistics"]
        A2["/admin/logs<br/>GET - System logs"]
        A3["/admin/backup<br/>POST - Create backup"]
        A4["/admin/vacuum<br/>POST - Optimize DB"]
    end

    subgraph Services["🔌 External Services"]
        M1["/mqtt/status<br/>GET - Broker status"]
        M2["/mqtt/publish<br/>POST - Send message"]
        G1["/services/grafana<br/>GET - Status"]
        N1["/services/nodered<br/>GET - Status"]
    end

    API --> IODD
    API --> Search
    API --> Themes
    API --> Admin
    API --> Services

    style API fill:#3DB60F,stroke:#51cf66,stroke-width:3px,color:#000
    style IODD fill:#1a1f3a,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Search fill:#1a1f3a,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Themes fill:#1a1f3a,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Admin fill:#1a1f3a,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Services fill:#1a1f3a,stroke:#3DB60F,stroke-width:2px,color:#fff
          `}
        />
      </DocsSection>

      {/* Security Architecture */}
      <DocsSection title="Security Architecture" icon={<GitBranch />}>
        <DocsParagraph>
          Security is implemented at multiple layers with rate limiting, input validation,
          and protection against common vulnerabilities.
        </DocsParagraph>

        <DocsMermaid
          chart={`
graph TB
    Request["🌐 Incoming Request"]

    subgraph Security["🛡️ Security Layers"]
        L1["Layer 1: CORS<br/>Origin validation"]
        L2["Layer 2: Rate Limiting<br/>SlowAPI middleware"]
        L3["Layer 3: Input Validation<br/>Pydantic models"]
        L4["Layer 4: SQL Injection Protection<br/>SQLAlchemy ORM"]
        L5["Layer 5: XSS Protection<br/>React auto-escaping"]
    end

    Response["✅ Secure Response"]

    Request --> L1
    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> L5
    L5 --> Response

    style Request fill:#ff6b6b,stroke:#ffd43b,stroke-width:2px,color:#000
    style Response fill:#51cf66,stroke:#3DB60F,stroke-width:2px,color:#000
    style Security fill:#1a1f3a,stroke:#3DB60F,stroke-width:3px,color:#fff
    style L1 fill:#2a3050,stroke:#51cf66,color:#fff
    style L2 fill:#2a3050,stroke:#51cf66,color:#fff
    style L3 fill:#2a3050,stroke:#51cf66,color:#fff
    style L4 fill:#2a3050,stroke:#51cf66,color:#fff
    style L5 fill:#2a3050,stroke:#51cf66,color:#fff
          `}
        />

        <div className="grid gap-4 md:grid-cols-2 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Backend Security</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• <strong>Rate Limiting:</strong> SlowAPI (10/min uploads, 100/min general)</li>
                <li>• <strong>CORS:</strong> Configured allowed origins</li>
                <li>• <strong>SQL Injection:</strong> SQLAlchemy ORM parameterization</li>
                <li>• <strong>File Validation:</strong> Type & size checks</li>
                <li>• <strong>Input Sanitization:</strong> Pydantic models</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Frontend Security</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• <strong>XSS Protection:</strong> React automatic escaping</li>
                <li>• <strong>CSRF:</strong> SameSite cookie policy</li>
                <li>• <strong>Input Validation:</strong> Client-side validation</li>
                <li>• <strong>Secure Storage:</strong> No sensitive data in localStorage</li>
                <li>• <strong>Content Security:</strong> Vite security defaults</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Deployment Architecture */}
      <DocsSection title="Deployment Architecture">
        <DocsParagraph>
          Greenstack supports multiple deployment configurations from development to production.
        </DocsParagraph>

        <DocsMermaid
          chart={`
graph TB
    subgraph Production["🚀 Production Deployment"]
        Internet["☁️ Internet"]
        Proxy["Reverse Proxy<br/>(Nginx/Traefik)<br/>Port 443 HTTPS"]
        FE["Frontend Container<br/>(Nginx Static)<br/>Port 80"]
        BE["Backend Container<br/>(FastAPI)<br/>Port 8000"]
        DBP[(Database<br/>PostgreSQL<br/>or SQLite)]

        Internet -->|HTTPS| Proxy
        Proxy -->|Static Files| FE
        Proxy -->|API /api/*| BE
        BE -->|SQL| DBP
    end

    subgraph Development["💻 Development Environment"]
        Dev["Developer Machine"]
        Vite["Vite Dev Server<br/>Port 5173<br/>Hot Reload"]
        Fast["FastAPI Server<br/>Port 8000<br/>Auto Reload"]
        DBS[(SQLite File<br/>greenstack.db)]

        Dev --> Vite
        Dev --> Fast
        Vite -.->|Proxy API| Fast
        Fast -->|SQL| DBS
    end

    style Production fill:#2d5016,stroke:#3DB60F,stroke-width:3px,color:#fff
    style Development fill:#1a1f3a,stroke:#3DB60F,stroke-width:3px,color:#fff
    style Proxy fill:#3a4060,stroke:#51cf66,color:#fff
    style FE fill:#3a4060,stroke:#51cf66,color:#fff
    style BE fill:#3a4060,stroke:#51cf66,color:#fff
    style Vite fill:#3a4060,stroke:#51cf66,color:#fff
    style Fast fill:#3a4060,stroke:#51cf66,color:#fff
          `}
        />
      </DocsSection>

      {/* Related Resources */}
      <DocsSection title="Related Resources">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-6">
          <DocsLink href="/docs/developer/backend" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Backend Development</h5>
            <p className="text-sm text-muted-foreground">Deep dive into FastAPI backend</p>
          </DocsLink>

          <DocsLink href="/docs/developer/frontend" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Frontend Development</h5>
            <p className="text-sm text-muted-foreground">React components and state management</p>
          </DocsLink>

          <DocsLink href="/docs/api/overview" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">API Overview</h5>
            <p className="text-sm text-muted-foreground">Complete API documentation</p>
          </DocsLink>

          <DocsLink href="/docs/deployment/production" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Production Deployment</h5>
            <p className="text-sm text-muted-foreground">Deploy Greenstack to production</p>
          </DocsLink>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
