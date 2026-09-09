import { redirect } from 'next/navigation';
import { getUserRole } from '../../lib/auth';
import BarChart from '../../components/charts/BarChart';

export default function AnalyticsPage() {
  const role = getUserRole();

  if (!role) {
    redirect('/login');
  }

  const adminCharts = [
    {
      title: 'Platform Revenue (Last 6 Months)',
      data: [
        { label: 'May', value: 45000 },
        { label: 'Jun', value: 52000 },
        { label: 'Jul', value: 48000 },
        { label: 'Aug', value: 61000 },
        { label: 'Sep', value: 59000 },
        { label: 'Oct', value: 75000 },
      ]
    },
    {
      title: 'Artisans by Region',
      data: [
        { label: 'North', value: 450 },
        { label: 'South', value: 380 },
        { label: 'East', value: 290 },
        { label: 'West', value: 310 },
      ]
    }
  ];

  const artisanCharts = [
    {
      title: 'My Revenue (Last 6 Months)',
      data: [
        { label: 'May', value: 4500 },
        { label: 'Jun', value: 5200 },
        { label: 'Jul', value: 4800 },
        { label: 'Aug', value: 6100 },
        { label: 'Sep', value: 5900 },
        { label: 'Oct', value: 8500 },
      ]
    },
    {
      title: 'Product Views (This Week)',
      data: [
        { label: 'Mon', value: 120 },
        { label: 'Tue', value: 150 },
        { label: 'Wed', value: 90 },
        { label: 'Thu', value: 210 },
        { label: 'Fri', value: 280 },
        { label: 'Sat', value: 350 },
        { label: 'Sun', value: 310 },
      ]
    }
  ];

  const charts = role === 'admin' ? adminCharts : artisanCharts;

  return (
    <div className="py-6 px-4 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900">Analytics</h1>
        <p className="mt-1 text-sm text-slate-500">
          {role === 'admin' 
            ? 'Platform-wide performance and metrics.' 
            : 'Performance of your shop and products.'}
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {charts.map((chart, index) => (
          <BarChart key={index} title={chart.title} data={chart.data} />
        ))}
      </div>
    </div>
  );
}
