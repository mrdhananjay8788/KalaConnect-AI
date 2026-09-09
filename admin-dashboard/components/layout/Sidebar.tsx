import Link from 'next/link';
import { getUserRole } from '../../lib/auth';

export default function Sidebar() {
  const role = getUserRole();

  const adminLinks = [
    { name: 'Dashboard', href: '/dashboard', icon: '📊' },
    { name: 'Orders', href: '/orders', icon: '🛒' },
    { name: 'Products', href: '/products', icon: '📦' },
    { name: 'Customers', href: '/buyers', icon: '👥' },
    { name: 'Analytics', href: '/analytics', icon: '📈' },
    { name: 'Categories', href: '/categories', icon: '🏷️' },
    { name: 'Artisans', href: '/artisans', icon: '🎨' },
    { name: 'Settings', href: '/settings', icon: '⚙️' },
  ];

  const artisanLinks = [
    { name: 'Dashboard', href: '/dashboard', icon: '📊' },
    { name: 'My Products', href: '/products', icon: '📦' },
    { name: 'My Orders', href: '/orders', icon: '🛒' },
    { name: 'Enquiries', href: '/buyers', icon: '💬' },
    { name: 'Analytics', href: '/analytics', icon: '📈' },
    { name: 'Settings', href: '/settings', icon: '⚙️' },
  ];

  const links = role === 'admin' ? adminLinks : artisanLinks;

  if (!role) return null;

  return (
    <div className="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0 bg-slate-900">
      <div className="flex-1 flex flex-col min-h-0">
        <div className="flex items-center h-16 flex-shrink-0 px-4 bg-slate-900">
          <h1 className="text-xl font-bold text-white tracking-tight">KalaConnect<span className="text-indigo-400">AI</span></h1>
        </div>
        <div className="flex-1 flex flex-col overflow-y-auto">
          <nav className="flex-1 px-2 py-4 space-y-1">
            <div className="px-3 py-2 mb-4">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                {role === 'admin' ? 'Super Admin' : 'Shopkeeper'}
              </p>
            </div>
            {links.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="text-slate-300 hover:bg-slate-700 hover:text-white group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors"
              >
                <span className="mr-3 text-lg">{item.icon}</span>
                {item.name}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </div>
  );
}
