/**
 * Lowercase + strip combining marks so "neutrino" matches text with accents.
 */
export function normalizeSearchText(value) {
  return String(value ?? '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
}

/**
 * Split query into non-empty tokens (whitespace-separated).
 */
export function searchTokens(query) {
  return normalizeSearchText(query)
    .split(/\s+/)
    .filter(Boolean)
}

/**
 * Build a single haystack from article fields (for "all fields" search).
 */
export function articleHaystackAll(article) {
  const parts = [
    article.title,
    article.abstract,
    article.journal,
    article.year,
    article.doi,
    article.author,
    article.orcid,
  ]
  return normalizeSearchText(parts.join(' '))
}

/**
 * @param {object} article
 * @param {string} query raw user query
 * @param {string} searchField key on article or 'all'
 */
export function articleMatchesQuery(article, query, searchField) {
  const tokens = searchTokens(query)
  if (tokens.length === 0) return true

  if (searchField === 'all') {
    const hay = articleHaystackAll(article)
    return tokens.every((t) => hay.includes(t))
  }

  const raw = article[searchField]
  const hay = normalizeSearchText(raw)
  return tokens.every((t) => hay.includes(t))
}
