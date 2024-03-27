import { setCookie } from 'cookies-next';
import { createSlice } from '@reduxjs/toolkit';
import { SearchDataResponse } from '@/types';
import { searchApi } from '../api/searchApi';
import { useAppSelector } from '../store';
import extractSearchResults from '../utils/extractResult';

const initialState: Partial<SearchDataResponse> = {
  query: "",
  searchResults: [],
};

const setSearchCookie = (key: string, value: string) => {
  const toBase64 = Buffer.from(value).toString('base64');

  setCookie(key, toBase64, {
    maxAge: 24 * 60 * 60,
    path: '/',
    // more security options here
    // sameSite: 'strict',
    // httpOnly: true,
    // secure: process.env.NODE_ENV === 'production',
  });
};

const searchSlice = createSlice({
  name: 'search',
  initialState,
  reducers: {
  },
  extraReducers: (builder) => {
    builder
     .addMatcher(
        searchApi.endpoints.getSearchResults.matchFulfilled,
        (_state, { payload }) => {
          console.log('search promise fulfilled ', payload);
          // set the token in the cookies
          console.log('current state: ',_state);
          console.log('payload: ',payload);

          // store the user data in the store
          // "mutation" also works
          // state = payload;

          // update the state.search.results = payload;
          _state.query = payload.queries.request[0].title.replace("Google Custom Search - ", ""),
          _state.searchResults = extractSearchResults(payload);
          
        }
     )
  }
});

export const { } = searchSlice.actions;
export default searchSlice.reducer;
