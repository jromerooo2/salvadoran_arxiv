import { publicationYearValue } from './articleItems.js'
import contentData from '../assets/content.json'

const itemModules = import.meta.glob('../../articles/items/*.json', {
  eager: true,
})

function validAffiliation(aff) {
  const a = (aff ?? '').trim()
  return Boolean(a && a.toUpperCase() !== 'N/A')
}

const subcategoryNameByCode = (() => {
  const map = {}
  for (const category of contentData) {
    const subs = Array.isArray(category.subcategories) ? category.subcategories : []
    for (const sub of subs) {
      const code = (sub.subcategories_code ?? '').trim()
      const name = (sub.subcategories_name ?? '').trim()
      if (code) map[code] = name || code
    }
  }
  return map
})()

function buildCategoryList(data) {
  const codes = []
  const seen = new Set()

  const raw = (data?.author_categories ?? '').toString()
  if (raw.trim()) {
    for (const piece of raw.split(',')) {
      const code = piece.trim()
      if (code && !seen.has(code)) {
        seen.add(code)
        codes.push(code)
      }
    }
  }

  if (Array.isArray(data?.publications)) {
    for (const pub of data.publications) {
      const code = (pub?.category ?? '').toString().trim()
      if (code && !seen.has(code)) {
        seen.add(code)
        codes.push(code)
      }
    }
  }

  return codes.map((code) => ({
    code,
    name: subcategoryNameByCode[code] ?? code,
  }))
}

/**
 * One entry per JSON bundle in articles/items: name, orcid, paperCount,
 * affiliation from newest paper that has a real affiliation, and the three
 * newest paper titles.
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

    const paperCount = Array.isArray(data.publications)
      ? data.publications.length
      : 0

    const categories = buildCategoryList(data)
    categories.sort((a, b) => a.code.localeCompare(b.code, undefined, { sensitivity: 'base' }))

    out.push({
      name: (data.author ?? '').trim(),
      orcid: (data.orcid ?? '').trim(),
      recentAffiliation: recentAffiliation || null,
      recentTitles,
      paperCount,
      categories,
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
