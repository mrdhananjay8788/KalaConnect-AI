'use client';

import { logout } from '../../lib/api';

export default function Header({ role }: { role: 'admin' | 'artisan' | null }) {
  if (!role) return null;

  return (
    <div className="sticky top-0 z-10 flex-shrink-0 flex h-16 bg-white shadow">
      <div className="flex-1 px-4 flex justify-between">
        <div className="flex-1 flex items-center">
          <h2 className="text-xl font-semibold text-slate-800 hidden sm:block">
            {role === 'admin' ? 'Platform Administration' : 'Artisan Workspace'}
          </h2>
        </div>
        <div className="ml-4 flex items-center md:ml-6 gap-4">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold">
              {role === 'admin' ? 'A' : 'S'}
            </div>
            <span className="text-sm font-medium text-slate-700 hidden sm:block">
              {role === 'admin' ? 'Super Admin' : 'Shopkeeper'}
            </span>
          </div>
          <button
            onClick={() => logout()}
            className="text-sm text-red-600 hover:text-red-800 font-medium px-3 py-2 rounded-md hover:bg-red-50 transition-colors"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}
