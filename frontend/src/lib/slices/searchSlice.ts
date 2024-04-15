import { setCookie } from 'cookies-next';
import { PayloadAction, createSlice } from '@reduxjs/toolkit';
import { Options, SearchDataResponse } from '@/types';
import { searchApi } from '../api/searchApi';
import { useAppSelector } from '../store';
import extractSearchResults from '../utils/extractResult';
import { deleteAppStorage, getAppStorage, removeAppStorage, setAppStorage } from '../cookies';
import { redirect } from 'next/navigation';
import { toast } from 'react-toastify';

const options: Options = {
  storageType: "localStorage",
  encode: false,
};

const clearKeys = () => {
  deleteAppStorage('search-results', options);
  deleteAppStorage('search-query', options);
  deleteAppStorage('search-configurations', options);
  deleteAppStorage('retry-status');
}

const initialState: Partial<SearchDataResponse> = {
  query: "",
  isQueryChanged: true,
  searchResults: [],
  isResultsFetched: true,
};

const searchSlice = createSlice({
  name: 'search',
  initialState,
  reducers: {
    searchQueryChanged : (state, action: PayloadAction<any>) => {
      state.isQueryChanged = true;
    },
    retainState: (state, action: PayloadAction<any>) => {
      state.query                 = getAppStorage('search-query', options) || "";
      state.searchConfigurations  = JSON.parse(getAppStorage('search-configurations', options) || "{}");

      try {
        const obj = JSON.parse(getAppStorage('retry-status') ?? "{}");
        if(obj?.q === state.query) {
          console.log('research called...')
          const body = {
            searchConfig: { ...state.searchConfigurations, q: state.query, linkSite: obj.likeStatus ? obj.linkSite: '' }
          }
          console.log(body);
          searchApi.endpoints.getSearchResults.initiate(body);
        }
        else if (getAppStorage('search-results', options)) {
          state.searchResults       = JSON.parse(getAppStorage('search-results', options) || "[]");
        }
      }
      catch (e) {
        console.log(e)
      }
      console.log('retain state called .....');
      return state;
      /*

      const obj = JSON.parse(getAppStorage('retry-status') ?? "{}");
      if(Object.keys(obj).length > 0) {
        clearKeys();
        searchApi.endpoints.getSearchResults.initiate({
          searchConfig: { ...state.searchConfigurations, q: state.query, linkSite: obj.likeStatus ? obj.linkSite: '' }
        })
      } else {
        state.searchResults       = JSON.parse(getAppStorage('search-results', options) || "[]");
      }*/
    },
    searchConfigurationsChanged: (state, action: PayloadAction<any>) => {
      state.searchConfigurations = {
        ...state.searchConfigurations,
        ...action.payload
      };
      setAppStorage('search-configurations', JSON.stringify(state.searchConfigurations), options);
    },
    clearSearchResults: (state) => {
      clearKeys();

      state.query = '';
      state.isResultsFetched = true;
      state.searchInformation = {
        formattedSearchTime: "",
        formattedTotalResults: '',
        totalResults: '',
      };
      state.searchResults = [];
      state.isQueryChanged = false;
      // state
    }
  },
  extraReducers: (builder) => {
    builder
     .addMatcher(
        searchApi.endpoints.getSearchResults.matchFulfilled,
        (_state, { payload }) => {
          _state.query = payload.queries.request[0].title.replace("Google Custom Search - ", ""),
          _state.searchResults = extractSearchResults(payload);
          _state.isQueryChanged = false;

          console.log('............getSearchResults promise fulfilled ', payload);
          setAppStorage('search-results', JSON.stringify(_state.searchResults), options);
          setAppStorage('search-query', _state.query, options);
          setAppStorage('search-configurations', JSON.stringify(_state.searchConfigurations), options);
          setAppStorage('search-information', JSON.stringify(_state.searchInformation), options);
          deleteAppStorage('retry-status');
        }
     )
     .addMatcher(
      searchApi.endpoints.userReviewNoted.matchFulfilled,
      (_state, { payload }) => {
        // _state.searchResults = undefined;
        // removeAppStorage('search-results', options);
        // searchApi.endpoints.getSearchResults.initiate({
        //   searchConfig: { ..._state.searchConfigurations }
        // });
        // console.log('re-configuring results');
      }
    );
  }
});

export const { searchQueryChanged, retainState, searchConfigurationsChanged, clearSearchResults } = searchSlice.actions;
export default searchSlice.reducer;
