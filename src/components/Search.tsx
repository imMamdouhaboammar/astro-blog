import Fuse from "fuse.js";
import { useEffect, useRef, useState, useMemo } from "react";
import type { CollectionEntry } from "astro:content";

export type SearchItem = {
  title: string;
  description: string;
  data: CollectionEntry<"blog">["data"];
  slug: string;
};

interface Props {
  searchList: SearchItem[];
}

interface SearchResult {
  item: SearchItem;
  refIndex: number;
}

export default function SearchBar({ searchList }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [inputVal, setInputVal] = useState("");
  const [searchResults, setSearchResults] = useState<SearchResult[] | null>(
    null
  );

  const handleChange = (e: React.FormEvent<HTMLInputElement>) => {
    setInputVal(e.currentTarget.value);
  };

  const fuse = useMemo(
    () =>
      new Fuse(searchList, {
        keys: ["title", "description", "data.tags"],
        includeMatches: true,
        minMatchCharLength: 2,
        threshold: 0.4,
      }),
    [searchList]
  );

  useEffect(() => {
    const searchUrl = new URLSearchParams(window.location.search);
    const searchStr = searchUrl.get("q");
    if (searchStr) setInputVal(searchStr);

    setTimeout(function () {
      if (inputRef.current) {
        inputRef.current.selectionStart = inputRef.current.selectionEnd =
          searchStr?.length || 0;
      }
    }, 50);
  }, []);

  useEffect(() => {
    const inputResult = inputVal.trim().length > 1 ? fuse.search(inputVal) : [];
    setSearchResults(inputResult);

    if (inputVal.trim().length > 0) {
      const searchParams = new URLSearchParams(window.location.search);
      searchParams.set("q", inputVal);
      const newRelativePathQuery =
        window.location.pathname + "?" + searchParams.toString();
      history.replaceState(history.state, "", newRelativePathQuery);
    } else {
      history.replaceState(history.state, "", window.location.pathname);
    }
  }, [inputVal, fuse]);

  const countText =
    searchResults?.length === 1
      ? "بلاي بوك واحد"
      : searchResults?.length === 2
        ? "2 بلاي بوك"
        : `${searchResults?.length ?? 0} بلاي بوكس`;

  return (
    <div className="search-container">
      <div className="search-input-wrapper">
        <input
          className="search-input"
          placeholder="ابحث في البلاي بوكس والمقالات..."
          type="search"
          name="search"
          value={inputVal}
          onChange={handleChange}
          autoComplete="off"
          ref={inputRef}
          aria-label="ابحث في البلاي بوكس"
          dir="auto"
        />
      </div>

      {inputVal.trim().length > 1 && (
        <div className="search-status" role="status" aria-live="polite">
          تم العثور على {countText} لـ &ldquo;{inputVal}&rdquo;
        </div>
      )}

      {inputVal.trim().length > 1 && searchResults?.length === 0 && (
        <p className="search-empty">
          جرّب كلمة مختلفة أو ابحث باسم الموضوع بدلًا من عنوانه الكامل.
        </p>
      )}

      {searchResults && searchResults.length > 0 && (
        <ul className="search-results-list" role="list">
          {searchResults.map(({ item, refIndex }) => (
            <li key={`${refIndex}-${item.slug}`} className="search-result-item">
              <a href={`/posts/${item.slug}/`}>
                <h3 dir="auto">{item.title}</h3>
                {item.description !== item.title && (
                  <p dir="auto">{item.description}</p>
                )}
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
