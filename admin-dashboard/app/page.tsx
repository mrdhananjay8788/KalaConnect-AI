import { redirect } from 'next/navigation';
import { getUserRole } from '../lib/auth';

export default function RootPage() {
  const role = getUserRole();
  if (role) {
    redirect('/dashboard');
  } else {
    redirect('/login');
  }
}
