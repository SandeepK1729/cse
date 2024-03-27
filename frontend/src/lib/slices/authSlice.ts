import { setCookie } from 'cookies-next';
import { createSlice } from '@reduxjs/toolkit';
import { authApi } from '../api/authApi';
import { LoginResponse } from '@/types';

const initialState: Partial<LoginResponse> = {};
  
// store/auth.ts
const setAuthCookie = (token: string, name: string) => {
  const toBase64 = Buffer.from(token).toString('base64');

  setCookie(name, toBase64, {
    maxAge: 30 * 24 * 60 * 60,
    path: '/',
    // more security options here
    // sameSite: 'strict',
    // httpOnly: true,
    // secure: process.env.NODE_ENV === 'production',
  });
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
  },
  extraReducers: (builder) => {
    builder
      .addMatcher(
        authApi.endpoints.login.matchFulfilled,
        (_state, { payload }) => {
          console.log('login promise fulfilled ', payload);
          // set the token in the cookies
          setAuthCookie(payload.access, 'auth_token');
          setAuthCookie(payload.refresh, 'refresh_token');

          // store the user data in the store
          // "mutation" also works
          // state = payload;
          return payload;
        }
      )
      .addMatcher(
        authApi.endpoints.signup.matchFulfilled,
        (_state, { payload }) => {
          console.log('signup promise fulfilled ', payload);
          // set the token in the cookies
          setAuthCookie(payload.token.access, 'auth_token');
          setAuthCookie(payload.token.refresh, 'refresh_token');

          // store the user data in the store
          // "mutation" also works
          // state = payload;
          return payload;
        }
      )
      .addMatcher(
        authApi.endpoints.getAuthData.matchFulfilled,
        (_state, { payload }) => {
          // in case we receive a new token when refetching the details
          setAuthCookie(payload.access, 'auth_token');
          return payload;
        }
      );
  },
});

export const { } = authSlice.actions;
export default authSlice.reducer;
