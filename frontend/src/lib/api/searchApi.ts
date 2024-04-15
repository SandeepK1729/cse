import { Options, SearchApiResponse, SearchRequestConfiguration, SearchResult } from "@/types";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { getAppStorage } from "../cookies";

const options: Options = {
  storageType: "localStorage",
  encode: false,
};

export const searchApi = createApi({
  reducerPath: 'searchApi',
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.API_URL ?? 'http://127.0.0.1:8000',
  }),
  endpoints: (builder) => ({
    getSearchResults: builder.query<SearchApiResponse, { searchConfig: Partial<SearchRequestConfiguration> }>({
      query: ({ searchConfig }) => ({
        url: '/api/search/',
        method: 'POST',
        body: { ...searchConfig, ...JSON.parse(getAppStorage('search-configurations', options) ?? "{}") },
        headers: {
          Authorization: 'Bearer ' + getAppStorage('auth_token'),
        },
      }),
      providesTags: (result) => {
        console.log(
          'getSearchResults providesTags result ',
          result,
        );
        
        return result ? [{ type: 'SearchResults' }] : [];
      }
    }),
    userReviewNoted: builder.mutation<{ redirect: Boolean }, { 
      currentPage: SearchResult, 
      userReview: boolean,
      query: string
    }>({
      query: ({ currentPage, userReview, query }) => ({
        url: '/api/feedback/',
        method: 'POST',
        body: { ...currentPage, feedback: userReview, query },
        headers: {
          Authorization: 'Bearer ' + getAppStorage('auth_token'),
        },
      }),
      invalidatesTags: [{ type: 'SearchResults' }],
    }),
  }),
});

export const { useGetSearchResultsQuery, useUserReviewNotedMutation } = searchApi;
