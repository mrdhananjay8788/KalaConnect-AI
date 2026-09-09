import { redirect } from 'next/navigation';
import { getUserRole } from '../../lib/auth';

export default function CategoriesPage() {
  const role = getUserRole();

  if (!role) {
    redirect('/login');
  }

  // Artisan should not access this directly if we want to restrict, 
  // but let's assume they might see it or it's just hidden from their sidebar.
  // The plan said "Global Categories page (Admin only visibility)."
  if (role !== 'admin') {
    return (
      <div className="p-8 text-center text-slate-500">
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Access Denied</h2>
        <p>You do not have permission to view global categories.</p>
      </div>
    );
  }

  return (
    <div className="py-6 px-4 sm:px-6 lg:px-8">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-bold text-slate-900">Categories</h1>
          <p className="mt-2 text-sm text-slate-700">
            Manage global product categories used across the entire KalaConnect-AI platform.
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <button
            type="button"
            className="inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 sm:w-auto"
          >
            Add Category
          </button>
        </div>
      </div>
      
      <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {/* Placeholder Categories */}
        {['Textiles & Fabrics', 'Pottery & Ceramics', 'Woodwork & Carving', 'Jewelry', 'Paintings', 'Metalwork'].map((cat) => (
          <div key={cat} className="relative rounded-lg border border-slate-300 bg-white px-6 py-5 shadow-sm flex items-center space-x-3 hover:border-slate-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500">
            <div className="flex-1 min-w-0">
              <span className="absolute inset-0" aria-hidden="true" />
              <p className="text-sm font-medium text-slate-900">{cat}</p>
              <p className="text-sm text-slate-500 truncate">124 Products</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
