export default function KpiCard({
  title,
  value,
  trend,
  trendUp,
  icon,
}: {
  title: string;
  value: string;
  trend?: string;
  trendUp?: boolean;
  icon?: string;
}) {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg border border-slate-100 p-5 hover:shadow-md transition-shadow">
      <div className="flex items-center">
        <div className="flex-shrink-0 bg-indigo-50 rounded-md p-3 text-2xl">
          {icon || '📊'}
        </div>
        <div className="ml-5 w-0 flex-1">
          <dl>
            <dt className="text-sm font-medium text-slate-500 truncate">{title}</dt>
            <dd className="flex items-baseline">
              <div className="text-2xl font-semibold text-slate-900">{value}</div>
              {trend && (
                <div className={`ml-2 flex items-baseline text-sm font-semibold ${trendUp ? 'text-green-600' : 'text-red-600'}`}>
                  {trendUp ? '↑' : '↓'}
                  <span className="ml-1">{trend}</span>
                </div>
              )}
            </dd>
          </dl>
        </div>
      </div>
    </div>
  );
}
