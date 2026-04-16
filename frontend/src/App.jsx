import { useState } from "react";

/* ═══════════════════════════════════════════════════════
   AmalGus — Smart Product Discovery  (single-page UI)
   ═══════════════════════════════════════════════════════ */

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const CATEGORIES = [
  "Tempered Glass",
  "Laminated Glass",
  "Insulated Glass Unit",
  "Float Glass",
  "Tinted Glass",
  "Mirror Glass",
  "Decorative Glass",
  "Safety Glass",
  "Aluminium Hardware",
  "Sealants & Accessories",
];

/* ── Helpers ──────────────────────────────────────────── */

/** Return a Tailwind-friendly color class set based on the score */
function scoreColor(score) {
  if (score >= 60) return { text: "text-emerald-600", bg: "bg-emerald-50", bar: "score-bar-high", ring: "ring-emerald-200" };
  if (score >= 40) return { text: "text-amber-600", bg: "bg-amber-50", bar: "score-bar-mid", ring: "ring-amber-200" };
  return { text: "text-red-500", bg: "bg-red-50", bar: "score-bar-low", ring: "ring-red-200" };
}

/** Format price with dollar sign */
function fmtPrice(p) {
  return `$${Number(p).toFixed(2)}`;
}

/* ── SVG Icons (inline, no deps) ──────────────────────── */

function SearchIcon({ className = "w-5 h-5" }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-4.35-4.35M11 19a8 8 0 100-16 8 8 0 000 16z" />
    </svg>
  );
}

function SpinnerIcon({ className = "w-6 h-6" }) {
  return (
    <svg className={`animate-spin ${className}`} fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
    </svg>
  );
}

function GlassIcon({ className = "w-16 h-16" }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 64 64" stroke="currentColor" strokeWidth={1.5}>
      <rect x="8" y="8" width="48" height="48" rx="6" className="stroke-indigo-300" />
      <line x1="8" y1="32" x2="56" y2="32" className="stroke-indigo-200" />
      <line x1="32" y1="8" x2="32" y2="56" className="stroke-indigo-200" />
      <rect x="14" y="14" width="16" height="16" rx="2" fill="currentColor" className="text-indigo-100" />
    </svg>
  );
}

function EmptyIcon({ className = "w-20 h-20" }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 80 80" stroke="currentColor" strokeWidth={1.5}>
      <circle cx="40" cy="35" r="18" className="stroke-slate-300" />
      <line x1="53" y1="48" x2="64" y2="59" className="stroke-slate-300" strokeWidth={3} strokeLinecap="round" />
      <line x1="32" y1="35" x2="48" y2="35" className="stroke-slate-300" />
    </svg>
  );
}

/* ── Product Card ─────────────────────────────────────── */

function ProductCard({ product, index }) {
  const sc = scoreColor(product.match_score);
  const specs = product.specifications || {};
  const [imgError, setImgError] = useState(false);
  const hasImage = product.image_url && !imgError;

  const specEntries = Object.entries(specs).filter(
    ([, v]) => v && v !== "N/A"
  );

  return (
    <div
      className={`animate-fade-in-up stagger-${index + 1} group bg-white rounded-2xl shadow-sm hover:shadow-xl border border-slate-100 hover:border-indigo-200 transition-all duration-300 overflow-hidden flex flex-col`}
    >
      {/* Image / Placeholder */}
      <div className="relative h-48 bg-gradient-to-br from-slate-50 to-indigo-50 overflow-hidden">
        {hasImage ? (
          <img
            src={product.image_url}
            alt={product.product_name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            onError={() => setImgError(true)}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <GlassIcon className="w-16 h-16 text-indigo-300 group-hover:scale-110 transition-transform duration-300" />
          </div>
        )}

        {/* Score badge (top-right) */}
        <div
          className={`absolute top-3 right-3 ${sc.bg} ${sc.text} ring-1 ${sc.ring} px-3 py-1 rounded-full text-sm font-bold shadow-sm`}
        >
          {product.match_score}%
        </div>

        {/* Category pill (bottom-left) */}
        <div className="absolute bottom-3 left-3 bg-white/80 backdrop-blur-sm text-xs font-medium text-slate-600 px-2.5 py-1 rounded-full shadow-sm">
          {product.category}
        </div>
      </div>

      {/* Body */}
      <div className="p-5 flex flex-col flex-1">
        {/* Title + Supplier */}
        <h3 className="text-base font-semibold text-slate-800 leading-snug mb-1 group-hover:text-indigo-700 transition-colors">
          {product.product_name}
        </h3>
        <p className="text-xs text-slate-400 mb-3">{product.supplier}</p>

        {/* Score bar */}
        <div className="w-full bg-slate-100 rounded-full h-1.5 mb-3 overflow-hidden">
          <div
            className={`h-full rounded-full ${sc.bar} transition-all duration-700`}
            style={{ width: `${Math.min(product.match_score, 100)}%` }}
          />
        </div>

        {/* Explanation */}
        <p className="text-sm text-slate-500 mb-4 leading-relaxed line-clamp-2">
          {product.explanation}
        </p>

        {/* Specs chips */}
        {specEntries.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-4">
            {specEntries.slice(0, 4).map(([key, val]) => (
              <span
                key={key}
                className="text-[11px] bg-slate-50 text-slate-500 border border-slate-200 px-2 py-0.5 rounded-md"
              >
                <span className="font-medium text-slate-600 capitalize">{key.replace("_", " ")}</span>: {val}
              </span>
            ))}
            {specEntries.length > 4 && (
              <span className="text-[11px] text-slate-400 px-2 py-0.5">+{specEntries.length - 4} more</span>
            )}
          </div>
        )}

        {/* Price (pushed to bottom) */}
        <div className="mt-auto pt-3 border-t border-slate-100 flex items-center justify-between">
          <span className="text-lg font-bold text-slate-800">{fmtPrice(product.price)}</span>
          <span className="text-xs text-slate-400">per unit</span>
        </div>
      </div>
    </div>
  );
}

