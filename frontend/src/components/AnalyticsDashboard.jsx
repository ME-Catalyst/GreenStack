import React, { useState, useEffect, useMemo } from 'react';
import {
  Card, CardHeader, CardContent, CardTitle, CardDescription,
  Tabs, TabsContent, TabsList, TabsTrigger,
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from './ui';
import {
  BarChart3, TrendingUp, Package, Database, Activity, Download,
  Cpu, Zap, Calendar, Users, PieChart, LineChart as LineChartIcon
} from 'lucide-react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line, Bar, Doughnut, Pie } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const AnalyticsDashboard = ({ devices, edsFiles, stats }) => {
  const [timeRange, setTimeRange] = useState('30d');
  const [selectedMetric, setSelectedMetric] = useState('devices');

  // Calculate analytics data
  const analyticsData = useMemo(() => {
    // Manufacturer distribution
    const manufacturerCounts = {};
    devices.forEach((device) => {
      const mfg = device.manufacturer || 'Unknown';
      manufacturerCounts[mfg] = (manufacturerCounts[mfg] || 0) + 1;
    });

    // EDS vendor distribution
    const vendorCounts = {};
    edsFiles.forEach((eds) => {
      const vendor = eds.vendor_name || 'Unknown';
      vendorCounts[vendor] = (vendorCounts[vendor] || 0) + 1;
    });

    // Device I/O types distribution
    const ioTypeCounts = { digital: 0, analog: 0, mixed: 0, unknown: 0 };
    devices.forEach((device) => {
      const params = device.parameters || [];
      const hasDigital = params.some(p => p.datatype?.toLowerCase().includes('bool'));
      const hasAnalog = params.some(p => !p.datatype?.toLowerCase().includes('bool'));

      if (hasDigital && hasAnalog) ioTypeCounts.mixed++;
      else if (hasDigital) ioTypeCounts.digital++;
      else if (hasAnalog) ioTypeCounts.analog++;
      else ioTypeCounts.unknown++;
    });

    // Parameter data types
    const datatypeCounts = {};
    devices.forEach((device) => {
      const params = device.parameters || [];
      params.forEach((param) => {
        const dt = param.datatype || 'Unknown';
        datatypeCounts[dt] = (datatypeCounts[dt] || 0) + 1;
      });
    });

    // Parameters per device distribution
    const paramDistribution = { '0-10': 0, '11-50': 0, '51-100': 0, '100+': 0 };
    devices.forEach((device) => {
      const count = device.parameters?.length || 0;
      if (count <= 10) paramDistribution['0-10']++;
      else if (count <= 50) paramDistribution['11-50']++;
      else if (count <= 100) paramDistribution['51-100']++;
      else paramDistribution['100+']++;
    });

    return {
      manufacturerCounts,
      vendorCounts,
      ioTypeCounts,
      datatypeCounts,
      paramDistribution,
    };
  }, [devices, edsFiles]);

  // Chart configurations with readable colors
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#9ca3af',
          font: { size: 12 },
        },
      },
      tooltip: {
        backgroundColor: 'rgba(17, 24, 39, 0.95)',
        titleColor: '#f3f4f6',
        bodyColor: '#d1d5db',
        borderColor: '#374151',
        borderWidth: 1,
        padding: 12,
        cornerRadius: 8,
      },
    },
    scales: {
      x: {
        ticks: {
          color: '#9ca3af',
          font: { size: 11 },
        },
        grid: {
          color: 'rgba(75, 85, 99, 0.2)',
          drawBorder: false,
        },
      },
      y: {
        ticks: {
          color: '#9ca3af',
          font: { size: 11 },
        },
        grid: {
          color: 'rgba(75, 85, 99, 0.2)',
          drawBorder: false,
        },
      },
    },
  };

  const pieChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
        labels: {
          color: '#9ca3af',
          padding: 15,
          font: { size: 12 },
          boxWidth: 15,
          boxHeight: 15,
        },
      },
      tooltip: {
        backgroundColor: 'rgba(17, 24, 39, 0.95)',
        titleColor: '#f3f4f6',
        bodyColor: '#d1d5db',
        borderColor: '#374151',
        borderWidth: 1,
        padding: 12,
        cornerRadius: 8,
      },
    },
  };

  // Vibrant color palette for charts
  const colors = {
    green: { bg: 'rgba(34, 197, 94, 0.7)', border: 'rgb(34, 197, 94)' },
    cyan: { bg: 'rgba(6, 182, 212, 0.7)', border: 'rgb(6, 182, 212)' },
    blue: { bg: 'rgba(59, 130, 246, 0.7)', border: 'rgb(59, 130, 246)' },
    purple: { bg: 'rgba(168, 85, 247, 0.7)', border: 'rgb(168, 85, 247)' },
    pink: { bg: 'rgba(236, 72, 153, 0.7)', border: 'rgb(236, 72, 153)' },
    orange: { bg: 'rgba(249, 115, 22, 0.7)', border: 'rgb(249, 115, 22)' },
    yellow: { bg: 'rgba(234, 179, 8, 0.7)', border: 'rgb(234, 179, 8)' },
    red: { bg: 'rgba(239, 68, 68, 0.7)', border: 'rgb(239, 68, 68)' },
    teal: { bg: 'rgba(20, 184, 166, 0.7)', border: 'rgb(20, 184, 166)' },
    indigo: { bg: 'rgba(99, 102, 241, 0.7)', border: 'rgb(99, 102, 241)' },
  };

  // Manufacturer chart data
  const manufacturerChartData = {
    labels: Object.keys(analyticsData.manufacturerCounts).slice(0, 10),
    datasets: [
      {
        label: 'Devices',
        data: Object.values(analyticsData.manufacturerCounts).slice(0, 10),
        backgroundColor: colors.green.bg,
        borderColor: colors.green.border,
        borderWidth: 2,
        borderRadius: 6,
      },
    ],
  };

  // Vendor chart data
  const vendorChartData = {
    labels: Object.keys(analyticsData.vendorCounts).slice(0, 10),
    datasets: [
      {
        label: 'EDS Files',
        data: Object.values(analyticsData.vendorCounts).slice(0, 10),
        backgroundColor: colors.cyan.bg,
        borderColor: colors.cyan.border,
        borderWidth: 2,
        borderRadius: 6,
      },
    ],
  };

  // I/O Type distribution
  const ioTypeChartData = {
    labels: Object.keys(analyticsData.ioTypeCounts).map(k => k.charAt(0).toUpperCase() + k.slice(1)),
    datasets: [
      {
        data: Object.values(analyticsData.ioTypeCounts),
        backgroundColor: [
          colors.green.bg,
          colors.cyan.bg,
          colors.purple.bg,
          colors.orange.bg,
        ],
        borderColor: [
          colors.green.border,
          colors.cyan.border,
          colors.purple.border,
          colors.orange.border,
        ],
        borderWidth: 2,
      },
    ],
  };

  // Parameter distribution
  const paramDistChartData = {
    labels: Object.keys(analyticsData.paramDistribution),
    datasets: [
      {
        label: 'Number of Devices',
        data: Object.values(analyticsData.paramDistribution),
        backgroundColor: colors.purple.bg,
        borderColor: colors.purple.border,
        borderWidth: 2,
        borderRadius: 6,
      },
    ],
  };

  // Data type distribution (top 10)
  const topDatatypes = Object.entries(analyticsData.datatypeCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  const datatypeChartData = {
    labels: topDatatypes.map(([dt]) => dt),
    datasets: [
      {
        data: topDatatypes.map(([, count]) => count),
        backgroundColor: [
          colors.green.bg,
          colors.cyan.bg,
          colors.blue.bg,
          colors.purple.bg,
          colors.pink.bg,
          colors.orange.bg,
          colors.yellow.bg,
          colors.red.bg,
          colors.teal.bg,
          colors.indigo.bg,
        ],
        borderColor: [
          colors.green.border,
          colors.cyan.border,
          colors.blue.border,
          colors.purple.border,
          colors.pink.border,
          colors.orange.border,
          colors.yellow.border,
          colors.red.border,
          colors.teal.border,
          colors.indigo.border,
        ],
        borderWidth: 2,
      },
    ],
  };

  // Summary metrics
  const metrics = [
    {
      title: 'IO-Link Devices',
      value: devices.length,
      icon: <Package className="w-5 h-5" />,
      bgColor: 'bg-emerald-500/10',
      iconColor: 'text-emerald-500',
    },
    {
      title: 'Total Parameters',
      value: stats.total_parameters || 0,
      icon: <Database className="w-5 h-5" />,
      bgColor: 'bg-cyan-500/10',
      iconColor: 'text-cyan-500',
    },
    {
      title: 'EDS Files',
      value: edsFiles.length,
      icon: <Cpu className="w-5 h-5" />,
      bgColor: 'bg-purple-500/10',
      iconColor: 'text-purple-500',
    },
    {
      title: 'Manufacturers',
      value: Object.keys(analyticsData.manufacturerCounts).length,
      icon: <Users className="w-5 h-5" />,
      bgColor: 'bg-orange-500/10',
      iconColor: 'text-orange-500',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Analytics Dashboard</h2>
          <p className="text-muted-foreground mt-1">Insights and trends from your device library</p>
        </div>
        <div className="flex items-center gap-4">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-40 bg-secondary border-border text-foreground">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7d">Last 7 days</SelectItem>
              <SelectItem value="30d">Last 30 days</SelectItem>
              <SelectItem value="90d">Last 90 days</SelectItem>
              <SelectItem value="1y">Last year</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((metric, index) => (
          <Card key={index} className="bg-card border-border hover:border-border/80 transition-colors">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between mb-3">
                <p className="text-sm font-medium text-muted-foreground">{metric.title}</p>
                <div className={`p-2 rounded-lg ${metric.bgColor}`}>
                  <div className={metric.iconColor}>{metric.icon}</div>
                </div>
              </div>
              <div className="text-3xl font-bold text-foreground">{metric.value.toLocaleString()}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charts */}
      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="bg-secondary/50 border-b border-border p-1">
          <TabsTrigger value="overview" className="data-[state=active]:bg-card data-[state=active]:text-foreground">
            Overview
          </TabsTrigger>
          <TabsTrigger value="devices" className="data-[state=active]:bg-card data-[state=active]:text-foreground">
            Devices
          </TabsTrigger>
          <TabsTrigger value="parameters" className="data-[state=active]:bg-card data-[state=active]:text-foreground">
            Parameters
          </TabsTrigger>
          <TabsTrigger value="eds" className="data-[state=active]:bg-card data-[state=active]:text-foreground">
            EDS Files
          </TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="text-foreground flex items-center gap-2">
                  <PieChart className="w-5 h-5" />
                  I/O Type Distribution
                </CardTitle>
                <CardDescription>Device categorization by I/O capabilities</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <Doughnut data={ioTypeChartData} options={pieChartOptions} />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="text-foreground flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  Parameters per Device
                </CardTitle>
                <CardDescription>Distribution of parameter counts</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-80">
                  <Bar data={paramDistChartData} options={chartOptions} />
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="devices" className="space-y-6">
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="text-foreground flex items-center gap-2">
                <BarChart3 className="w-5 h-5" />
                Top Manufacturers
              </CardTitle>
              <CardDescription>Devices by manufacturer (top 10)</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-96">
                <Bar data={manufacturerChartData} options={chartOptions} />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="parameters" className="space-y-6">
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="text-foreground flex items-center gap-2">
                <PieChart className="w-5 h-5" />
                Data Type Distribution
              </CardTitle>
              <CardDescription>Top 10 parameter data types across all devices</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-96">
                <Pie data={datatypeChartData} options={pieChartOptions} />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="eds" className="space-y-6">
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="text-foreground flex items-center gap-2">
                <BarChart3 className="w-5 h-5" />
                EDS Vendors
              </CardTitle>
              <CardDescription>EDS files by vendor (top 10)</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-96">
                <Bar data={vendorChartData} options={chartOptions} />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AnalyticsDashboard;
