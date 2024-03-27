// store/authApi.ts
import { LoginRequest, LoginResponse, SignupRequest, SignupResponse } from '@/types';
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const authApi = createApi({
  reducerPath: 'authApi',
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.API_URL ?? 'http://127.0.0.1:8000',
  }),
  tagTypes: ['post', 'UNAUTHORIZED', 'UNKNOWN_ERROR'],
  endpoints: (builder) => ({
    login: builder.mutation<LoginResponse, LoginRequest>({
      query: ({ username, password }) => ({
        url: '/api/token/',
        method: 'POST',
        body: {
          username,
          password,
        },
      }),
      // providesTags: (result, error, arg) => {
      //   console.log("tags result ", result);
      //   return result.success ? [{ type: 'login', id: 'LIST' }] : [{ type: 'UNAUTHORIZED' }];
      // }
    }),
    signup: builder.mutation<SignupResponse, SignupRequest>({
      query: (payload) => ({
        url: '/api/signup/',
        method: 'POST',
        body: payload,
      }),
      // providesTags: (result, error, arg) => {
      //   console.log("tags result ", result);
      //   return result.success ? [{ type: 'login', id: 'LIST' }] : [{ type: 'UNKNOWN_ERROR' }];
      // }
    }),
    getAuthData: builder.query<LoginResponse, { token: string }>({
      query: ({ token }) => ({
        url: 'api/profile',
        // this is the default but I'm leaving it here for reference
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }),
    }),
  }),
});

export const { useLoginMutation, useSignupMutation, useGetAuthDataQuery } = authApi;