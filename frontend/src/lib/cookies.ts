// lib/cookies.ts
"use client";
import { deleteCookie, getCookie, setCookie } from 'cookies-next';

// helpers to get cookies
const getAuthCookie = (name: string) => {
  const cookie = getCookie(name);

  if (!cookie) return undefined;

  return Buffer.from(cookie, 'base64').toString('ascii');
};

export const setAppStorage = (name: string, value: string, options: object = {}) => {
  const toBase64 = (options?.encode ?? true) ? Buffer.from(value).toString('base64') : value;

  console.log('setting cookie: ', name, toBase64, options);
  switch (options?.storageType) {
    case 'localStorage':
      localStorage.setItem(name, toBase64);
      break;
    case'sessionStorage':
      sessionStorage.setItem(name, toBase64);
      break;
    default:
      setCookie(name, toBase64, { maxAge: 30 * 24 * 60 * 60,
        path: '/',
        ...options,
        // more security options here
        // sameSite: 'strict',
        // httpOnly: true,
        // secure: process.env.NODE_ENV === 'production',
      });
  }
};

export const getAppStorage = (name: string, options: Object = {}) => {
  let val = undefined;
  switch (options?.storageType) {
    case 'localStorage':
      val = localStorage.getItem(name);
      break;
    case'sessionStorage':
      val = sessionStorage.getItem(name);
      break;
    default:
      val = getCookie(name);
  }

  if (!val) return undefined;

  if (options?.encode ?? true) 
    return Buffer.from(val, 'base64').toString('ascii');
  
  return val;
};

export const deleteAppStorage = (name: string, options: Object = {}) => {
  switch (options?.storageType) {
    case 'localStorage':
      localStorage.removeItem(name);
      break;
    case'sessionStorage':
      sessionStorage.removeItem(name);
      break;
    default:
      deleteCookie(name);
  }
};

export const removeAppStorage = (name: string, options: Object = {}) => {
  switch (options?.storageType) {
    case 'localStorage':
      localStorage.removeItem(name);
      break;
    case'sessionStorage':
      sessionStorage.removeItem(name);
      break;
    default:
      deleteCookie(name);
  }
}

export const getValidAuthTokens = () => {
  const token = getAuthCookie('auth_token');

  const now = new Date();
  const tokenDate = new Date(token || 0);

  return {
    token: token
  };
};
