import React, { useState, useEffect } from 'react';
import {
  Activity, AlertCircle, XCircle, CheckCircle, Target, BarChart,
  ArrowRight, ChevronDown, ChevronRight, RefreshCw, TrendingUp,
  AlertTriangle, FileText, Play, Clock
} from 'lucide-react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from './ui';
import { Button } from './ui';
import { Badge } from './ui';

/**
 * Comprehensive PQA (Parser Quality Assurance) Console
 * Provides forensic analysis and quality metrics for IODD and EDS parsers
 */
const PQAConsole = ({ API_BASE, toast }) => {
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState(null);
  const [trends, setTrends] = useState(null);
  const [failures, setFailures] = useState(null);
  const [thresholds, setThresholds] = useState(null);
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [expandedFailure, setExpandedFailure] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    loadPQAData();
  }, []);

  const loadPQAData = async () => {
    setLoading(true);
    try {
      const [summaryRes, trendsRes, failuresRes, thresholdsRes] = await Promise.all([
        axios.get(`${API_BASE}/api/pqa/dashboard/summary`).catch(() => ({ data: null })),
        axios.get(`${API_BASE}/api/pqa/dashboard/trends?days=30`).catch(() => ({ data: null })),
        axios.get(`${API_BASE}/api/pqa/dashboard/failures?limit=20`).catch(() => ({ data: null })),
        axios.get(`${API_BASE}/api/pqa/thresholds`).catch(() => ({ data: [] }))
      ]);

      setSummary(summaryRes.data);
      setTrends(trendsRes.data);
      setFailures(failuresRes.data);
      setThresholds(thresholdsRes.data);
    } catch (error) {
      console.error('Error loading PQA data:', error);
      toast?.({
        title: 'PQA Data Load Error',
        description: 'Could not load PQA dashboard data. The PQA system may not be initialized yet.',
        variant: 'warning'
      });
    } finally {
      setLoading(false);
    }
  };

  const runAnalysis = async (deviceId, fileType) => {
    setAnalyzing(true);
    try {
      await axios.post(`${API_BASE}/api/pqa/analyze`, {
        device_id: deviceId,
        file_type: fileType
      });

      toast?.({
        title: 'Analysis Started',
        description: `Parser quality analysis initiated for ${fileType} device ${deviceId}`,
        variant: 'success'
      });

      // Reload data after a delay to see results
      setTimeout(() => loadPQAData(), 3000);
    } catch (error) {
      toast?.({
        title: 'Analysis Failed',
        description: error.response?.data?.detail || 'Could not start quality analysis',
        variant: 'error'
      });
    } finally {
      setAnalyzing(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 98) return 'text-success';
    if (score >= 95) return 'text-warning';
    return 'text-error';
  };

  const getScoreBgColor = (score) => {
    if (score >= 98) return 'bg-success/20 border-success/50';
    if (score >= 95) return 'bg-warning/20 border-warning/50';
    return 'bg-error/20 border-error/50';
  };

  const QualityGauge = ({ score, label }) => {
    const radius = 60;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (score / 100) * circumference;

    return (
      <div className="flex flex-col items-center">
        <svg width="150" height="150" className="-rotate-90">
          <circle
            cx="75"
            cy="75"
            r={radius}
            stroke="currentColor"
            strokeWidth="8"
            fill="transparent"
            className="text-secondary"
          />
          <circle
            cx="75"
            cy="75"
            r={radius}
            stroke="currentColor"
            strokeWidth="8"
            fill="transparent"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            className={score >= 98 ? 'text-success' : score >= 95 ? 'text-warning' : 'text-error'}
            strokeLinecap="round"
          />
          <text
            x="75"
            y="75"
            className="text-3xl font-bold fill-current text-foreground rotate-90"
            textAnchor="middle"
            dominantBaseline="middle"
            transform="rotate(90 75 75)"
          >
            {score.toFixed(1)}
          </text>
        </svg>
        <p className="text-sm text-muted-foreground mt-2">{label}</p>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin text-brand-green" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* PQA System Header */}
      <Card className="bg-gradient-to-br from-brand-green/10 to-background border-brand-green/30">
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-lg bg-brand-green/20 flex items-center justify-center">
                <Target className="w-6 h-6 text-brand-green" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-foreground">Parser Quality Assurance</h2>
                <p className="text-sm text-muted-foreground">Forensic analysis & reconstruction quality metrics</p>
              </div>
            </div>
            <Button
              onClick={loadPQAData}
              className="bg-brand-green/20 hover:bg-brand-green/30 text-brand-green border-brand-green/50"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh
            </Button>
          </CardTitle>
        </CardHeader>
      </Card>

      {/* Summary Statistics */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="bg-card border-border">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Total Analyses</p>
                  <p className="text-3xl font-bold text-foreground">{summary.total_analyses || 0}</p>
                </div>
                <BarChart className="w-10 h-10 text-brand-green/50" />
              </div>
            </CardContent>
          </Card>

          <Card className={`bg-card border ${getScoreBgColor(summary.average_score || 0)}`}>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Average Score</p>
                  <p className={`text-3xl font-bold ${getScoreColor(summary.average_score || 0)}`}>
                    {(summary.average_score || 0).toFixed(1)}%
                  </p>
                </div>
                <TrendingUp className="w-10 h-10 text-success/50" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-card border-success/50">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Passed</p>
                  <p className="text-3xl font-bold text-success">{summary.passed_analyses || 0}</p>
                </div>
                <CheckCircle className="w-10 h-10 text-success/50" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-card border-error/50">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">Failed</p>
                  <p className="text-3xl font-bold text-error">{summary.failed_analyses || 0}</p>
                </div>
                <XCircle className="w-10 h-10 text-error/50" />
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Quality Metrics Gauges */}
      {summary && summary.average_score > 0 && (
        <Card className="bg-card border-border">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-brand-green" />
              Quality Metrics Overview
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 justify-items-center">
              <QualityGauge score={summary.average_score || 0} label="Overall Quality" />
              <div className="flex flex-col items-center space-y-4">
                <div className="text-center">
                  <p className="text-4xl font-bold text-foreground">{summary.devices_analyzed || 0}</p>
                  <p className="text-sm text-muted-foreground">Devices Analyzed</p>
                </div>
                <div className="text-center">
                  <p className="text-4xl font-bold text-error">{summary.critical_failures || 0}</p>
                  <p className="text-sm text-muted-foreground">Critical Failures</p>
                </div>
              </div>
              <div className="flex flex-col space-y-2 w-full max-w-xs">
                <h4 className="text-sm font-semibold text-foreground mb-2">Quality Target: 98%+</h4>
                <div className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-muted-foreground">Pass Rate</span>
                    <span className={getScoreColor(summary.average_score || 0)}>
                      {summary.total_analyses > 0
                        ? ((summary.passed_analyses / summary.total_analyses) * 100).toFixed(1)
                        : 0}%
                    </span>
                  </div>
                  <div className="w-full bg-secondary/30 rounded-full h-2">
                    <div
                      className="h-2 rounded-full bg-success"
                      style={{
                        width: summary.total_analyses > 0
                          ? `${(summary.passed_analyses / summary.total_analyses) * 100}%`
                          : '0%'
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Active Thresholds */}
      {thresholds && thresholds.length > 0 && (
        <Card className="bg-card border-border">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="w-5 h-5 text-warning" />
              Quality Thresholds
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {thresholds.slice(0, 2).map((threshold, idx) => (
                <div key={idx} className="p-4 bg-secondary/30 rounded-lg border border-border">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-semibold text-foreground">{threshold.threshold_name}</h4>
                    <Badge className={threshold.active ? 'bg-success/20 text-success' : 'bg-secondary'}>
                      {threshold.active ? 'Active' : 'Inactive'}
                    </Badge>
                  </div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Min Overall Score:</span>
                      <span className="text-foreground font-medium">{threshold.min_overall_score}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Max Data Loss:</span>
                      <span className="text-foreground font-medium">{threshold.max_data_loss_percentage}%</span>
                    </div>
                    {threshold.auto_ticket_on_fail && (
                      <Badge className="bg-warning/20 text-warning text-xs">Auto-ticket enabled</Badge>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Recent Failures */}
      {failures && failures.failures && failures.failures.length > 0 && (
        <Card className="bg-card border-error/30">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-error" />
              Recent Quality Failures ({failures.failures.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {failures.failures.map((failure, idx) => (
                <div
                  key={idx}
                  className="p-4 bg-error/10 rounded-lg border border-error/30 cursor-pointer hover:bg-error/20 transition-colors"
                  onClick={() => setExpandedFailure(expandedFailure === idx ? null : idx)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <FileText className="w-4 h-4 text-error" />
                        <span className="font-medium text-foreground">
                          {failure.file_type} Device #{failure.device_id}
                        </span>
                        <Badge className="bg-error/20 text-error text-xs">
                          Score: {failure.overall_score.toFixed(1)}%
                        </Badge>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Analyzed: {new Date(failure.timestamp).toLocaleString()}
                      </div>
                    </div>
                    {expandedFailure === idx ? (
                      <ChevronDown className="w-5 h-5 text-muted-foreground flex-shrink-0" />
                    ) : (
                      <ChevronRight className="w-5 h-5 text-muted-foreground flex-shrink-0" />
                    )}
                  </div>

                  {expandedFailure === idx && (
                    <div className="mt-4 pt-4 border-t border-error/30 space-y-3">
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-muted-foreground">Data Loss:</span>
                          <span className="ml-2 text-error font-medium">
                            {failure.data_loss_percentage?.toFixed(2)}%
                          </span>
                        </div>
                        <div>
                          <span className="text-muted-foreground">Critical:</span>
                          <span className="ml-2 text-error font-medium">
                            {failure.critical_data_loss ? 'Yes' : 'No'}
                          </span>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          className="bg-brand-green/20 hover:bg-brand-green/30 text-brand-green"
                          onClick={(e) => {
                            e.stopPropagation();
                            runAnalysis(failure.device_id, failure.file_type);
                          }}
                          disabled={analyzing}
                        >
                          <Play className="w-3 h-3 mr-1" />
                          Re-analyze
                        </Button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Getting Started Guide */}
      {(!summary || summary.total_analyses === 0) && (
        <Card className="bg-card border-brand-green/30">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-brand-green" />
              Getting Started with PQA
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-muted-foreground">
              The Parser Quality Assurance system provides forensic analysis of IODD and EDS file parsing.
              No analyses have been run yet.
            </p>
            <div className="space-y-2">
              <h4 className="font-semibold text-foreground">How it works:</h4>
              <ol className="list-decimal list-inside space-y-1 text-sm text-muted-foreground">
                <li>Original files are archived with SHA256 hash verification</li>
                <li>Files are reconstructed from database using forensic engines</li>
                <li>Differential analysis compares original vs. reconstructed</li>
                <li>Quality scores are calculated (Target: 98%+, Structural: 99%+)</li>
                <li>Auto-tickets are generated for failures</li>
              </ol>
            </div>
            <div className="flex items-start gap-2 p-3 bg-brand-green/10 rounded-lg">
              <AlertTriangle className="w-5 h-5 text-brand-green flex-shrink-0 mt-0.5" />
              <p className="text-sm text-muted-foreground">
                Run your first analysis using the API: <code className="text-xs bg-secondary px-1 py-0.5 rounded">POST /api/pqa/analyze</code>
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default PQAConsole;
