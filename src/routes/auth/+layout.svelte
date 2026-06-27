<script lang="ts">
  import "../layout.css";
  import Navbar from "$lib/components/landing/Navbar.svelte";
  import Footer from "$lib/components/landing/Footer.svelte";

  let { children } = $props();
</script>

<div class="stone-texture min-h-screen">
  <Navbar />
  <main>
    {@render children()}
  </main>
  <Footer />
</div>
