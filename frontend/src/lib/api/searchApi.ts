import { SearchApiResponse, SearchRequestConfiguration } from "@/types";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const searchApi = createApi({
  reducerPath: 'searchApi',
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.API_URL ?? 'http://127.0.0.1:8000',
  }),
  endpoints: (builder) => ({
    getSearchResults: builder.query<SearchApiResponse, { token: string, searchConfig: Partial<SearchRequestConfiguration> }>({
      query: ({ token, searchConfig }) => ({
        url: '/api/search/',
        method: 'POST',
        body: searchConfig,
        headers: {
          // contentType: 'application/json',
          // accept: 'application/json',
          Authorization: 'Bearer ' + token,
        },
      }),
    }),
  }),
});

export const { useGetSearchResultsQuery } = searchApi;
