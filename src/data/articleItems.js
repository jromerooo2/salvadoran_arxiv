const itemModules = import.meta.glob('../../articles/items/*.json', {
  eager: true,
})

export function publicationYearValue(year) {
  if (year === undefined || year === null || String(year).trim() === '') return 0
  const n = parseInt(String(year), 10)
  return Number.isFinite(n) ? n : 0
}

/**
 * Flatten all ORCID publication bundles under articles/items into one list.
 * Each row: id, author, orcid, affiliation, title, abstract, year, journal, doi
 * Newest first (higher year first; within a year, higher id first).
 */
export function getAllArticles() {
  const articles = []
  let id = 0
  for (const mod of Object.values(itemModules)) {
    const data = mod.default
    if (!data || !Array.isArray(data.publications)) continue
    const author = data.author ?? ''
    const orcid = data.orcid ?? ''
    for (const pub of data.publications) {
      articles.push({
        id: ++id,
        author,
        orcid,
        affiliation: pub.affiliation ?? '',
        title: pub.title ?? '',
        abstract: pub.abstract ?? '',
        year: pub.year ?? '',
        journal: pub.journal ?? '',
        doi: pub.doi ?? '',
      })
    }
  }
  articles.sort((a, b) => {
    const ya = publicationYearValue(a.year)
    const yb = publicationYearValue(b.year)
    if (ya !== yb) return yb - ya
    return (b.id ?? 0) - (a.id ?? 0)
  })
  return articles
}
