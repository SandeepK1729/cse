import { searchApi } from "@/lib/api";
import { getValidAuthTokens } from "@/lib/cookies";
import { clearSearchResults, searchQueryChanged } from "@/lib/slices/searchSlice";
import { useAppDispatch, useAppSelector } from "@/lib/store";
import { useState } from "react";
import { toast } from "react-toastify";
import { FaTruckLoading } from "react-icons/fa";
import DynamicIcon from "@/helpers/DynamicIcon";
import { AiOutlineLoading } from "react-icons/ai";

const SearchInputBox = () => {
  const { query, isResultsFetched, searchConfig } = useAppSelector((state) => ({
    query: state.search.query, 
    isResultsFetched: state.search.isResultsFetched
  }));
  const dispatch  = useAppDispatch();
  
  const [searchString, setSearchString] = useState("");

  const doSearch = () => {
    if (searchString === undefined || searchString === "" || searchString === query) {
      return;
    }
    toast("Searching results for " + searchString, {
      position: "top-center",
      autoClose: 5000,
      hideProgressBar: true,
      closeOnClick: false,
      pauseOnHover: false,
      draggable: true,
      progress: undefined,
    });
    dispatch(searchQueryChanged({ q: searchString, isResultsFetched: false }));
    dispatch(searchApi.endpoints.getSearchResults.initiate({
      searchConfig: { q : searchString },
    }));
  }

  const handleSearchClear = () => {
    setSearchString("");
    dispatch(clearSearchResults());
  }

  return (
    <>
      <form onSubmit={(e) => { e.preventDefault(); doSearch(); }}>
        <label
          htmlFor="searchInput"
          className="absolute left-7 top-[calc(50%-7px)]"
        >
          {!isResultsFetched ? <AiOutlineLoading /> : 
          searchString ? (
            <svg
              onClick={() => setSearchString("")}
              viewBox="0 0 512 512"
              height="18"
              width="18"
              className="hover:text-red-500 cursor-pointer -mt-0.5"
            >
              <path
                fill="currentcolor"
                d="M256 512A256 256 0 10256 0a256 256 0 100 512zM175 175c9.4-9.4 24.6-9.4 33.9.0l47 47 47-47c9.4-9.4 24.6-9.4 33.9.0s9.4 24.6.0 33.9l-47 47 47 47c9.4 9.4 9.4 24.6.0 33.9s-24.6 9.4-33.9.0l-47-47-47 47c-9.4 9.4-24.6 9.4-33.9.0s-9.4-24.6.0-33.9l47-47-47-47c-9.4-9.4-9.4-24.6.0-33.9z"
              ></path>
            </svg>
          ) : (
            <svg
              viewBox="0 0 512 512"
              height="18"
              width="18"
              className="-mt-0.5"
            >
              <path
                fill="currentcolor"
                d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8.0 45.3s-32.8 12.5-45.3.0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9.0 208S93.1.0 208 0 416 93.1 416 208zM208 352a144 144 0 100-288 144 144 0 100 288z"
              ></path>
            </svg>
          )}
        </label>
        <input
          id="searchInput"
          placeholder={query === "" ? "Search...": query}
          className="search-wrapper-header-input"
          type="input"
          name="search"
          value={searchString ?? query}
          onChange={(e: any) => {
            setSearchString(e.currentTarget.value.replace("\\", ""));
          }}
          autoFocus
          autoComplete="on"
        />
      </form>

      <button
      className="absolute right-7 top-[calc(50%-7px)]"
      onClick={handleSearchClear}
      >
      <svg
          viewBox="0 0 512 512"
          height="18"
          width="18"
          className="hover:text-blue-500 cursor-pointer -mt-0.5"
        >
          <path
            fill="currentcolor"
            d="M256 512A256 256 0 10256 0a256 256 0 100 512zM175 175c9.4-9.4 24.6-9.4 33.9.0l47 47 47-47c9.4-9.4 24.6-9.4 33.9.0s9.4 24.6.0 33.9l-47 47 47 47c9.4 9.4 9.4 24.6.0 33.9s-24.6 9.4-33.9.0l-47-47-47 47c-9.4 9.4-24.6 9.4-33.9.0s-9.4-24.6.0-33.9l47-47-47-47c-9.4-9.4-9.4-24.6.0-33.9z"
          ></path>
        </svg>
      </button>
    </>
  )
}

export default SearchInputBox;
