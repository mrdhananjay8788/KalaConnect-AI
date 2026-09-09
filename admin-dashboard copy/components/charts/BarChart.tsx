export default function BarChart({ title, data }: { title: string, data: {label: string, value: number}[] }) {
  const maxValue = Math.max(...data.map(d => d.value));

  return (
    <div className="bg-white p-6 rounded-lg shadow border border-slate-100">
      <h3 className="text-lg font-medium text-slate-900 mb-6">{title}</h3>
      <div className="flex items-end h-48 space-x-2 sm:space-x-4">
        {data.map((item, i) => {
          const heightPercent = maxValue > 0 ? (item.value / maxValue) * 100 : 0;
          return (
            <div key={i} className="flex-1 flex flex-col items-center justify-end group relative">
              {/* Tooltip */}
              <div className="absolute bottom-full mb-2 hidden group-hover:block bg-slate-800 text-white text-xs py-1 px-2 rounded whitespace-nowrap z-10">
                {item.value}
              </div>
              <div 
                className="w-full bg-indigo-500 rounded-t-sm hover:bg-indigo-600 transition-colors duration-300"
                style={{ height: `${heightPercent}%`, minHeight: '10%' }}
              ></div>
              <div className="mt-2 text-xs text-slate-500 truncate w-full text-center" title={item.label}>
                {item.label}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
