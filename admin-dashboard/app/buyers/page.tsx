import { redirect } from 'next/navigation';
import { getUserRole } from '../../lib/auth';

export default function BuyersPage() {
  const role = getUserRole();

  if (!role) {
    redirect('/login');
  }

  return (
    <div className="py-6 px-4 sm:px-6 lg:px-8">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-bold text-slate-900">
            {role === 'admin' ? 'Registered Buyers' : 'Direct Enquiries'}
          </h1>
          <p className="mt-2 text-sm text-slate-700">
            {role === 'admin' 
              ? 'A global list of all registered buyers and their platform activity.'
              : 'Direct requirements and enquiries sent to you by buyers.'}
          </p>
        </div>
      </div>
      
      <div className="mt-8 bg-white shadow overflow-hidden sm:rounded-md">
        <ul role="list" className="divide-y divide-slate-200">
          {role === 'admin' ? (
            // Admin View: List of Buyers
            <li>
              <div className="px-4 py-4 sm:px-6 hover:bg-slate-50 transition-colors cursor-pointer">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-indigo-600 truncate">Anita Desai</p>
                  <div className="ml-2 flex-shrink-0 flex">
                    <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      Active
                    </p>
                  </div>
                </div>
                <div className="mt-2 sm:flex sm:justify-between">
                  <div className="sm:flex">
                    <p className="flex items-center text-sm text-slate-500">
                      anita.d@example.com
                    </p>
                  </div>
                  <div className="mt-2 flex items-center text-sm text-slate-500 sm:mt-0">
                    <p>
                      Joined on <time dateTime="2023-01-07">January 7, 2023</time>
                    </p>
                  </div>
                </div>
              </div>
            </li>
          ) : (
            // Artisan View: Enquiries
            <li>
              <div className="px-4 py-4 sm:px-6 hover:bg-slate-50 transition-colors cursor-pointer">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-indigo-600 truncate">Bulk order inquiry for Silk Sarees</p>
                  <div className="ml-2 flex-shrink-0 flex">
                    <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                      New
                    </p>
                  </div>
                </div>
                <div className="mt-2 sm:flex sm:justify-between">
                  <div className="sm:flex">
                    <p className="flex items-center text-sm text-slate-500">
                      From: Boutique Owner in Mumbai
                    </p>
                  </div>
                  <div className="mt-2 flex items-center text-sm text-slate-500 sm:mt-0">
                    <p>Received 2 hours ago</p>
                  </div>
                </div>
              </div>
            </li>
          )}
        </ul>
      </div>
    </div>
  );
}
