import React from 'react';
import { AlertTriangle, Bug, Code, Info, XCircle, AlertCircle } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, Badge } from '../../../components/ui';

export const metadata = {
  id: 'api/errors',
  title: 'Error Handling',
  description: 'Understanding API error codes, responses, and debugging techniques',
  category: 'api-reference',
  order: 4,
  keywords: ['errors', 'exceptions', 'debugging', 'http', 'status-codes', 'troubleshooting'],
  lastUpdated: '2025-01-17',
};

export default function Errors({ onNavigate }) {
  return (
    <DocsPage>
      <DocsHero
        title="API Error Handling"
        description="Comprehensive guide to understanding and resolving API errors in Greenstack"
        icon={<AlertTriangle className="w-12 h-12 text-brand-green" />}
      />

      {/* Error Response Format */}
      <DocsSection title="Error Response Format" icon={<Code />}>
        <DocsParagraph>
          All API errors follow a consistent JSON response format that includes the HTTP status code,
          error type, and detailed message to help you debug issues quickly.
        </DocsParagraph>

        <DocsCodeBlock language="json">
{`// Standard Error Response
{
  "detail": "Error message describing what went wrong",
  "status": 400,
  "type": "validation_error"
}`}
        </DocsCodeBlock>

        <DocsParagraph className="mt-4">
          For validation errors with multiple fields, the response includes a detailed breakdown:
        </DocsParagraph>

        <DocsCodeBlock language="json">
{`// Validation Error Response
{
  "detail": [
    {
      "loc": ["body", "vendor_id"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "device_id"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}`}
        </DocsCodeBlock>
      </DocsSection>

      {/* HTTP Status Codes */}
      <DocsSection title="HTTP Status Codes" icon={<Info />}>
        <DocsParagraph>
          Greenstack uses standard HTTP status codes to indicate the success or failure of API requests:
        </DocsParagraph>

        <div className="grid gap-4 my-6">
          {/* 2xx Success */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Badge className="bg-green-500/10 text-green-500 border-green-500/20">2xx</Badge>
                Success Responses
              </CardTitle>
              <CardDescription>Request completed successfully</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">200 OK</code>
                  </div>
                  <p className="text-sm text-muted-foreground ml-6">
                    Request succeeded. Response includes requested data.
                  </p>
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">201 Created</code>
                  </div>
                  <p className="text-sm text-muted-foreground ml-6">
                    Resource successfully created (IODD upload, device creation).
                  </p>
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">204 No Content</code>
                  </div>
                  <p className="text-sm text-muted-foreground ml-6">
                    Request succeeded with no response body (DELETE operations).
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* 4xx Client Errors */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Badge className="bg-yellow-500/10 text-yellow-500 border-yellow-500/20">4xx</Badge>
                Client Error Responses
              </CardTitle>
              <CardDescription>Problem with the request</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">400 Bad Request</code>
                  </div>
                  <p className="text-sm text-muted-foreground ml-6">
                    Invalid request format or missing required parameters.
                  </p>
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">404 Not Found</code>
                  </div>
                  <p className="text-sm text-muted-foreground ml-6">
                    Requested resource (device, IODD file) does not exist.
                  </p>
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">409 Conflict</code>
                  </div>
                  <p className="text-sm text-muted-foreground ml-6">
                    Resource already exists or duplicate operation attempted.
                  </p>
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">422 Unprocessable Entity</code>
                  </div>
                  <p className="text-sm text-muted-foreground ml-6">
                    Request syntax is correct but validation failed.
                  </p>
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">429 Too Many Requests</code>
                  </div>
                  <p className="text-sm text-muted-foreground ml-6">
                    Rate limit exceeded. Wait before retrying.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* 5xx Server Errors */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Badge className="bg-red-500/10 text-red-500 border-red-500/20">5xx</Badge>
                Server Error Responses
              </CardTitle>
              <CardDescription>Problem on the server side</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">500 Internal Server Error</code>
                  </div>
                  <p className="text-sm text-muted-foreground ml-6">
                    Unexpected error on the server. Check logs for details.
                  </p>
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">503 Service Unavailable</code>
                  </div>
                  <p className="text-sm text-muted-foreground ml-6">
                    Server temporarily unavailable (maintenance, overload).
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Common Error Scenarios */}
      <DocsSection title="Common Error Scenarios" icon={<AlertCircle />}>
        <DocsParagraph>
          Here are the most common errors you'll encounter and how to resolve them:
        </DocsParagraph>

        <div className="space-y-6 my-6">
          {/* File Upload Errors */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <XCircle className="w-4 h-4 text-warning" />
                File Upload Errors
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold text-foreground mb-2">Invalid file type</h4>
                <DocsCodeBlock language="json">
{`{
  "detail": "Invalid file type. Only .zip, .xml, or .eds files are allowed"
}`}
                </DocsCodeBlock>
                <DocsParagraph className="mt-2">
                  <strong>Solution:</strong> Ensure you're uploading IODD files in ZIP, XML, or EDS format.
                  Check file extension and MIME type.
                </DocsParagraph>
              </div>

              <div>
                <h4 className="font-semibold text-foreground mb-2">File too large</h4>
                <DocsCodeBlock language="json">
{`{
  "detail": "File size exceeds maximum allowed (10MB)"
}`}
                </DocsCodeBlock>
                <DocsParagraph className="mt-2">
                  <strong>Solution:</strong> Reduce file size or increase <code>MAX_UPLOAD_SIZE</code> in
                  server configuration.
                </DocsParagraph>
              </div>

              <div>
                <h4 className="font-semibold text-foreground mb-2">Invalid IODD format</h4>
                <DocsCodeBlock language="json">
{`{
  "detail": "Failed to parse IODD file: Invalid XML structure"
}`}
                </DocsCodeBlock>
                <DocsParagraph className="mt-2">
                  <strong>Solution:</strong> Verify IODD file is valid XML and conforms to IO-Link specification.
                  Check for syntax errors or missing required elements.
                </DocsParagraph>
              </div>
            </CardContent>
          </Card>

          {/* Database Errors */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <XCircle className="w-4 h-4 text-warning" />
                Database Errors
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold text-foreground mb-2">Resource not found</h4>
                <DocsCodeBlock language="json">
{`{
  "detail": "Device not found with ID: 12345"
}`}
                </DocsCodeBlock>
                <DocsParagraph className="mt-2">
                  <strong>Solution:</strong> Verify the resource ID exists. Use GET endpoints to list
                  available resources first.
                </DocsParagraph>
              </div>

              <div>
                <h4 className="font-semibold text-foreground mb-2">Duplicate resource</h4>
                <DocsCodeBlock language="json">
{`{
  "detail": "Device with vendor_id=310 and device_id=1234 already exists"
}`}
                </DocsCodeBlock>
                <DocsParagraph className="mt-2">
                  <strong>Solution:</strong> Resource already exists. Use PUT to update instead, or
                  check if the resource was already created.
                </DocsParagraph>
              </div>

              <div>
                <h4 className="font-semibold text-foreground mb-2">Database locked</h4>
                <DocsCodeBlock language="json">
{`{
  "detail": "Database is locked. Please retry.",
  "status": 503
}`}
                </DocsCodeBlock>
                <DocsParagraph className="mt-2">
                  <strong>Solution:</strong> SQLite database is locked by another process. Wait and retry,
                  or consider using PostgreSQL for production with higher concurrency.
                </DocsParagraph>
              </div>
            </CardContent>
          </Card>

          {/* Rate Limiting */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <XCircle className="w-4 h-4 text-warning" />
                Rate Limiting
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div>
                <h4 className="font-semibold text-foreground mb-2">Too many requests</h4>
                <DocsCodeBlock language="json">
{`{
  "detail": "Rate limit exceeded: 10 per 1 minute"
}`}
                </DocsCodeBlock>
                <DocsParagraph className="mt-2">
                  <strong>Solution:</strong> You've exceeded the rate limit (10 requests/minute for uploads,
                  100/minute for general endpoints). Wait before retrying or implement exponential backoff
                  in your client.
                </DocsParagraph>
              </div>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Debugging Tips */}
      <DocsSection title="Debugging Tips" icon={<Bug />}>
        <DocsParagraph>
          When encountering errors, follow these debugging steps to quickly identify and resolve issues:
        </DocsParagraph>

        <Card className="my-6">
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  1
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Check the Error Response</h4>
                  <p className="text-sm text-muted-foreground">
                    Read the <code>detail</code> field carefully. It usually contains specific information
                    about what went wrong and how to fix it.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  2
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Inspect Server Logs</h4>
                  <p className="text-sm text-muted-foreground">
                    Check the backend console for detailed stack traces and error messages.
                    Enable debug logging with <code>LOG_LEVEL=DEBUG</code>.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  3
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Use API Documentation</h4>
                  <p className="text-sm text-muted-foreground">
                    Visit <code>http://localhost:8000/docs</code> to see interactive API documentation
                    with request/response schemas and try requests directly.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  4
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Verify Request Format</h4>
                  <p className="text-sm text-muted-foreground">
                    Ensure your request includes required headers (<code>Content-Type: application/json</code>
                    or <code>multipart/form-data</code>) and all required fields.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  5
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Test with curl or Postman</h4>
                  <p className="text-sm text-muted-foreground">
                    Isolate the issue by testing the API endpoint directly with curl or Postman
                    to rule out client-side problems.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-green/10 flex items-center justify-center text-brand-green font-bold">
                  6
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-foreground mb-1">Check Database State</h4>
                  <p className="text-sm text-muted-foreground">
                    Use the Admin Console to inspect database contents and verify data integrity.
                    Navigate to Tools → Admin Console.
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <DocsCallout type="info" title="Development Mode">
          <DocsParagraph>
            When running in development mode, the API returns detailed stack traces in error responses
            to help with debugging. In production, these are sanitized for security.
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      {/* Example Error Handling Code */}
      <DocsSection title="Error Handling in Your Code">
        <DocsParagraph>
          Here's how to handle API errors gracefully in your client application:
        </DocsParagraph>

        <DocsCodeBlock language="javascript">
{`// JavaScript/TypeScript example
async function uploadIODD(file) {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:8000/api/iodds/upload', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();

      // Handle specific error types
      if (response.status === 429) {
        console.error('Rate limit exceeded. Retry after 1 minute.');
        // Implement retry logic with backoff
      } else if (response.status === 422) {
        console.error('Validation error:', error.detail);
        // Show field-specific errors to user
      } else {
        console.error('API error:', error.detail);
      }

      throw new Error(error.detail);
    }

    const data = await response.json();
    return data;

  } catch (error) {
    console.error('Upload failed:', error.message);
    throw error;
  }
}`}
        </DocsCodeBlock>

        <DocsCodeBlock language="python" className="mt-4">
{`# Python example
import requests
from time import sleep

def upload_iodd(file_path):
    url = 'http://localhost:8000/api/iodds/upload'

    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        error_detail = e.response.json().get('detail', str(e))

        # Handle rate limiting with retry
        if e.response.status_code == 429:
            print('Rate limit exceeded. Waiting 60 seconds...')
            sleep(60)
            return upload_iodd(file_path)  # Retry

        # Handle validation errors
        elif e.response.status_code == 422:
            print(f'Validation error: {error_detail}')

        else:
            print(f'API error ({e.response.status_code}): {error_detail}')

        raise

    except requests.exceptions.RequestException as e:
        print(f'Request failed: {str(e)}')
        raise`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Related Resources */}
      <DocsSection title="Related Resources">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-6">
          <DocsLink href="/docs/api/overview" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">API Overview</h5>
            <p className="text-sm text-muted-foreground">Learn about the REST API structure</p>
          </DocsLink>

          <DocsLink href="/docs/api/endpoints" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">API Endpoints</h5>
            <p className="text-sm text-muted-foreground">Complete endpoint reference</p>
          </DocsLink>

          <DocsLink href="/docs/api/authentication" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Authentication & Security</h5>
            <p className="text-sm text-muted-foreground">API security and rate limiting</p>
          </DocsLink>

          <DocsLink href="/docs/user-guide/troubleshooting" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Troubleshooting Guide</h5>
            <p className="text-sm text-muted-foreground">Common issues and solutions</p>
          </DocsLink>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
