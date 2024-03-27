"use client";

import React, { useEffect, useState } from "react";
import SearchResult, { type ISearchItem } from "./SearchResult";
import { useAppDispatch } from "@/lib/store";
import SearchInputBox from "./SearchInputBox";

const SearchModal = () => {
  const [searchString, setSearchString] = useState("");

  // search dom manipulation
  useEffect(() => {
    const searchModal = document.getElementById("searchModal");
    const searchInput = document.getElementById("searchInput");
    const searchModalOverlay = document.getElementById("searchModalOverlay");
    const searchResultItems = document.querySelectorAll("#searchItem");
    const searchModalTriggers = document.querySelectorAll(
      "[data-search-trigger]",
    );

    // search modal open
    searchModalTriggers.forEach((button) => {
      button.addEventListener("click", function () {
        const searchModal = document.getElementById("searchModal");
        searchModal!.classList.add("show");
        searchInput!.focus();
      });
    });

    // search modal close
    searchModalOverlay!.addEventListener("click", function () {
      searchModal!.classList.remove("show");
    });

    // keyboard navigation
    let selectedIndex = -1;

    const updateSelection = () => {
      searchResultItems.forEach((item, index) => {
        if (index === selectedIndex) {
          item.classList.add("search-result-item-active");
        } else {
          item.classList.remove("search-result-item-active");
        }
      });

      searchResultItems[selectedIndex]?.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
      });
    };

    document.addEventListener("keydown", function (event) {
      if ((event.metaKey || event.ctrlKey) && event.key === "k") {
        searchModal!.classList.add("show");
        searchInput!.focus();
        updateSelection();
      }

      if (event.key === "ArrowUp" || event.key === "ArrowDown") {
        event.preventDefault();
      }

      if (event.key === "Escape") {
        searchModal!.classList.remove("show");
      }

      if (event.key === "ArrowUp" && selectedIndex > 0) {
        selectedIndex--;
      } else if (
        event.key === "ArrowDown" &&
        selectedIndex < searchResultItems.length - 1
      ) {
        selectedIndex++;
      } else if (event.key === "Enter") {
        const activeLink = document.querySelector(
          ".search-result-item-active a",
        ) as HTMLAnchorElement;
        if (activeLink) {
          activeLink?.click();
          searchModal!.classList.remove("show");
        }
      }

      updateSelection();
    });
  }, [searchString]);

  return (
    <div id="searchModal" className="search-modal px-5">
      <div id="searchModalOverlay" className="search-modal-overlay " />
      <div className="search-wrapper">
        <div className="search-wrapper-header">
          <SearchInputBox />
        </div>
        <SearchResult/>
        <div className="search-wrapper-footer">
          <span className="flex items-center">
            <kbd>
              <svg
                width="14"
                height="14"
                fill="currentcolor"
                viewBox="0 0 16 16"
              >
                <path d="M3.204 11h9.592L8 5.519 3.204 11zm-.753-.659 4.796-5.48a1 1 0 011.506.0l4.796 5.48c.566.647.106 1.659-.753 1.659H3.204a1 1 0 01-.753-1.659z"></path>
              </svg>
            </kbd>
            <kbd>
              <svg
                width="14"
                height="14"
                fill="currentcolor"
                viewBox="0 0 16 16"
              >
                <path d="M3.204 5h9.592L8 10.481 3.204 5zm-.753.659 4.796 5.48a1 1 0 001.506.0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 00-.753 1.659z"></path>
              </svg>
            </kbd>
            to navigate
          </span>
          <span className="flex items-center">
            <kbd>
              <svg
                width="12"
                height="12"
                fill="currentcolor"
                viewBox="0 0 16 16"
              >
                <path
                  fillRule="evenodd"
                  d="M14.5 1.5a.5.5.0 01.5.5v4.8a2.5 2.5.0 01-2.5 2.5H2.707l3.347 3.346a.5.5.0 01-.708.708l-4.2-4.2a.5.5.0 010-.708l4-4a.5.5.0 11.708.708L2.707 8.3H12.5A1.5 1.5.0 0014 6.8V2a.5.5.0 01.5-.5z"
                ></path>
              </svg>
            </kbd>
            to select
          </span>
          {searchString && (
            <span>
              <strong>{5} </strong> results - in{" "}
              <strong>{5} </strong> seconds
            </span>
          )}
          <span>
            <kbd>ESC</kbd> to close
          </span>
        </div>
      </div>
    </div>
  );
};

export default SearchModal;
