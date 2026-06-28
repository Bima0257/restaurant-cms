<script lang="ts">
  import "../layout.css";
  import Navbar from "$lib/components/landing/Navbar.svelte";
  import Footer from "$lib/components/landing/Footer.svelte";

  let { children } = $props();
</script>

<div class="stone-texture min-h-screen">
  <Navbar />
  <main class="pb-24 md:pb-0">
    {@render children()}
  </main>
  <Footer />
</div>
