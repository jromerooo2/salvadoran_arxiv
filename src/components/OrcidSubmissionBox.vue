<template>
  <section
    class="mx-auto w-full rounded-xl bg-[#0047ab] px-5 py-8 text-center shadow-md sm:px-8"
  >
    <h2 class="mb-6 text-xl font-semibold leading-snug text-white sm:text-2xl">
      Not listed yet? Add your ORCID here
    </h2>

    <form
      class="mx-auto flex w-full max-w-4xl flex-col items-stretch gap-4"
      novalidate
      @submit.prevent="handleSubmit"
    >
      <div class="flex w-full flex-col gap-3 sm:flex-row sm:items-stretch">
        <input
          v-model.trim="orcid"
          type="text"
          name="orcid"
          autocomplete="off"
          inputmode="numeric"
          maxlength="19"
          placeholder="ORCID iD (e.g. 0000-0002-1825-0097)"
          aria-label="ORCID iD"
          :class="inputClass"
        />
        <input
          v-model.trim="email"
          type="email"
          name="email"
          autocomplete="email"
          placeholder="Email address"
          aria-label="Email address"
          :class="inputClass"
        />
      </div>

      <label
        class="mx-auto flex w-full max-w-3xl cursor-pointer items-center justify-center gap-3 text-center text-sm text-white sm:text-base"
      >
        <input
          v-model="confirmed"
          type="checkbox"
          name="confirmed"
          class="h-4 w-4 shrink-0 cursor-pointer rounded border-white/60 bg-white text-[#0047ab] accent-white focus:outline-none focus:ring-2 focus:ring-white/80"
        />
        <span class="leading-snug">
          I confirm that the provided ORCID belongs to a Salvadoran researcher.
        </span>
      </label>

      <div class="flex w-full flex-col items-center gap-3 sm:flex-row sm:justify-center">
        <button
          type="submit"
          :class="buttonClass"
          :disabled="submitting"
        >
          {{ submitting ? 'Submitting…' : 'Submit ORCID' }}
        </button>
      </div>

      <p
        v-if="message"
        :class="[
          'mx-auto max-w-3xl rounded-lg px-4 py-2.5 text-sm font-medium',
          messageType === 'error'
            ? 'border-2 border-white/60 bg-white/10 text-white'
            : 'border-2 border-white bg-white text-[#0047ab]',
        ]"
        role="status"
        aria-live="polite"
      >
        {{ message }}
      </p>
    </form>
  </section>
</template>

<script>
const ORCID_REGEX = /^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$/
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const FORMSPREE_ENDPOINT = 'https://formspree.io/f/xeedlegn'
const FORMSPREE_SUBJECT = 'A new ORCID was recieved from ssscience.org'

export default {
  name: 'OrcidSubmissionBox',
  data() {
    return {
      orcid: '',
      email: '',
      confirmed: false,
      submitting: false,
      message: '',
      messageType: 'info',
    }
  },
  computed: {
    inputClass() {
      return [
        'min-h-[44px] flex-1 rounded-lg border-2 px-4 py-2.5 shadow-inner placeholder:text-slate-400',
        'focus:outline-none focus:ring-2 sm:min-w-0',
        'border-white/40 bg-white text-[#0047ab] focus:border-white focus:ring-white/80',
      ].join(' ')
    },
    buttonClass() {
      return [
        'min-h-[44px] shrink-0 rounded-lg border-2 px-6 py-2.5 text-sm font-bold transition',
        'focus:outline-none focus:ring-2 sm:px-8',
        'border-white bg-white text-[#0047ab] hover:bg-white/90',
        'focus:ring-white focus:ring-offset-2 focus:ring-offset-[#0047ab]',
        'disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:bg-white',
      ].join(' ')
    },
  },
  methods: {
    setMessage(text, type = 'info') {
      this.message = text
      this.messageType = type
    },
    validate() {
      if (!ORCID_REGEX.test(this.orcid)) {
        this.setMessage(
          'Please enter a valid ORCID iD in the format 0000-0000-0000-0000.',
          'error',
        )
        return false
      }
      if (!EMAIL_REGEX.test(this.email)) {
        this.setMessage('Please enter a valid email address.', 'error')
        return false
      }
      if (!this.confirmed) {
        this.setMessage(
          'Please confirm that the ORCID belongs to a Salvadoran researcher.',
          'error',
        )
        return false
      }
      return true
    },
    async handleSubmit() {
      this.setMessage('', 'info')
      if (!this.validate()) return

      this.submitting = true
      try {
        const payload = {
          _subject: FORMSPREE_SUBJECT,
          _replyto: this.email,
          message: `${this.orcid}\n${this.email}`,
          orcid: this.orcid,
          email: this.email,
          confirmed_salvadoran_researcher: 'yes',
        }

        const response = await fetch(FORMSPREE_ENDPOINT, {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        })

        if (response.ok) {
          this.setMessage(
            'Thanks! Your ORCID submission has been received.',
            'success',
          )
          this.orcid = ''
          this.email = ''
          this.confirmed = false
          return
        }

        let detail = ''
        try {
          const data = await response.json()
          if (Array.isArray(data?.errors) && data.errors.length > 0) {
            detail = data.errors
              .map((e) => e?.message)
              .filter(Boolean)
              .join(' ')
          }
        } catch (_) {
          // ignore JSON parse failures and fall back to generic message
        }
        this.setMessage(
          detail ||
            'Sorry, your submission could not be sent. Please try again later.',
          'error',
        )
      } catch (_) {
        this.setMessage(
          'Network error. Please check your connection and try again.',
          'error',
        )
      } finally {
        this.submitting = false
      }
    },
  },
}
</script>
