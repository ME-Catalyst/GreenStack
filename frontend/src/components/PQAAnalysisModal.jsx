import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription,
  Card, CardContent, CardHeader, CardTitle,
  Badge, Button, Progress, Tabs, TabsContent, TabsList, TabsTrigger
} from '@/components/ui';
import {
  AlertTriangle, CheckCircle, XCircle, TrendingUp, TrendingDown,
  Activity, Database, FileCode, GitCompare, Eye, Download, ExternalLink
} from 'lucide-react';

/**
 * PQA Analysis Modal - displays detailed quality metrics for a specific analysis
 */
const PQAAnalysisModal = ({ isOpen, onClose, metricId, API_BASE, toast }) => {
  const [loading, setLoading] = useState(true);
  const [metrics, setMetrics] = useState(null);
  const [diffItems, setDiffItems] = useState([]);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    if (isOpen && metricId) {
      loadAnalysisData();
    }
  }, [isOpen, metricId]);

  const loadAnalysisData = async () => {
    setLoading(true);
    try {
      const [metricsRes, diffsRes] = await Promise.all([
        axios.get(`${API_BASE}/api/pqa/metrics/by-id/${metricId}`),
        axios.get(`${API_BASE}/api/pqa/diff/${metricId}`)
      ]);

      setMetrics(metricsRes.data);
      setDiffItems(diffsRes.data || []);
    } catch (error) {
      console.error('Failed to load PQA analysis:', error);
      toast?.({
        title: 'Load Error',
        description: 'Failed to load PQA analysis details',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'CRITICAL': return 'text-error border-error bg-error/10';
      case 'HIGH': return 'text-warning border-warning bg-warning/10';
      case 'MEDIUM': return 'text-yellow-500 border-yellow-500 bg-yellow-500/10';
      case 'LOW': return 'text-blue-500 border-blue-500 bg-blue-500/10';
      default: return 'text-muted-foreground border-border bg-muted';
    }
  };

  const getDiffTypeIcon = (diffType) => {
    switch (diffType) {
      case 'MISSING': return <XCircle className="w-4 h-4" />;
      case 'ADDED': return <CheckCircle className="w-4 h-4" />;
      case 'MODIFIED': return <GitCompare className="w-4 h-4" />;
      default: return <Activity className="w-4 h-4" />;
    }
  };

  if (!isOpen) return null;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-5xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-brand-green" />
            Parser Quality Analysis
          </DialogTitle>
          <DialogDescription>
            Detailed quality metrics and differences for parsed file
          </DialogDescription>
        </DialogHeader>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="text-muted-foreground">Loading analysis...</div>
          </div>
        ) : metrics ? (
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="differences">
                Differences ({diffItems.length})
              </TabsTrigger>
              <TabsTrigger value="details">Details</TabsTrigger>
            </TabsList>

            {/* Overview Tab */}
            <TabsContent value="overview" className="space-y-4 mt-4">
              {/* Score Summary Card */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>Overall Quality Score</span>
                    <Badge
                      className={`text-lg px-4 py-1 ${
                        metrics.passed_threshold
                          ? 'bg-success/20 text-success border-success/50'
                          : metrics.critical_data_loss
                            ? 'bg-error/20 text-error border-error/50'
                            : 'bg-warning/20 text-warning border-warning/50'
                      }`}
                    >
                      {metrics.overall_score.toFixed(1)}%
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-muted-foreground">Status</span>
                    <Badge className={metrics.passed_threshold ? 'bg-success/20 text-success' : 'bg-error/20 text-error'}>
                      {metrics.passed_threshold ? (
                        <>
                          <CheckCircle className="w-4 h-4 mr-1" />
                          PASS
                        </>
                      ) : (
                        <>
                          <XCircle className="w-4 h-4 mr-1" />
                          FAIL
                        </>
                      )}
                    </Badge>
                  </div>
                  {metrics.critical_data_loss && (
                    <div className="flex items-center gap-2 p-3 bg-error/10 border border-error/50 rounded-lg">
                      <AlertTriangle className="w-5 h-5 text-error" />
                      <span className="text-error font-semibold">Critical Data Loss Detected</span>
                    </div>
                  )}
                  <Progress value={metrics.overall_score} className="h-3" />
                </CardContent>
              </Card>

              {/* Score Breakdown */}
              <Card>
                <CardHeader>
                  <CardTitle>Score Breakdown</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">
                        Structural/Section Score
                      </span>
                      <span className="font-mono font-bold">
                        {(metrics.structural_score || metrics.section_score || 0).toFixed(1)}%
                      </span>
                    </div>
                    <Progress value={metrics.structural_score || metrics.section_score || 0} className="h-2" />
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">
                        Attribute/Key Score
                      </span>
                      <span className="font-mono font-bold">
                        {(metrics.attribute_score || metrics.key_score || 0).toFixed(1)}%
                      </span>
                    </div>
                    <Progress value={metrics.attribute_score || metrics.key_score || 0} className="h-2" />
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-muted-foreground">Value Score</span>
                      <span className="font-mono font-bold">
                        {(metrics.value_score || 0).toFixed(1)}%
                      </span>
                    </div>
                    <Progress value={metrics.value_score || 0} className="h-2" />
                  </div>

                  <div className="pt-3 border-t border-border">
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-muted-foreground">Data Loss</span>
                      <span className={`font-bold ${metrics.data_loss_percentage > 1 ? 'text-error' : 'text-success'}`}>
                        {metrics.data_loss_percentage.toFixed(2)}%
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Analysis Metadata */}
              <Card>
                <CardHeader>
                  <CardTitle>Analysis Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">File Type</span>
                    <Badge>{metrics.file_type || 'Unknown'}</Badge>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Device/File ID</span>
                    <span className="font-mono">{metrics.device_id || metrics.eds_file_id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Analysis Date</span>
                    <span className="font-mono">
                      {new Date(metrics.analysis_timestamp).toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Ticket Generated</span>
                    <Badge className={metrics.ticket_generated ? 'bg-brand-green/20 text-brand-green' : 'bg-muted text-muted-foreground'}>
                      {metrics.ticket_generated ? 'Yes' : 'No'}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Differences Tab */}
            <TabsContent value="differences" className="space-y-4 mt-4">
              {diffItems.length === 0 ? (
                <Card>
                  <CardContent className="py-8 text-center text-muted-foreground">
                    No differences found
                  </CardContent>
                </Card>
              ) : (
                <div className="space-y-3">
                  {diffItems.map((item, idx) => (
                    <Card key={idx} className="hover:border-brand-green/50 transition-all">
                      <CardContent className="py-4">
                        <div className="flex items-start gap-3">
                          <div className="mt-1">
                            {getDiffTypeIcon(item.diff_type)}
                          </div>
                          <div className="flex-1">
                            <div className="flex items-start justify-between gap-2 mb-2">
                              <div>
                                <Badge className={getSeverityColor(item.severity)}>
                                  {item.severity}
                                </Badge>
                                <Badge className="ml-2 bg-muted text-foreground">
                                  {item.diff_type}
                                </Badge>
                              </div>
                              <span className="text-xs text-muted-foreground font-mono">
                                {item.xpath}
                              </span>
                            </div>
                            <p className="text-sm text-foreground mb-2">{item.description}</p>
                            {item.original_value && (
                              <div className="text-xs bg-error/10 border border-error/30 rounded p-2 mb-1">
                                <span className="text-muted-foreground">Expected:</span>
                                <span className="ml-2 font-mono text-foreground">
                                  {item.original_value}
                                </span>
                              </div>
                            )}
                            {item.reconstructed_value && (
                              <div className="text-xs bg-brand-green/10 border border-brand-green/30 rounded p-2">
                                <span className="text-muted-foreground">Got:</span>
                                <span className="ml-2 font-mono text-foreground">
                                  {item.reconstructed_value}
                                </span>
                              </div>
                            )}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </TabsContent>

            {/* Details Tab */}
            <TabsContent value="details" className="space-y-4 mt-4">
              <Card>
                <CardHeader>
                  <CardTitle>Raw Metrics Data</CardTitle>
                </CardHeader>
                <CardContent>
                  <pre className="text-xs bg-muted p-4 rounded-lg overflow-x-auto">
                    {JSON.stringify(metrics, null, 2)}
                  </pre>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        ) : (
          <div className="text-center py-8 text-muted-foreground">
            No analysis data available
          </div>
        )}

        <div className="flex justify-end gap-2 pt-4 border-t border-border">
          <Button variant="outline" onClick={onClose}>
            Close
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default PQAAnalysisModal;
