import { redirect } from 'next/navigation';
import { getUserRole } from '../../lib/auth';

export default function ProductsPage() {
  const role = getUserRole();

  if (!role) {
    redirect('/login');
  }

  return (
    <div className="py-6 px-4 sm:px-6 lg:px-8">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-bold text-slate-900">
            {role === 'admin' ? 'Global Product Management' : 'My Products'}
          </h1>
          <p className="mt-2 text-sm text-slate-700">
            {role === 'admin' 
              ? 'A list of all products across the platform including their title, category, status and artisan.'
              : 'A list of all your products. You can generate AI catalogs for your items here.'}
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none flex gap-3">
          {role === 'artisan' && (
            <>
              <button
                type="button"
                className="inline-flex items-center justify-center rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50 sm:w-auto"
              >
                Generate AI Catalog
              </button>
              <button
                type="button"
                className="inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 sm:w-auto"
              >
                Add product
              </button>
            </>
          )}
        </div>
      </div>
      
      <div className="mt-8 flex flex-col">
        <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
              <table className="min-w-full divide-y divide-slate-300 bg-white">
                <thead className="bg-slate-50">
                  <tr>
                    <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-slate-900 sm:pl-6">Product</th>
                    {role === 'admin' && <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-slate-900">Artisan</th>}
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-slate-900">Category</th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-slate-900">Status</th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-slate-900">Price</th>
                    <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                      <span className="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 bg-white">
                  <tr>
                    <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-slate-900 sm:pl-6">Handwoven Silk Saree</td>
                    {role === 'admin' && <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-500">Ravi Kumar</td>}
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-500">Textiles</td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm">
                      <span className="inline-flex rounded-full bg-yellow-100 px-2 text-xs font-semibold leading-5 text-yellow-800">Pending</span>
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-500">₹4,500</td>
                    <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                      {role === 'admin' ? (
                        <div className="flex justify-end gap-2">
                          <button className="text-green-600 hover:text-green-900">Approve</button>
                          <button className="text-red-600 hover:text-red-900">Reject</button>
                        </div>
                      ) : (
                        <div className="flex justify-end gap-2">
                          <button className="text-indigo-600 hover:text-indigo-900">Edit</button>
                        </div>
                      )}
                    </td>
                  </tr>
                  {/* More rows... */}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
