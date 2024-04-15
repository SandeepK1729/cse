// {
//   "kind": "customsearch#result",
//   "title": "Hello - Wikipedia",
//   "htmlTitle": "<b>Hello</b> - Wikipedia",
//   "link": "https://en.wikipedia.org/wiki/Hello",
//   "displayLink": "en.wikipedia.org",
//   "snippet": "Etymology · According to the Oxford English Dictionary, hello is an alteration of hallo, hollo, which came from · Bill Bryson · The use of hello as a telephone ...",
//   "htmlSnippet": "Etymology &middot; According to the Oxford English Dictionary, <b>hello</b> is an alteration of hallo, hollo, which came from &middot; Bill Bryson &middot; The use of <b>hello</b> as a telephone&nbsp;...",
//   "cacheId": "ZW__FDER0tIJ",
//   "formattedUrl": "https://en.wikipedia.org/wiki/Hello",
//   "htmlFormattedUrl": "https://en.wikipedia.org/wiki/<b>Hello</b>",
//   "pagemap": {
//       "metatags": [
//           {
//               "referrer": "origin",
//               "og:image": "https://upload.wikimedia.org/wikipedia/commons/b/b3/TelephoneHelloNellie.jpg",
//               "theme-color": "#eaecf0",
//               "og:image:width": "1200",
//               "og:type": "website",
//               "viewport": "width=device-width, initial-scale=1.0, user-scalable=yes, minimum-scale=0.25, maximum-scale=5.0",
//               "og:title": "Hello - Wikipedia",
//               "og:image:height": "2042",
//               "format-detection": "telephone=no"
//           }
//       ]
//   },
//   "priority_score": 0.4183849692344666
// },

export type SearchApiResponse = {
  kind: string;
  url: {
    type: string;
    template: string;
  };
  queries: {
    request: Array<{
      title: string;
      totalResults: string;
      searchTerms: string;
      count: number;
      startIndex: number;
      inputEncoding: string;
      outputEncoding: string;
      safe: string;
      cx: string;
    }>;
    nextPage: Array<{
      title: string;
      totalResults: string;
      searchTerms: string;
      count: number;
      startIndex: number;
      inputEncoding: string;
      outputEncoding: string;
      safe: string;
      cx: string;
    }>;
  };
  context: {
    title: string;
  };
  searchInformation: {
    searchTime: number;
    formattedSearchTime: string;
    totalResults: string;
    formattedTotalResults: string;
  };
  items: Array<{
    kind: string;
    title: string;
    htmlTitle: string;
    link: string;
    displayLink: string;
    snippet: string;
    htmlSnippet: string;
    cacheId: string;
    formattedUrl: string;
    htmlFormattedUrl: string;
    pagemap: {
      cse_thumbnail: Array<{
        src: string;
        width: string;
        height: string;
      }>;
      metatags: Array<{
        [key: string]: string;
      }>;
      cse_image: Array<{
        src: string;
      }>;
    };
    priority_score: number;
  }>;
};

export type SearchResult = {
  title:  string;
  html_title: string;

  link: string;
  display_link: string;

  formatted_url: string;
  html_formatted_url: string;

  snippet: string;
  html_snippet: string;

  priority_score: number;
  cacheId: string;

  pagemap: {
    cse_thumbnail: Array<{
      src: string;
      width: string;
      height: string;
    }>;
    metatags: Array<{
      [key: string]: string;
    }>;
    cse_image: Array<{
      src: string;
    }>;
  };
}

export type SearchRequestConfiguration = {
  q: string;
  data_type: 'any' | 'image' | 'video' | 'news' | 'shopping'; // set default to 'any'
  start_date: Date;
  end_date: Date;
  highlight: boolean;
  matchMarker: boolean;
  caseSensitive: boolean;
  sort: string;
  siteSearch: string;
  siteSearchFilter: 'i' | 'e';
  linkSite: string;
}

export type SearchDataResponse = {
  query: string;
  searchConfigurations: SearchRequestConfiguration;
  isResultsFetched: boolean;
  searchInformation: {
    formattedSearchTime: string;
    formattedTotalResults: string;
    totalResults: string;
  };
  searchResults: Array<SearchResult>;
  isQueryChanged: boolean;
}

export type Options = {
  storageType: "localStorage" | "sessionStorage" | "cookieStorage" | undefined;
  encode: boolean;
}
