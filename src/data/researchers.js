import { publicationYearValue } from './articleItems.js'

const itemModules = import.meta.glob('../../articles/items/*.json', {
  eager: true,
})

function validAffiliation(aff) {
  const a = (aff ?? '').trim()
  return Boolean(a && a.toUpperCase() !== 'N/A')
}

/**
 * One entry per JSON bundle in articles/items: name, orcid, affiliation from
 * newest paper that has a real affiliation, and the three newest paper titles.
 */
export function getResearchers() {
  const out = []
  for (const mod of Object.values(itemModules)) {
    const data = mod.default
    if (!data || !Array.isArray(data.publications)) continue
    const pubs = [...data.publications].sort(
      (a, b) => publicationYearValue(b.year) - publicationYearValue(a.year),
    )

    let recentAffiliation = ''
    for (const p of pubs) {
      if (validAffiliation(p.affiliation)) {
        recentAffiliation = String(p.affiliation).trim()
        break
      }
    }

    const recentTitles = pubs
      .slice(0, 3)
      .map((p) => (p.title ?? '').trim())
      .filter(Boolean)

    out.push({
      name: (data.author ?? '').trim(),
      orcid: (data.orcid ?? '').trim(),
      recentAffiliation: recentAffiliation || null,
      recentTitles,
    })
  }
  out.sort((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: 'base' }))
  return out
}

export function orcidDisplayId(orcidUrl) {
  const s = String(orcidUrl ?? '')
  const m = s.match(/(\d{4}-\d{4}-\d{4}-\d{3}[0-9X])$/i)
  return m ? m[1] : s
}
