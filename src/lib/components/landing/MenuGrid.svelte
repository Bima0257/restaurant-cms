<script lang="ts">
  import MenuCard from "./MenuCard.svelte";

  const menuItems = [
    {
      image: "https://lh3.googleusercontent.com/aida-public/AB6AXuANhSiWN8hPO8OtHS7WjyrYybUC5w4bdVyNVJU-U4ksceBI20D9HaWICkSEMGe4lEU35eHj1L7mq57IyXaltC5zP9mULH-V3nq2y3YxCgO7nUd5E9-DW4xuE7GXaBF62sG2JhrY4ZjEnYU3HxQb-qBAtMcDcwrjn5ESD-CV_0wnEEkAvtB7cXdlqj6MM8gG1UDBTK4sSmxWbkK3ggJkdXu1cSCjK6fv2303txnkP2JJDi6GxAyR_AieAJcekYez6r8_tVovgrTml-M",
      title: "Margherita Pizza",
      description: "Best Chicken and beef mix with tomato fresh from the farm.",
      price: "$19.00",
      rating: 4,
    },
    {
      image: "https://lh3.googleusercontent.com/aida-public/AB6AXuDb3pJdmvEnZxoKWvYkarI8zzhb83b26xrhVMxXEt5_Lx68SJpdGHX9GAQ_CYIWmh7uxWybAO_G3RfP1AvuyXLFJs0xL70ty1tGo4TWBPw8Qte2rS6cx6y7IgjD1Pyd4lVvcCsZ45ZTps9q9MliCxLSjIO-uljPkCQKZGCCHIbAae3poFk_m3y-nZa3yJVonmV9DdZR3WwFLqV4trZzRdYpOoyCOrDEKjnZ4jbNydwmjgftHVuUATWnpffnQmXwVRePyu1W3eWw8Rk",
      title: "Signature Burger",
      description: "Double patties, melted gouda, and our secret WorldPlate sauce.",
      price: "$24.00",
      rating: 5,
    },
    {
      image: "https://lh3.googleusercontent.com/aida-public/AB6AXuA8tjIxQN5CxrGB7X3_hOsJdtLDXD0yFoQ2usEGLgdB52T-LUP9f63ctkfyj0OzeRFizlJS4ybG6GAmHgvUeLRyVxVT6L3cc9LqTTj_TUNR7PIbqT672Se9C2-YEZ3cLJfbzANNn2Ac2p7jlnWmR-YJJDArXpWt8B0qMcxdGSbjOoctrKViOn_M4GLwwc1wAxFF4ZPJ4T7NuTFIFrKjMpmaQ-T97Zg0b2Pxc0iLxnLGQFX6ovZL-T01-fKufPN0uSeWZMuzLvzLWDM",
      title: "Salmon Sushi Set",
      description: "Fresh Atlantic salmon with premium wasabi and ginger.",
      price: "$32.00",
      rating: 4,
    },
  ];
</script>

<section class="px-gutter mb-section-gap">
  <div class="max-w-grid-max-width mx-auto">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      {#each menuItems as item}
        <MenuCard {...item} />
      {/each}
    </div>
  </div>
</section>
