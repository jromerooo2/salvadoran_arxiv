const itemModules = import.meta.glob('../../articles/items/*.json', {
  eager: true,
})

/**
 * Flatten all ORCID publication bundles under articles/items into one list.
 * Each row: id, author, orcid, title, abstract, year, journal, doi
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
        title: pub.title ?? '',
        abstract: pub.abstract ?? '',
        year: pub.year ?? '',
        journal: pub.journal ?? '',
        doi: pub.doi ?? '',
      })
    }
  }
  return articles
}
