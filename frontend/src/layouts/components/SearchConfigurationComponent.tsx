"use client";

import { searchConfigurationsChanged } from '@/lib/slices/searchSlice';
import { useAppDispatch, useAppSelector } from '@/lib/store';
import { SearchRequestConfiguration } from '@/types';
import { Input } from '@mui/material';
import { useState } from 'react';
import Datepicker from "react-tailwindcss-datepicker";

const SearchConfigurationComponent = () => {
  const dispatch = useAppDispatch();
  const updateSearchConfigurations = async (config: Partial<SearchRequestConfiguration>) => {
    dispatch(searchConfigurationsChanged(config));
  }

  const searchConfig = useAppSelector((state) => state.search.searchConfigurations);

  const [showConfig, setShowConfig] = useState(false);
  return (
    <div className="flex w-100">
      <button className='flex-start' onClick={() => setShowConfig(!showConfig)}>
        <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
          <path stroke="currentColor" stroke-linecap="round" stroke-width="2" d="M20 6H10m0 0a2 2 0 1 0-4 0m4 0a2 2 0 1 1-4 0m0 0H4m16 6h-2m0 0a2 2 0 1 0-4 0m4 0a2 2 0 1 1-4 0m0 0H4m16 6H10m0 0a2 2 0 1 0-4 0m4 0a2 2 0 1 1-4 0m0 0H4"/>
        </svg>

      </button>
      <div className='flex flex-wrap'>
        {showConfig && (
          <>
            <div className="search-config flex gap-3">
              <div className="search-config-label">
                <label>
                  <input
                    type="checkbox"
                    checked={searchConfig?.highlight ?? false}
                    onChange={(e) => {
                      updateSearchConfigurations({ highlight: e.target.checked })
                    }
                    }
                  />
                  Highlight
                </label>
              </div>
              <div className="search-config-label">
                <label>
                  <input
                    type="checkbox"
                    checked={searchConfig?.matchMarker ?? false}
                    onChange={(e) => updateSearchConfigurations({ matchMarker: e.target.checked })}
                  />
                  Match Marker
                </label>
              </div>
              <div className="search-config-label">
                <label>
                  <input
                    type="checkbox"
                    checked={searchConfig?.caseSensitive ?? false}
                    onChange={(e) => updateSearchConfigurations({ caseSensitive: e.target.checked })}
                  />
                  Case Sensitive
                </label>
              </div>
            </div>
            <br/>
            <div className="search-config" style={{ zIndex: 999, width: '100%' }}>
              <Datepicker
                separator='to'
                maxDate={new Date()}
                showFooter={true}
                placeholder={"Select Date Range"} 
                primaryColor={"blue"}
                value={{ startDate: searchConfig?.start_date ?? null, endDate: searchConfig?.end_date ?? null }} 
                onChange={(e) => updateSearchConfigurations({
                  start_date: e?.startDate,
                  end_date: e?.endDate
                })}
                showShortcuts={true} 
              />
            </div>
            <form className="">
              <div>
                
                <select
                  onChange={(e) => updateSearchConfigurations({
                    siteSearchFilter: e.target.value
                  })}
                  id="Selection Type" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                  <option selected={searchConfig?.siteSearchFilter === 'i'} value={'i'}>Search From</option>
                  <option selected={searchConfig?.siteSearchFilter === 'e'} value={'e'}>Exclude From</option>
                </select>

                <input 
                  type="text" 
                  onChange={(e) => updateSearchConfigurations({
                    siteSearch: e.target.value
                  })}
                  value={searchConfig?.siteSearch}
                  id="small-input" 
                  className="block w-full p-2 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 text-xs focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-700 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" 
                />
              </div>
            </form>
          </>
        )}
      </div>
    </div>
  )
}

export default SearchConfigurationComponent;
