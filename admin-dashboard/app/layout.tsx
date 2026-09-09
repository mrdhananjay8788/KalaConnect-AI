import { getUserRole } from '../lib/auth';
import Sidebar from '../components/layout/Sidebar';
import Header from '../components/layout/Header';
import './globals.css';

export const metadata = {
  title: 'KalaConnect-AI Dashboard',
  description: 'Admin and Artisan Dashboard for KalaConnect-AI',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const role = getUserRole();

  return (
    <html lang="en">
      <body className="h-screen bg-gray-50 flex overflow-hidden font-sans text-slate-900">
        {role && <Sidebar />}
        <div className={`flex flex-col w-0 flex-1 overflow-hidden ${role ? 'md:ml-64' : ''}`}>
          {role && <Header role={role} />}
          <main className="flex-1 relative z-0 overflow-y-auto focus:outline-none">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