/* ── Loading Skeleton ─────────────────────────────────── */

function SkeletonCard() {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
      <div className="h-48 animate-shimmer" />
      <div className="p-5 space-y-3">
        <div className="h-4 w-3/4 rounded animate-shimmer" />
        <div className="h-3 w-1/2 rounded animate-shimmer" />
        <div className="h-1.5 w-full rounded-full animate-shimmer" />
        <div className="h-3 w-full rounded animate-shimmer" />
        <div className="h-3 w-2/3 rounded animate-shimmer" />
        <div className="flex gap-2 pt-2">
          <div className="h-5 w-16 rounded animate-shimmer" />
          <div className="h-5 w-20 rounded animate-shimmer" />
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════
   Main App
   ═══════════════════════════════════════════════════════ */

export default function App() {
  // ─── State ──────────────────────────────────────────
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [thickness, setThickness] = useState("");
  const [results, setResults] = useState(null); // null = initial, [] = no results
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // ─── Search handler ─────────────────────────────────
  async function handleSearch(e) {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setResults(null);

    // Build request body — only include filters that have values
    const body = { query: query.trim() };
    if (category) body.category = category;
    if (maxPrice) body.max_price = parseFloat(maxPrice);
    if (thickness) body.thickness = thickness.trim();

    try {
      const res = await fetch(`${API_URL}/match`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (!res.ok) throw new Error(`Server returned ${res.status}`);

      const data = await res.json();
      setResults(data.results || []);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  // ─── Clear filters ─────────────────────────────────
  function clearFilters() {
    setCategory("");
    setMaxPrice("");
    setThickness("");
  }

  const hasFilters = category || maxPrice || thickness;

  // ─── Render ─────────────────────────────────────────
  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      {/* ── Header ──────────────────────────────────── */}
      <header className="relative bg-gradient-to-r from-indigo-700 via-indigo-600 to-violet-600 overflow-hidden">
        {/* Background decorations */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-20 -right-20 w-80 h-80 bg-white/5 rounded-full blur-3xl" />
          <div className="absolute -bottom-32 -left-20 w-96 h-96 bg-indigo-400/10 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 py-10 sm:py-16 text-center">
          {/* Logo / Brand */}
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm px-4 py-1.5 rounded-full text-indigo-100 text-sm font-medium mb-5">
            <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
            B2B Glass Marketplace
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight mb-3">
            Amal<span className="text-indigo-200">Gus</span>
          </h1>
          <p className="text-indigo-200 text-base sm:text-lg max-w-xl mx-auto">
            Smart Product Discovery — find the perfect glass & allied products
            using natural language
          </p>
        </div>
      </header>

      {/* ── Search Section ──────────────────────────── */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 -mt-7 relative z-10">
        <form
          onSubmit={handleSearch}
          className="glass-panel rounded-2xl shadow-lg p-5 sm:p-6"
        >
          {/* Query input */}
          <div className="flex gap-3">
            <div className="relative flex-1">
              <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                id="search-input"
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. 6mm tempered glass for office partitions, clear, polished edges"
                className="w-full pl-12 pr-4 py-3.5 rounded-xl border border-slate-200 bg-white text-slate-800 placeholder:text-slate-400 text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent transition"
              />
            </div>
            <button
              id="search-button"
              type="submit"
              disabled={loading || !query.trim()}
              className="px-5 sm:px-7 py-3.5 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white font-semibold rounded-xl text-sm sm:text-base transition-all duration-200 flex items-center gap-2 shadow-md shadow-indigo-200 hover:shadow-lg hover:shadow-indigo-300 active:scale-[0.97]"
            >
              {loading ? <SpinnerIcon className="w-5 h-5" /> : <SearchIcon className="w-5 h-5" />}
              <span className="hidden sm:inline">Find Best Matches</span>
            </button>
          </div>

          {/* Filters row */}
          <div className="mt-4 flex flex-wrap gap-3 items-end">
            {/* Category */}
            <div className="flex-1 min-w-[160px]">
              <label htmlFor="filter-category" className="block text-xs font-medium text-slate-500 mb-1">
                Category
              </label>
              <select
                id="filter-category"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3 py-2.5 rounded-lg border border-slate-200 bg-white text-sm text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-300 transition"
              >
                <option value="">All Categories</option>
                {CATEGORIES.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            {/* Max Price */}
            <div className="w-32">
              <label htmlFor="filter-price" className="block text-xs font-medium text-slate-500 mb-1">
                Max Price ($)
              </label>
              <input
                id="filter-price"
                type="number"
                min="0"
                step="0.01"
                value={maxPrice}
                onChange={(e) => setMaxPrice(e.target.value)}
                placeholder="e.g. 100"
                className="w-full px-3 py-2.5 rounded-lg border border-slate-200 bg-white text-sm text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-300 transition"
              />
            </div>

            {/* Thickness */}
            <div className="w-32">
              <label htmlFor="filter-thickness" className="block text-xs font-medium text-slate-500 mb-1">
                Thickness
              </label>
              <input
                id="filter-thickness"
                type="text"
                value={thickness}
                onChange={(e) => setThickness(e.target.value)}
                placeholder="e.g. 6mm"
                className="w-full px-3 py-2.5 rounded-lg border border-slate-200 bg-white text-sm text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-300 transition"
              />
            </div>

            {/* Clear filters */}
            {hasFilters && (
              <button
                type="button"
                onClick={clearFilters}
                className="text-xs text-indigo-500 hover:text-indigo-700 font-medium py-2.5 transition"
              >
                Clear filters
              </button>
            )}
          </div>
        </form>
      </section>

      {/* ── Results Section ─────────────────────────── */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 py-10">
        {/* Error */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-600 rounded-xl px-5 py-4 text-sm flex items-start gap-3">
            <span className="text-red-400 mt-0.5 text-lg">⚠</span>
            <div>
              <p className="font-semibold">Connection Error</p>
              <p className="mt-1 text-red-500">{error}</p>
              <p className="mt-1 text-red-400 text-xs">Make sure the backend is running on {API_URL}</p>
            </div>
          </div>
        )}

        {/* Loading skeletons */}
        {loading && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(3)].map((_, i) => (
              <SkeletonCard key={i} />
            ))}
          </div>
        )}

        {/* Results grid */}
        {!loading && results && results.length > 0 && (
          <>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-slate-700">
                Top Matches
                <span className="ml-2 text-sm font-normal text-slate-400">
                  ({results.length} result{results.length !== 1 ? "s" : ""})
                </span>
              </h2>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {results.map((product, i) => (
                <ProductCard key={i} product={product} index={i} />
              ))}
            </div>
          </>
        )}

        {/* No results */}
        {!loading && results && results.length === 0 && (
          <div className="text-center py-16">
            <EmptyIcon className="w-20 h-20 mx-auto text-slate-300 mb-4" />
            <h3 className="text-lg font-semibold text-slate-500 mb-1">No matching products found</h3>
            <p className="text-sm text-slate-400 max-w-md mx-auto">
              Try broadening your search or removing some filters to see more results.
            </p>
          </div>
        )}

        {/* Initial state (before any search) */}
        {!loading && results === null && !error && (
          <div className="text-center py-20">
            <div className="animate-float inline-block mb-5">
              <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-indigo-100 to-violet-100 flex items-center justify-center mx-auto shadow-sm">
                <SearchIcon className="w-9 h-9 text-indigo-400" />
              </div>
            </div>
            <h3 className="text-xl font-semibold text-slate-600 mb-2">Discover Products</h3>
            <p className="text-sm text-slate-400 max-w-md mx-auto leading-relaxed">
              Describe what you're looking for in plain English — our AI-powered
              semantic search will find the best matches from our catalog.
            </p>
            <div className="mt-6 flex flex-wrap justify-center gap-2">
              {[
                "6mm clear glass for partitions",
                "energy efficient facade glass",
                "fire rated safety glass",
                "aluminium curtain wall profile",
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  onClick={() => setQuery(suggestion)}
                  className="text-xs bg-white border border-slate-200 text-slate-500 hover:text-indigo-600 hover:border-indigo-200 hover:bg-indigo-50 px-3 py-1.5 rounded-full transition-all duration-200"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}
      </section>

      {/* ── Footer ──────────────────────────────────── */}
      <footer className="border-t border-slate-200 bg-white/50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-400">
          <p>© 2026 AmalGus · Smart Product Discovery Prototype</p>
          <p>
            Powered by{" "}
            <span className="font-medium text-slate-500">Sentence Transformers</span>{" "}
            + <span className="font-medium text-slate-500">FastAPI</span>
          </p>
        </div>
      </footer>
    </div>
  );
}
