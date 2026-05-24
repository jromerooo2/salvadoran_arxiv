<template>
  <footer
    class="footer-salvador w-full border-t border-black/10 px-4 py-4 text-white sm:px-6 lg:px-8"
    role="contentinfo"
    aria-label="Site footer"
  >
    <div
      class="mx-auto flex w-full max-w-none flex-col items-center justify-between gap-2 text-sm sm:flex-row"
    >
      <p>© {{ copyrightRange }} Salvadoran Repository of Sciences</p>
      <a
        href="mailto:elsalvador.stem@gmail.com"
        class="text-white hover:underline focus:outline-none focus:ring-2 focus:ring-white/80 focus:ring-offset-2 focus:ring-offset-[#0047ab]"
      >
        elsalvador.stem@gmail.com
      </a>
    </div>
  </footer>
</template>

<script>
const FOUNDED_YEAR = 2024

export default {
  name: 'AppFooter',
  computed: {
    copyrightRange() {
      const current = new Date().getFullYear()
      return current > FOUNDED_YEAR
        ? `${FOUNDED_YEAR}–${current}`
        : `${FOUNDED_YEAR}`
    },
  },
}
</script>

<style scoped>
.footer-salvador {
  background-color: #0047ab;
}
</style>
