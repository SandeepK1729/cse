import { SearchApiResponse, SearchResult } from "@/types";

const extractSearchResults = (response: SearchApiResponse): Array<SearchResult> => { 
  const { items } = response;
  const searchResults: SearchResult[] = items.map((item) => {
    const {
      title,
      htmlTitle,
      link,
      displayLink,
      snippet,
      htmlSnippet,
      cacheId,
      formattedUrl,
      htmlFormattedUrl,
      pagemap,
      priority_score,
    } = item;
    return {
      q: response.queries.request[0].searchTerms,
      title,
      html_title: htmlTitle,

      link,
      display_link: displayLink,

      formatted_url: formattedUrl,
      html_formatted_url: htmlFormattedUrl,

      snippet,
      html_snippet: htmlSnippet,

      priority_score,
      cacheId,

      pagemap,
    };
  });
  return searchResults;
};

export default extractSearchResults;
