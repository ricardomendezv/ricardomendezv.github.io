(() => {
  const select = document.querySelector("#language-select");
  const pages = { en: "./index.html", es: "./es.html" };
  select.value = document.documentElement.lang;
  select.addEventListener("change", () => {
    if (!Object.hasOwn(pages, select.value)) return;
    const next = new URL(pages[select.value], window.location.href);
    next.search = window.location.search;
    next.searchParams.set("theme", document.documentElement.dataset.theme);
    next.hash = window.location.hash;
    window.location.assign(next.href);
  });
  const gallery = document.querySelector('a[href="./themes.html"]');
  function updateGalleryLink() {
    const target = new URL(gallery.href);
    target.searchParams.set("lang", document.documentElement.lang);
    target.searchParams.set("theme", document.documentElement.dataset.theme);
    gallery.href = target.href;
  }
  updateGalleryLink();
  gallery.addEventListener("click", updateGalleryLink);
})();
