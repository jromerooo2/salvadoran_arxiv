<template>
  <div>
  <section class="relative flex flex-wrap lg:h-screen lg:items-center">
    <div class="w-full px-4 py-12 sm:px-6 sm:py-16 lg:w-1/2 lg:px-8 lg:py-24">
      <div class="mx-auto max-w-lg text-center">
        <h1 class="text-2xl font-bold sm:text-3xl">Contact us</h1>

        <p class="mt-4 text-gray-500">
          Reach out to request an interview or to ask about publishing or collaborating with the society.
        </p>
      </div>

      <form action="#" class="mx-auto mb-0 mt-8 max-w-md space-y-4">
        <div>
          <label for="email" class="sr-only">Email</label>

          <div class="relative">
            <input
              id="email"
              type="email"
              class="w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm"
              placeholder="Your email"
              required
            />

            <span class="absolute inset-y-0 end-0 grid place-content-center px-4">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="size-4 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
                />
              </svg>
            </span>
          </div>
        </div>
        <div>
            <label for="name" class="sr-only">Your name</label>
  
            <div class="relative">
              <input
                id="name"
                type="text"
                class="w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm"
                placeholder="Your name"
                required
              />
            </div>
          </div>
        <div class="flex items-center justify-center space-x-3">
          <div class=" bg-white">
            <label for="topic" class="sr-only">Subject area</label>
              <select id="topic" name="topic" class="w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm">
                <option value="Mathematics">Mathematics</option>
                <option value="Physics">Physics</option>
                <option value="Chemistry">Chemistry</option>
                <option value="other">Other</option>
              </select>
          </div>
          <div>
            <label for="paper-link" class="sr-only">Paper link</label>
  
            <div class="relative">
              <input
                id="paper-link"
                type="text"
                class="w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm"
                placeholder="Link to your paper (optional)"
              />
            </div>
          </div>
        </div>
        <div class=" bg-white">
            <label for="reason" class="sr-only">Reason</label>
              <select id="reason" name="reason" class="w-full rounded-lg border-gray-200 p-4 pe-12 text-sm shadow-sm">
                <option value="interview">Interview request</option>
                <option value="publish">Publication / collaboration</option>
                <option value="both">Both</option>
              </select>
        </div>
        <div class="flex items-center justify-center">

          <button
            type="submit"
            class="inline-block rounded-lg bg-blue-500 px-5 py-3 text-sm font-medium text-white"
          >
            Send
          </button>
        </div>
      </form>
    </div>

    <div class="relative h-64 w-full sm:h-96 lg:h-full lg:w-1/2">
      <img
        alt="Salvadoran Society of Sciences"
        src="/src/assets/logo1.png"
        class="absolute inset-0 h-full w-full object-cover"
      />
    </div>
  </section>
    </div>
  </template>
