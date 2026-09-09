'use server'

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

export async function loginAsAdmin() {
  cookies().set('user_role', 'admin', { path: '/' });
  redirect('/dashboard');
}

export async function loginAsArtisan() {
  cookies().set('user_role', 'artisan', { path: '/' });
  redirect('/dashboard');
}

export async function logout() {
  cookies().delete('user_role');
  redirect('/login');
}
