import React from 'react';
import { Box, Code, FileText, Package } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink, DocsList } from '../../../components/docs/DocsText';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, Badge } from '../../../components/ui';

export const metadata = {
  id: 'components/ui-components',
  title: 'UI Components Reference',
  description: 'Complete technical reference for all Greenstack UI components with props, variants, and usage patterns',
  category: 'components',
  order: 3,
  keywords: ['ui', 'components', 'reference', 'api', 'props', 'documentation'],
  lastUpdated: '2025-01-17',
};

export default function UIComponents({ onNavigate }) {
  return (
    <DocsPage>
      <DocsHero
        title="UI Components Reference"
        description="Complete technical reference for all Greenstack UI components"
        icon={<Box className="w-12 h-12 text-brand-green" />}
      />

      {/* Overview */}
      <DocsSection title="Overview" icon={<Package />}>
        <DocsParagraph>
          This reference documents all UI components available in Greenstack, including their props,
          variants, and usage patterns. All components are exported from <code>./components/ui</code>.
        </DocsParagraph>

        <DocsCodeBlock language="javascript">
{`// Import components from the ui barrel export
import {
  Card,
  CardHeader,
  CardTitle,
  Button,
  Badge,
  Input,
  // ... and many more
} from './components/ui';`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Card Components */}
      <DocsSection title="Card Components" icon={<Box />}>
        <DocsParagraph>
          Card components provide flexible containers for grouping related content.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Card</CardTitle>
              <CardDescription>Main container component</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="typescript">
{`interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string;
}

<Card className="custom-class">
  {/* Card content */}
</Card>`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">CardHeader</CardTitle>
              <CardDescription>Container for card title and description</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="typescript">
{`interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string;
}

<CardHeader>
  <CardTitle>Title</CardTitle>
  <CardDescription>Description</CardDescription>
</CardHeader>`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">CardTitle</CardTitle>
              <CardDescription>Heading element for card title</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="typescript">
{`interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  className?: string;
}

<CardTitle>My Card Title</CardTitle>`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">CardDescription</CardTitle>
              <CardDescription>Subtitle or description text</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="typescript">
{`interface CardDescriptionProps extends React.HTMLAttributes<HTMLParagraphElement> {
  className?: string;
}

<CardDescription>Brief description of the card</CardDescription>`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">CardContent</CardTitle>
              <CardDescription>Main content area of the card</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="typescript">
{`interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string;
}

<CardContent>
  {/* Your main content */}
</CardContent>`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">CardFooter</CardTitle>
              <CardDescription>Footer area for actions or additional info</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="typescript">
{`interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string;
}

<CardFooter>
  <Button>Action</Button>
</CardFooter>`}
              </DocsCodeBlock>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Button */}
      <DocsSection title="Button">
        <DocsParagraph>
          Buttons trigger actions with multiple variants and sizes.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Props</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="typescript">
{`interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
  className?: string;
}

// Usage examples
<Button variant="default">Default Button</Button>
<Button variant="destructive" size="sm">Delete</Button>
<Button variant="outline" size="lg">Large Outline</Button>
<Button variant="ghost" size="icon"><Icon /></Button>`}
            </DocsCodeBlock>

            <div className="mt-4">
              <h4 className="font-semibold text-foreground mb-2">Variants</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Badge variant="outline">default</Badge> - Primary brand green background</li>
                <li><Badge variant="outline">destructive</Badge> - Red background for dangerous actions</li>
                <li><Badge variant="outline">outline</Badge> - Transparent with border</li>
                <li><Badge variant="outline">secondary</Badge> - Secondary color background</li>
                <li><Badge variant="outline">ghost</Badge> - Transparent background, hover effect only</li>
                <li><Badge variant="outline">link</Badge> - Styled as an underlined link</li>
              </ul>
            </div>

            <div className="mt-4">
              <h4 className="font-semibold text-foreground mb-2">Sizes</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Badge variant="outline">sm</Badge> - Small button (h-9 px-3)</li>
                <li><Badge variant="outline">default</Badge> - Default size (h-10 px-4)</li>
                <li><Badge variant="outline">lg</Badge> - Large button (h-11 px-8)</li>
                <li><Badge variant="outline">icon</Badge> - Square button for icons (h-10 w-10)</li>
              </ul>
            </div>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Badge */}
      <DocsSection title="Badge">
        <DocsParagraph>
          Badges display small pieces of information like status or counts.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Props</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="typescript">
{`interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'secondary' | 'destructive' | 'outline';
  className?: string;
}

// Usage examples
<Badge>Default Badge</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Error</Badge>
<Badge variant="outline">Outline</Badge>
<Badge className="bg-brand-green">Custom</Badge>`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Input */}
      <DocsSection title="Input">
        <DocsParagraph>
          Text input fields for forms and user data entry.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Props</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="typescript">
{`interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  className?: string;
}

// Usage examples
<Input type="text" placeholder="Enter text" />
<Input type="email" placeholder="email@example.com" />
<Input type="password" placeholder="Password" />
<Input type="number" min={0} max={100} />
<Input disabled placeholder="Disabled input" />`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Label */}
      <DocsSection title="Label">
        <DocsParagraph>
          Labels provide accessible descriptions for form inputs.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Props</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="typescript">
{`interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  className?: string;
}

// Usage example
<div className="space-y-2">
  <Label htmlFor="email">Email Address</Label>
  <Input id="email" type="email" />
</div>`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Alert */}
      <DocsSection title="Alert">
        <DocsParagraph>
          Alerts display important messages with optional variants.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Props</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="typescript">
{`interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'destructive';
  className?: string;
}

// Usage example
<Alert>
  <AlertCircle className="w-4 h-4" />
  <AlertTitle>Heads up!</AlertTitle>
  <AlertDescription>
    This is an important message.
  </AlertDescription>
</Alert>

<Alert variant="destructive">
  <AlertCircle className="w-4 h-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>
    Something went wrong.
  </AlertDescription>
</Alert>`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Progress */}
      <DocsSection title="Progress">
        <DocsParagraph>
          Progress bars visualize task completion.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Props</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="typescript">
{`interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number; // 0-100
  className?: string;
}

// Usage examples
<Progress value={0} />    // 0% complete
<Progress value={50} />   // 50% complete
<Progress value={100} />  // 100% complete`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Tabs */}
      <DocsSection title="Tabs">
        <DocsParagraph>
          Tabs organize content into separate views.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Components & Props</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="typescript">
{`// Tabs Root
interface TabsProps {
  defaultValue?: string;
  value?: string;
  onValueChange?: (value: string) => void;
}

// TabsList - Container for tab triggers
interface TabsListProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string;
}

// TabsTrigger - Individual tab button
interface TabsTriggerProps {
  value: string;
  disabled?: boolean;
  className?: string;
}

// TabsContent - Content panel for a tab
interface TabsContentProps {
  value: string;
  className?: string;
}

// Usage example
<Tabs defaultValue="tab1">
  <TabsList>
    <TabsTrigger value="tab1">Tab 1</TabsTrigger>
    <TabsTrigger value="tab2">Tab 2</TabsTrigger>
  </TabsList>
  <TabsContent value="tab1">
    Content for tab 1
  </TabsContent>
  <TabsContent value="tab2">
    Content for tab 2
  </TabsContent>
</Tabs>`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Switch */}
      <DocsSection title="Switch">
        <DocsParagraph>
          Toggle switches for boolean settings.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Props</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="typescript">
{`interface SwitchProps {
  checked?: boolean;
  defaultChecked?: boolean;
  onCheckedChange?: (checked: boolean) => void;
  disabled?: boolean;
  className?: string;
}

// Controlled usage
const [enabled, setEnabled] = useState(false);
<Switch checked={enabled} onCheckedChange={setEnabled} />

// Uncontrolled usage
<Switch defaultChecked={true} />`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Dialog */}
      <DocsSection title="Dialog">
        <DocsParagraph>
          Modal dialogs for focused user interactions.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Components & Props</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="typescript">
{`// Dialog Root
interface DialogProps {
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
}

// Usage example
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogTrigger asChild>
    <Button>Open Dialog</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Dialog Title</DialogTitle>
      <DialogDescription>
        Dialog description goes here
      </DialogDescription>
    </DialogHeader>
    {/* Dialog content */}
    <DialogFooter>
      <Button variant="outline" onClick={() => setIsOpen(false)}>
        Cancel
      </Button>
      <Button onClick={handleSave}>Save</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Select */}
      <DocsSection title="Select">
        <DocsParagraph>
          Dropdown select menus for choosing from options.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Components & Props</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="typescript">
{`// Select Root
interface SelectProps {
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
  disabled?: boolean;
}

// Usage example
<Select value={value} onValueChange={setValue}>
  <SelectTrigger>
    <SelectValue placeholder="Select an option" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="option1">Option 1</SelectItem>
    <SelectItem value="option2">Option 2</SelectItem>
    <SelectItem value="option3">Option 3</SelectItem>
  </SelectContent>
</Select>`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* ScrollArea */}
      <DocsSection title="ScrollArea">
        <DocsParagraph>
          Custom scrollable areas with styled scrollbars.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Props</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="typescript">
{`interface ScrollAreaProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string;
}

// Usage example
<ScrollArea className="h-72 w-full rounded-md border">
  <div className="p-4">
    {/* Your scrollable content */}
  </div>
</ScrollArea>`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Separator */}
      <DocsSection title="Separator">
        <DocsParagraph>
          Visual dividers between content sections.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Props</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="typescript">
{`interface SeparatorProps extends React.HTMLAttributes<HTMLDivElement> {
  orientation?: 'horizontal' | 'vertical';
  decorative?: boolean;
  className?: string;
}

// Horizontal separator (default)
<Separator />

// Vertical separator
<Separator orientation="vertical" />`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Skeleton */}
      <DocsSection title="Skeleton">
        <DocsParagraph>
          Loading placeholders for content.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Props</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="typescript">
{`interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  className?: string;
}

// Usage examples
<Skeleton className="h-12 w-12 rounded-full" />
<Skeleton className="h-4 w-[250px]" />
<Skeleton className="h-4 w-[200px]" />`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Additional Information */}
      <DocsSection title="Additional Components">
        <DocsParagraph>
          Greenstack includes additional components from Radix UI that are not shown here:
        </DocsParagraph>

        <Card className="my-6">
          <CardContent className="pt-6">
            <DocsList>
              <li><strong>Dropdown Menu:</strong> Context menus with nested items and actions</li>
              <li><strong>Tooltip:</strong> Hover tooltips for additional information</li>
              <li><strong>Toast:</strong> Notification messages that appear temporarily</li>
              <li><strong>Alert Dialog:</strong> Modal alerts requiring user confirmation</li>
              <li><strong>Sheet:</strong> Slide-out panels from screen edges</li>
            </DocsList>

            <p className="text-sm text-muted-foreground mt-4">
              For complete documentation on these components, refer to the{' '}
              <DocsLink href="https://www.radix-ui.com/primitives/docs/overview/introduction" external>
                Radix UI documentation
              </DocsLink>.
            </p>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Styling & Customization */}
      <DocsSection title="Styling & Customization" icon={<Code />}>
        <DocsParagraph>
          All components accept a <code>className</code> prop for custom styling. Use Tailwind CSS
          classes or custom CSS to override default styles:
        </DocsParagraph>

        <DocsCodeBlock language="jsx">
{`// Using Tailwind classes
<Button className="bg-brand-green hover:bg-brand-green/90">
  Custom Green Button
</Button>

// Multiple custom classes
<Card className="border-2 border-brand-green shadow-xl">
  Custom styled card
</Card>

// Combining with theme colors
<Badge className="bg-success text-white">
  Success Badge
</Badge>`}
        </DocsCodeBlock>

        <DocsCallout type="info" title="Theme Integration">
          <DocsParagraph>
            All components automatically adapt to the active theme. Theme colors are available
            as CSS variables and Tailwind classes (e.g., <code>text-brand-green</code>,
            <code>bg-surface</code>, <code>border-border</code>).
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      {/* Related Resources */}
      <DocsSection title="Related Resources">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-6">
          <DocsLink href="/docs/components/gallery" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Component Gallery</h5>
            <p className="text-sm text-muted-foreground">Interactive examples of all components</p>
          </DocsLink>

          <DocsLink href="/docs/components/theme-system" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Theme System</h5>
            <p className="text-sm text-muted-foreground">Customize component appearance</p>
          </DocsLink>

          <DocsLink href="/docs/developer/frontend" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Frontend Development</h5>
            <p className="text-sm text-muted-foreground">Build features with components</p>
          </DocsLink>

          <DocsLink href="https://www.radix-ui.com/primitives/docs/overview/introduction" external className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Radix UI Docs</h5>
            <p className="text-sm text-muted-foreground">Component primitive documentation</p>
          </DocsLink>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
