(() => {
  const allowed = /^(silver|azure|titanium|iris|arctic)-(light|dark)$/;
  const names = {
    azure: { dark: "Midnight", light: "Azure" },
    silver: { dark: "Graphite", light: "Silver" },
    titanium: { dark: "Carbon", light: "Titanium" },
    iris: { dark: "Nebula", light: "Iris" },
    arctic: { dark: "Deep Sea", light: "Arctic" }
  };
  let saved;
  try { saved = window.localStorage.getItem("portfolio-theme"); } catch { /* Storage is optional, including file://. */ }
  const requested = new URLSearchParams(window.location.search).get("theme");
  let theme = allowed.test(requested) ? requested : allowed.test(saved) ? saved : "azure-dark";

  function applyTheme() {
    document.documentElement.dataset.theme = theme;
    document.querySelector('meta[name="color-scheme"]').content = theme.endsWith("dark") ? "dark" : "light";
    document.querySelector('meta[name="theme-color"]').content = getComputedStyle(document.documentElement).getPropertyValue("--paper").trim();
  }
  applyTheme();

  document.addEventListener("DOMContentLoaded", () => {
    const bar = document.querySelector(".appearance-bar");
    const select = document.querySelector("#theme-select");
    const buttons = [...document.querySelectorAll(".mode-switch button")];

    function syncControls() {
      const [palette, mode] = theme.split("-");
      select.value = palette;
      [...select.options].forEach((option) => { option.textContent = names[option.value][mode]; });
      buttons.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.mode === mode)));
    }

    function chooseTheme(next) {
      if (!allowed.test(next)) return;
      theme = next;
      applyTheme();
      syncControls();
      try { window.localStorage.setItem("portfolio-theme", theme); } catch { /* Selection still works without storage. */ }
      try {
        const url = new URL(window.location.href);
        url.searchParams.set("theme", theme);
        window.history.replaceState(null, "", url);
      } catch { /* Some browsers restrict file:// history updates. */ }
    }

    syncControls();
    bar.hidden = window.self !== window.top;
    select.addEventListener("change", () => chooseTheme(`${select.value}-${theme.split("-")[1]}`));
    buttons.forEach((button) => button.addEventListener("click", () => chooseTheme(`${theme.split("-")[0]}-${button.dataset.mode}`)));
  });
})();
