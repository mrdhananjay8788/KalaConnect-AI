import { cookies } from 'next/headers';

export type Role = 'admin' | 'artisan' | null;

export function getUserRole(): Role {
  const cookieStore = cookies();
  const roleCookie = cookieStore.get('user_role');
  return (roleCookie?.value as Role) || null;
}
