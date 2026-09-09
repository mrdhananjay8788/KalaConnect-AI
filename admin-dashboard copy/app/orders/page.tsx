import { redirect } from 'next/navigation';
import { getUserRole } from '../../lib/auth';

export default function OrdersPage() {
  const role = getUserRole();

  if (!role) {
    redirect('/login');
  }

  return (
    <div className="py-6 px-4 sm:px-6 lg:px-8">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-bold text-slate-900">
            {role === 'admin' ? 'Global Orders' : 'My Orders'}
          </h1>
          <p className="mt-2 text-sm text-slate-700">
            {role === 'admin' 
              ? 'A list of all orders placed across the entire KalaConnect-AI platform.'
              : 'A list of orders placed for your specific products.'}
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <button
            type="button"
            className="inline-flex items-center justify-center rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50 sm:w-auto"
          >
            Export CSV
          </button>
        </div>
      </div>
      
      <div className="mt-8 flex flex-col">
        <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
              <table className="min-w-full divide-y divide-slate-300 bg-white">
                <thead className="bg-slate-50">
                  <tr>
                    <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-slate-900 sm:pl-6">Order ID</th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-slate-900">Date</th>
                    {role === 'admin' && <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-slate-900">Artisan</th>}
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-slate-900">Customer</th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-slate-900">Total</th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-slate-900">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 bg-white">
                  <tr>
                    <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-indigo-600 sm:pl-6">#ORD-001</td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-500">Oct 24, 2023</td>
                    {role === 'admin' && <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-500">Ravi Kumar</td>}
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-500">Anita Desai</td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-500">₹4,500</td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm">
                      <span className="inline-flex rounded-full bg-green-100 px-2 text-xs font-semibold leading-5 text-green-800">Shipped</span>
                    </td>
                  </tr>
                  <tr>
                    <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-indigo-600 sm:pl-6">#ORD-002</td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-500">Oct 25, 2023</td>
                    {role === 'admin' && <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-500">Meera Weaves</td>}
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-500">John Smith</td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-500">₹12,000</td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm">
                      <span className="inline-flex rounded-full bg-yellow-100 px-2 text-xs font-semibold leading-5 text-yellow-800">Processing</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
