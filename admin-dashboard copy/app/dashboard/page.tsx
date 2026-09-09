import { getUserRole } from '../../lib/auth';
import KpiCard from '../../components/dashboard/KpiCard';
import { redirect } from 'next/navigation';

export default function DashboardPage() {
  const role = getUserRole();

  if (!role) {
    redirect('/login');
  }

  const metrics = [
    { title: 'Total Revenue', value: '$84,520', trend: '+12.5%', trendUp: true, icon: '💰' },
    { title: 'Active Orders', value: '142', trend: '+4.2%', trendUp: true, icon: '📦' },
    { title: 'Visitors', value: '12,450', trend: '-2.1%', trendUp: false, icon: '👥' },
  ];

  const recentOrders = [
    { id: '#ORD-7352', customer: 'Alice Johnson', date: 'Oct 26, 2023', total: '$120.00', status: 'Shipped' },
    { id: '#ORD-7353', customer: 'Bob Smith', date: 'Oct 26, 2023', total: '$45.50', status: 'Pending' },
    { id: '#ORD-7354', customer: 'Charlie Davis', date: 'Oct 25, 2023', total: '$299.99', status: 'Shipped' },
    { id: '#ORD-7355', customer: 'Diana Evans', date: 'Oct 25, 2023', total: '$89.00', status: 'Pending' },
    { id: '#ORD-7356', customer: 'Ethan Foster', date: 'Oct 24, 2023', total: '$14.99', status: 'Shipped' },
  ];

  return (
    <div className="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 tracking-tight">
          Dashboard overview
        </h1>
        <p className="mt-2 text-sm text-slate-600">
          Welcome back. Here is a summary of your e-commerce performance.
        </p>
      </div>

      {/* Top-Level Metric Cards */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
        {metrics.map((kpi) => (
          <div key={kpi.title} className="bg-white overflow-hidden shadow-sm rounded-xl border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-gray-50 rounded-lg p-3 text-2xl border border-gray-100">
                {kpi.icon}
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-slate-500 truncate">{kpi.title}</dt>
                  <dd className="flex items-baseline mt-1">
                    <div className="text-3xl font-bold text-slate-900">{kpi.value}</div>
                    <div className={`ml-3 flex items-baseline text-sm font-semibold ${kpi.trendUp ? 'text-emerald-600' : 'text-rose-600'}`}>
                      {kpi.trendUp ? '↑' : '↓'}
                      <span className="ml-1">{kpi.trend}</span>
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {/* Recent Orders Striped Data Table */}
      <div className="mt-10 bg-white shadow-sm rounded-xl border border-gray-200 overflow-hidden">
        <div className="px-6 py-5 border-b border-gray-200 bg-white">
          <h2 className="text-lg font-semibold text-slate-900">Recent Orders</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Order ID</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Customer</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Date</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Total</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {recentOrders.map((order, idx) => (
                <tr key={order.id} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">
                    {order.id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-600">
                    {order.customer}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                    {order.date}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">
                    {order.total}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      order.status === 'Shipped' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {order.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
