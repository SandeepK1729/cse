import { createSlice } from '@reduxjs/toolkit';
import { authApi } from '../api/authApi';
import { LoginResponse } from '@/types';
import { setAppStorage } from '../cookies';

const initialState: Partial<LoginResponse> = {};
  
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
          setAppStorage('auth_token', payload.access);
          setAppStorage('refresh_token', payload.refresh);

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
          setAppStorage('auth_token', payload.token.access);
          setAppStorage('refresh_token', payload.token.refresh);

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
          // setAppStorage('auth_token', payload.access);
          return payload;
        }
      );
  },
});

export const { } = authSlice.actions;
export default authSlice.reducer;
