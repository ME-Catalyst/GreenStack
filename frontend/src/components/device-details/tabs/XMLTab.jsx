import React from 'react';
import {
  Card, CardHeader, CardContent, CardTitle, Button, TabsContent, ScrollArea, Skeleton
} from '@/components/ui';
import {
  Code2, Copy
} from 'lucide-react';


export const XMLTab = ({ device, xmlContent, loadingXml, fetchXml }) => {
  return (
              <TabsContent value="xml" className="space-y-4 mt-6">
            <Card className="bg-card/80 backdrop-blur-sm border-border">
              <CardHeader>
                <CardTitle className="text-foreground text-xl flex items-center gap-2">
                  <FileCode className="w-5 h-5 text-success" />
                  IODD XML Source
                </CardTitle>
                <CardDescription className="text-muted-foreground">
                  View the raw XML definition for this device
                </CardDescription>
              </CardHeader>
              <CardContent>
                {loadingXml ? (
                  <div className="flex items-center justify-center py-12">
                    <div className="text-muted-foreground">Loading XML...</div>
                  </div>
                ) : xmlContent ? (
                  <div className="relative">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        navigator.clipboard.writeText(xmlContent);
                        toast({
                          title: 'Copied to clipboard',
                          description: 'XML content copied successfully',
                        });
                      }}
                      className="absolute top-2 right-2 z-10 border-border text-foreground hover:bg-secondary"
                    >
                      <Copy className="w-4 h-4 mr-2" />
                      Copy
                    </Button>
                    <div className="h-[600px] w-full rounded-lg border border-border bg-background overflow-auto">
                      <pre className="p-4 text-xs font-mono text-success whitespace-pre-wrap break-words">
                        {xmlContent}
                      </pre>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-12 text-muted-foreground">
                    No XML content available
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

  );
};
