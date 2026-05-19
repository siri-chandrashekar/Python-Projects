"use client";

import { useState } from "react";

const BREWERY_TYPES = [
  "micro",
  "nano",
  "regional",
  "brewpub",
  "large",
  "planning",
  "bar",
  "contract",
  "proprietor",
  "closed",
];

function formatTypeLabel(type) {
  if (!type) return "Unknown";
  return type.charAt(0).toUpperCase() + type.slice(1);
}

function buildAddress(brewery) {
  const parts = [
    brewery.street,
    brewery.city,
    brewery.state,
    brewery.postal_code,
  ].filter(Boolean);

  return parts.length ? parts.join(", ") : "Address not available";
}

export default function Home() {
  const [city, setCity] = useState("");
  const [breweries, setBreweries] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [type, setType] = useState("");
  const [hasMore, setHasMore] = useState(true);
  const [hasSearched, setHasSearched] = useState(false);
  const [error, setError] = useState("");

  const searchBreweries = async (pageNumber = 1, selectedType = type) => {
    const trimmedCity = city.trim();
    if (!trimmedCity) return;

    setLoading(true);
    setError("");
    setHasSearched(true);

    try {
      let url = `https://api.openbrewerydb.org/v1/breweries?by_city=${encodeURIComponent(trimmedCity)}&page=${pageNumber}&per_page=12`;

      if (selectedType) {
        url += `&by_type=${selectedType}`;
      }

      const res = await fetch(url);
      if (!res.ok) {
        throw new Error("Unable to fetch breweries right now.");
      }

      const data = await res.json();
      setBreweries(Array.isArray(data) ? data : []);
      setPage(pageNumber);
      setHasMore(Array.isArray(data) && data.length === 12);
    } catch (fetchError) {
      console.error(fetchError);
      setBreweries([]);
      setHasMore(false);
      setError("Something went wrong while loading brewery data. Please try again.");
    }

    setLoading(false);
  };

  const clearSearch = () => {
    setCity("");
    setType("");
    setBreweries([]);
    setPage(1);
    setHasMore(true);
    setHasSearched(false);
    setError("");
  };

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(211,173,127,0.24),_transparent_28%),linear-gradient(180deg,_#140f0c_0%,_#201611_45%,_#0f0c0a_100%)] px-4 py-6 text-stone-100 sm:px-6 lg:px-8">
      <section className="mx-auto max-w-6xl">
        <div className="overflow-hidden rounded-[2rem] border border-white/10 bg-white/5 shadow-[0_30px_80px_rgba(0,0,0,0.35)] backdrop-blur">
          <div className="border-b border-white/10 px-6 py-12 sm:px-10">
            <p className="mb-4 text-sm font-semibold uppercase tracking-[0.3em] text-amber-200/80">
              Coffee and Brewery Search
            </p>
            <h1 className="max-w-3xl text-4xl font-bold tracking-tight text-white sm:text-5xl">
              BrewFinder
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-8 text-stone-300 sm:text-lg">
              Search breweries by city, filter by brewery type, and explore
              curated results from the Open Brewery DB in a cleaner, more
              polished discovery experience.
            </p>
          </div>

          <div className="px-6 py-8 sm:px-10">
            <div className="grid gap-4 lg:grid-cols-[1.5fr_1fr_auto_auto]">
              <input
                type="text"
                placeholder="Enter a city, for example Austin or Chicago"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                className="w-full rounded-2xl border border-white/10 bg-black/20 px-4 py-3 text-white outline-none transition placeholder:text-stone-400 focus:border-amber-300/60 focus:ring-2 focus:ring-amber-200/30"
              />

              <select
                value={type}
                onChange={(e) => setType(e.target.value)}
                className="w-full rounded-2xl border border-white/10 bg-black/20 px-4 py-3 text-white outline-none transition focus:border-amber-300/60 focus:ring-2 focus:ring-amber-200/30"
              >
                <option value="">All Types</option>
                {BREWERY_TYPES.map((breweryType) => (
                  <option key={breweryType} value={breweryType}>
                    {formatTypeLabel(breweryType)}
                  </option>
                ))}
              </select>

              <button
                onClick={() => searchBreweries(1, type)}
                disabled={loading || !city.trim()}
                className="rounded-2xl bg-amber-300 px-5 py-3 font-semibold text-stone-950 transition hover:bg-amber-200 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Searching..." : "Search"}
              </button>

              <button
                onClick={clearSearch}
                className="rounded-2xl border border-white/10 bg-white/5 px-5 py-3 font-semibold text-stone-100 transition hover:bg-white/10"
              >
                Clear
              </button>
            </div>

            <div className="mt-5 flex flex-wrap items-center justify-between gap-3 text-sm text-stone-300">
              <p>
                {hasSearched
                  ? `${breweries.length} result${breweries.length === 1 ? "" : "s"} found${city.trim() ? ` for ${city.trim()}` : ""}.`
                  : "Start by entering a city to explore breweries."}
              </p>
              <p>Powered by Open Brewery DB</p>
            </div>
          </div>
        </div>

        {error && (
          <div className="mt-6 rounded-2xl border border-red-300/20 bg-red-500/10 px-5 py-4 text-sm text-red-100">
            {error}
          </div>
        )}

        {loading && (
          <div className="mt-6 rounded-2xl border border-white/10 bg-white/5 px-5 py-4 text-center text-amber-100">
            Loading breweries...
          </div>
        )}

        {!loading && hasSearched && breweries.length === 0 && !error && (
          <div className="mt-6 rounded-[1.75rem] border border-dashed border-white/10 bg-white/5 px-6 py-12 text-center">
            <h2 className="text-2xl font-semibold text-white">No breweries found</h2>
            <p className="mt-3 text-stone-300">
              Try another city or change the brewery type filter.
            </p>
          </div>
        )}

        <div className="mt-8 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          {breweries.map((brewery) => (
            <article
              key={brewery.id || brewery.name}
              className="rounded-[1.75rem] border border-white/10 bg-[linear-gradient(180deg,rgba(255,255,255,0.08),rgba(255,255,255,0.04))] p-6 shadow-[0_18px_40px_rgba(0,0,0,0.2)] transition duration-300 hover:-translate-y-1 hover:border-amber-200/30 hover:shadow-[0_22px_48px_rgba(0,0,0,0.32)]"
            >
              <div className="mb-4 flex items-start justify-between gap-3">
                <div>
                  <h2 className="text-xl font-semibold text-white">
                    {brewery.name}
                  </h2>
                  <p className="mt-1 text-sm text-stone-300">
                    {brewery.city || "Unknown city"}
                    {brewery.state ? `, ${brewery.state}` : ""}
                  </p>
                </div>
                <span className="rounded-full border border-amber-200/20 bg-amber-200/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-amber-100">
                  {formatTypeLabel(brewery.brewery_type)}
                </span>
              </div>

              <p className="text-sm leading-7 text-stone-300">
                {buildAddress(brewery)}
              </p>

              <div className="mt-5 flex flex-wrap gap-3">
                {brewery.website_url ? (
                  <a
                    href={brewery.website_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center rounded-full bg-white px-4 py-2 text-sm font-semibold text-stone-900 transition hover:bg-amber-100"
                  >
                    Visit Website
                  </a>
                ) : (
                  <span className="inline-flex items-center rounded-full border border-white/10 px-4 py-2 text-sm text-stone-400">
                    No website listed
                  </span>
                )}
              </div>
            </article>
          ))}
        </div>

        {breweries.length > 0 && (
          <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
            <button
              onClick={() => {
                if (page > 1) searchBreweries(page - 1);
              }}
              disabled={page === 1}
              className="rounded-full border border-white/10 bg-white/5 px-5 py-2.5 font-medium text-stone-100 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-40"
            >
              Previous
            </button>

            <span className="rounded-full border border-white/10 bg-black/20 px-4 py-2 text-sm text-stone-200">
              Page {page}
            </span>

            <button
              onClick={() => searchBreweries(page + 1)}
              disabled={!hasMore}
              className="rounded-full bg-amber-300 px-5 py-2.5 font-medium text-stone-950 transition hover:bg-amber-200 disabled:cursor-not-allowed disabled:opacity-40"
            >
              Next
            </button>
          </div>
        )}
      </section>
    </main>
  );
}
