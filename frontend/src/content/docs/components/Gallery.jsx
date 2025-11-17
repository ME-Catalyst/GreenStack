import React, { useState } from 'react';
import { Grid, Sparkles, Package, Check, AlertCircle, Info } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
  Button,
  Badge,
  Input,
  Label,
  Alert,
  AlertTitle,
  AlertDescription,
  Progress,
  Separator,
  Tabs,
  TabsList,
  TabsTrigger,
  TabsContent,
  Switch,
  Skeleton,
} from '../../../components/ui';

export const metadata = {
  id: 'components/gallery',
  title: 'Component Gallery',
  description: 'Interactive showcase of all Greenstack UI components with live examples and code snippets',
  category: 'components',
  order: 1,
  keywords: ['components', 'ui', 'library', 'showcase', 'examples', 'interactive'],
  lastUpdated: '2025-01-17',
};

export default function Gallery({ onNavigate }) {
  const [progressValue, setProgressValue] = useState(65);
  const [switchChecked, setSwitchChecked] = useState(false);

  return (
    <DocsPage>
      <DocsHero
        title="Component Gallery"
        description="Interactive showcase of all Greenstack UI components"
        icon={<Grid className="w-12 h-12 text-brand-green" />}
      />

      {/* Overview */}
      <DocsSection title="Overview" icon={<Sparkles />}>
        <DocsParagraph>
          Greenstack provides a comprehensive library of UI components built on top of{' '}
          <DocsLink href="https://www.radix-ui.com/" external>Radix UI</DocsLink> primitives,
          styled with Tailwind CSS and integrated with the theme system. All components are
          accessible, responsive, and fully customizable.
        </DocsParagraph>

        <div className="grid gap-4 md:grid-cols-3 my-6">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 mb-2">
                <Check className="w-5 h-5 text-brand-green" />
                <h4 className="font-semibold text-foreground">Accessible</h4>
              </div>
              <p className="text-sm text-muted-foreground">
                WCAG compliant with keyboard navigation and screen reader support
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 mb-2">
                <Check className="w-5 h-5 text-brand-green" />
                <h4 className="font-semibold text-foreground">Theme-Aware</h4>
              </div>
              <p className="text-sm text-muted-foreground">
                Automatically adapt to active theme with consistent styling
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 mb-2">
                <Check className="w-5 h-5 text-brand-green" />
                <h4 className="font-semibold text-foreground">Composable</h4>
              </div>
              <p className="text-sm text-muted-foreground">
                Mix and match components to build complex interfaces
              </p>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Cards */}
      <DocsSection title="Cards" icon={<Package />}>
        <DocsParagraph>
          Cards are flexible containers for grouping related content. They support headers,
          content areas, descriptions, and footers.
        </DocsParagraph>

        <div className="grid gap-4 md:grid-cols-2 my-6">
          <Card>
            <CardHeader>
              <CardTitle>Basic Card</CardTitle>
              <CardDescription>A simple card with title and description</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Card content goes here. You can put any content inside a card component.
              </p>
            </CardContent>
            <CardFooter>
              <Button size="sm">Action</Button>
            </CardFooter>
          </Card>

          <Card className="border-brand-green shadow-lg shadow-brand-green/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Check className="w-5 h-5 text-brand-green" />
                Featured Card
              </CardTitle>
              <CardDescription>Card with custom styling and icon</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Cards can be customized with borders, shadows, and theme colors.
              </p>
            </CardContent>
          </Card>
        </div>

        <DocsCodeBlock language="jsx">
{`import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Button } from './components/ui';

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description goes here</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Your content here</p>
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Buttons */}
      <DocsSection title="Buttons">
        <DocsParagraph>
          Buttons trigger actions and come in multiple variants and sizes to match different use cases.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Button Variants</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-3">
              <Button variant="default">Default</Button>
              <Button variant="secondary">Secondary</Button>
              <Button variant="outline">Outline</Button>
              <Button variant="ghost">Ghost</Button>
              <Button variant="destructive">Destructive</Button>
              <Button variant="link">Link</Button>
            </div>
          </CardContent>
        </Card>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Button Sizes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap items-center gap-3">
              <Button size="sm">Small</Button>
              <Button size="default">Default</Button>
              <Button size="lg">Large</Button>
              <Button size="icon">
                <Check className="w-4 h-4" />
              </Button>
            </div>
          </CardContent>
        </Card>

        <DocsCodeBlock language="jsx">
{`import { Button } from './components/ui';

// Variants
<Button variant="default">Default</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="destructive">Destructive</Button>

// Sizes
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
<Button size="icon"><Icon /></Button>`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Badges */}
      <DocsSection title="Badges">
        <DocsParagraph>
          Badges display small pieces of information like status, counts, or labels.
        </DocsParagraph>

        <Card className="my-6">
          <CardContent className="pt-6">
            <div className="flex flex-wrap gap-3">
              <Badge variant="default">Default</Badge>
              <Badge variant="secondary">Secondary</Badge>
              <Badge variant="outline">Outline</Badge>
              <Badge variant="destructive">Destructive</Badge>
              <Badge className="bg-brand-green text-white">Custom</Badge>
            </div>
          </CardContent>
        </Card>

        <DocsCodeBlock language="jsx">
{`import { Badge } from './components/ui';

<Badge variant="default">Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="outline">Outline</Badge>
<Badge variant="destructive">Destructive</Badge>
<Badge className="bg-brand-green text-white">Custom</Badge>`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Alerts */}
      <DocsSection title="Alerts">
        <DocsParagraph>
          Alerts display important messages and notifications with different severity levels.
        </DocsParagraph>

        <div className="space-y-4 my-6">
          <Alert>
            <Info className="w-4 h-4" />
            <AlertTitle>Information</AlertTitle>
            <AlertDescription>
              This is an informational alert message with default styling.
            </AlertDescription>
          </Alert>

          <Alert className="bg-success/10 border-success/50">
            <Check className="w-4 h-4 text-success" />
            <AlertTitle className="text-success">Success</AlertTitle>
            <AlertDescription className="text-foreground">
              Operation completed successfully! Your changes have been saved.
            </AlertDescription>
          </Alert>

          <Alert className="bg-warning/10 border-warning/50">
            <AlertCircle className="w-4 h-4 text-warning" />
            <AlertTitle className="text-warning">Warning</AlertTitle>
            <AlertDescription className="text-foreground">
              Please review this warning before proceeding with the action.
            </AlertDescription>
          </Alert>

          <Alert variant="destructive">
            <AlertCircle className="w-4 h-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>
              An error occurred while processing your request. Please try again.
            </AlertDescription>
          </Alert>
        </div>

        <DocsCodeBlock language="jsx">
{`import { Alert, AlertTitle, AlertDescription } from './components/ui';

<Alert>
  <Info className="w-4 h-4" />
  <AlertTitle>Information</AlertTitle>
  <AlertDescription>Your message here</AlertDescription>
</Alert>

<Alert variant="destructive">
  <AlertCircle className="w-4 h-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Error message here</AlertDescription>
</Alert>`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Form Inputs */}
      <DocsSection title="Form Inputs">
        <DocsParagraph>
          Form inputs allow users to enter data with proper labels and styling.
        </DocsParagraph>

        <Card className="my-6">
          <CardContent className="pt-6 space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <Input id="name" placeholder="Enter your name" />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" placeholder="email@example.com" />
            </div>

            <div className="space-y-2">
              <Label htmlFor="disabled">Disabled Input</Label>
              <Input id="disabled" placeholder="Disabled" disabled />
            </div>
          </CardContent>
        </Card>

        <DocsCodeBlock language="jsx">
{`import { Input, Label } from './components/ui';

<div className="space-y-2">
  <Label htmlFor="name">Name</Label>
  <Input id="name" placeholder="Enter your name" />
</div>

<Input type="email" placeholder="email@example.com" />
<Input disabled placeholder="Disabled input" />`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Progress */}
      <DocsSection title="Progress">
        <DocsParagraph>
          Progress bars visualize the completion status of tasks or operations.
        </DocsParagraph>

        <Card className="my-6">
          <CardContent className="pt-6 space-y-6">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm text-muted-foreground">Progress: {progressValue}%</span>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setProgressValue(Math.min(100, progressValue + 10))}
                >
                  +10%
                </Button>
              </div>
              <Progress value={progressValue} />
            </div>

            <Separator />

            <div>
              <p className="text-sm text-muted-foreground mb-2">Loading states:</p>
              <div className="space-y-3">
                <Progress value={25} />
                <Progress value={50} />
                <Progress value={75} />
                <Progress value={100} />
              </div>
            </div>
          </CardContent>
        </Card>

        <DocsCodeBlock language="jsx">
{`import { Progress } from './components/ui';

<Progress value={65} />
<Progress value={100} />`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Tabs */}
      <DocsSection title="Tabs">
        <DocsParagraph>
          Tabs organize content into separate views that users can switch between.
        </DocsParagraph>

        <Card className="my-6">
          <CardContent className="pt-6">
            <Tabs defaultValue="overview">
              <TabsList>
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="details">Details</TabsTrigger>
                <TabsTrigger value="settings">Settings</TabsTrigger>
              </TabsList>
              <TabsContent value="overview" className="space-y-4">
                <h4 className="font-semibold text-foreground">Overview Tab</h4>
                <p className="text-sm text-muted-foreground">
                  This is the overview tab content. You can put any components or content here.
                </p>
              </TabsContent>
              <TabsContent value="details" className="space-y-4">
                <h4 className="font-semibold text-foreground">Details Tab</h4>
                <p className="text-sm text-muted-foreground">
                  Detailed information goes in this tab. Each tab can have completely different content.
                </p>
              </TabsContent>
              <TabsContent value="settings" className="space-y-4">
                <h4 className="font-semibold text-foreground">Settings Tab</h4>
                <p className="text-sm text-muted-foreground">
                  Settings and configuration options would be displayed here.
                </p>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>

        <DocsCodeBlock language="jsx">
{`import { Tabs, TabsList, TabsTrigger, TabsContent } from './components/ui';

<Tabs defaultValue="overview">
  <TabsList>
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="details">Details</TabsTrigger>
  </TabsList>
  <TabsContent value="overview">
    Overview content
  </TabsContent>
  <TabsContent value="details">
    Details content
  </TabsContent>
</Tabs>`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Switch */}
      <DocsSection title="Switch">
        <DocsParagraph>
          Switches toggle between two states, typically on/off or enabled/disabled.
        </DocsParagraph>

        <Card className="my-6">
          <CardContent className="pt-6 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label htmlFor="switch-1" className="text-base">Enable Notifications</Label>
                <p className="text-sm text-muted-foreground">
                  Receive notifications about important updates
                </p>
              </div>
              <Switch id="switch-1" checked={switchChecked} onCheckedChange={setSwitchChecked} />
            </div>

            <Separator />

            <div className="flex items-center justify-between">
              <div>
                <Label htmlFor="switch-2" className="text-base">Dark Mode</Label>
                <p className="text-sm text-muted-foreground">
                  Use dark theme throughout the application
                </p>
              </div>
              <Switch id="switch-2" defaultChecked />
            </div>
          </CardContent>
        </Card>

        <DocsCodeBlock language="jsx">
{`import { Switch, Label } from './components/ui';

const [checked, setChecked] = useState(false);

<div className="flex items-center space-x-2">
  <Switch id="airplane-mode" checked={checked} onCheckedChange={setChecked} />
  <Label htmlFor="airplane-mode">Airplane Mode</Label>
</div>`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Skeleton */}
      <DocsSection title="Skeleton">
        <DocsParagraph>
          Skeleton loaders provide visual placeholders while content is loading.
        </DocsParagraph>

        <Card className="my-6">
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div className="space-y-2">
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-4 w-1/2" />
              </div>
              <Skeleton className="h-32 w-full" />
              <div className="flex gap-2">
                <Skeleton className="h-10 w-20" />
                <Skeleton className="h-10 w-20" />
              </div>
            </div>
          </CardContent>
        </Card>

        <DocsCodeBlock language="jsx">
{`import { Skeleton } from './components/ui';

<div className="space-y-2">
  <Skeleton className="h-4 w-3/4" />
  <Skeleton className="h-4 w-1/2" />
  <Skeleton className="h-32 w-full" />
</div>`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Separator */}
      <DocsSection title="Separator">
        <DocsParagraph>
          Separators create visual division between content sections.
        </DocsParagraph>

        <Card className="my-6">
          <CardContent className="pt-6">
            <div>
              <p className="text-sm text-muted-foreground">Content above separator</p>
              <Separator className="my-4" />
              <p className="text-sm text-muted-foreground">Content below separator</p>
            </div>

            <div className="flex h-20 items-center my-6">
              <p className="text-sm text-muted-foreground">Left content</p>
              <Separator orientation="vertical" className="mx-4" />
              <p className="text-sm text-muted-foreground">Right content</p>
            </div>
          </CardContent>
        </Card>

        <DocsCodeBlock language="jsx">
{`import { Separator } from './components/ui';

// Horizontal separator (default)
<Separator />

// Vertical separator
<Separator orientation="vertical" />`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Related Resources */}
      <DocsSection title="Related Resources">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-6">
          <DocsLink href="/docs/components/ui-components" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">UI Components Reference</h5>
            <p className="text-sm text-muted-foreground">Complete API documentation for all components</p>
          </DocsLink>

          <DocsLink href="/docs/components/theme-system" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Theme System</h5>
            <p className="text-sm text-muted-foreground">Customize component appearance with themes</p>
          </DocsLink>

          <DocsLink href="/docs/developer/frontend" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Frontend Development</h5>
            <p className="text-sm text-muted-foreground">Build features with Greenstack components</p>
          </DocsLink>

          <DocsLink href="https://www.radix-ui.com/primitives/docs/overview/introduction" external className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Radix UI Documentation</h5>
            <p className="text-sm text-muted-foreground">Learn about underlying component primitives</p>
          </DocsLink>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
