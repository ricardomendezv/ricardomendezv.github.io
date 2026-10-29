(() => {
  const picker = document.querySelector("#theme-picker");
  const preview = document.querySelector("#portfolio-preview");
  const title = document.querySelector("#preview-title");
  const openTheme = document.querySelector("#open-theme");
  const initial = new URLSearchParams(location.search).get("theme");
  const options = [...picker.querySelectorAll('input[name="theme"]')];
  const palette = document.querySelector("#gallery-theme-select");
  const modes = [...document.querySelectorAll("[data-gallery-mode]")];
  const language = document.querySelector("#gallery-language-select");
  language.value = new URLSearchParams(location.search).get("lang") === "es" ? "es" : "en";

  function selectTheme(input) {
    input.checked = true;
    const name = input.closest("label").querySelector(".theme-caption strong").textContent;
    const mode = input.value.endsWith("dark") ? "Dark" : "Light";
    const url = `./${language.value === "es" ? "es.html" : "index.html"}?theme=${input.value}`;
    title.textContent = `${name} / ${mode}`;
    preview.title = `Portafolio con tema ${name} ${mode === "Dark" ? "oscuro" : "claro"}`;
    preview.src = url;
    openTheme.href = url;
    palette.value = input.value.split("-")[0];
    [...palette.options].forEach((option) => {
      const radio = options.find((item) => item.value === `${option.value}-${mode.toLowerCase()}`);
      option.textContent = radio.closest("label").querySelector(".theme-caption strong").textContent;
    });
    modes.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.galleryMode === mode.toLowerCase())));
    // file:// can reject history updates; theme selection still works offline.
    try { history.replaceState(null, "", `?theme=${input.value}&lang=${language.value}`); } catch { /* Preview needs no storage. */ }
  }

  picker.addEventListener("change", (event) => {
    if (options.includes(event.target)) selectTheme(event.target);
  });
  const match = options.find((input) => input.value === initial) || options.find((input) => input.value === "azure-dark");
  selectTheme(match);
  language.addEventListener("change", () => selectTheme(picker.querySelector("input:checked")));
  palette.addEventListener("change", () => {
    const mode = picker.querySelector("input:checked").value.split("-")[1];
    selectTheme(options.find((input) => input.value === `${palette.value}-${mode}`));
  });
  modes.forEach((button) => button.addEventListener("click", () => selectTheme(options.find((input) => input.value === `${palette.value}-${button.dataset.galleryMode}`))));

  const viewportButtons = [...document.querySelectorAll("[data-width]")];
  const stage = document.querySelector(".preview-stage");
  viewportButtons.forEach((button) => button.addEventListener("click", () => {
    stage.dataset.width = button.dataset.width;
    viewportButtons.forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
  }));
})();
