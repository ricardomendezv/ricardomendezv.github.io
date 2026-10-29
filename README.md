# Ricardo Mendez Vargas — Portfolio

Portafolio estático en inglés y español: KiMouse, KiBoard, AgroERP Manager, AgroERP Website, experiencia en Comscore, trayectoria profesional, formación, contacto y CV. Inglés es el idioma predeterminado. HTML, CSS y JavaScript mínimo para los controles de apariencia e idioma, sin dependencias, compilación ni servicios externos de seguimiento. El contenido y los detalles siguen funcionando sin JavaScript, con Midnight oscuro como diseño inicial.

## GitHub Pages

- Portafolio: [ricardomendezv.github.io](https://ricardomendezv.github.io/).
- Versión en español: [ricardomendezv.github.io/es.html](https://ricardomendezv.github.io/es.html).
- Código: [ricardomendezv/ricardomendezv.github.io](https://github.com/ricardomendezv/ricardomendezv.github.io).

La publicación usa la rama `main` y la carpeta `/docs`. Los cambios enviados a esa rama actualizan el sitio automáticamente. Para revertir una actualización, revierte su commit y envía el resultado a `main`.

## Idiomas

`docs/index.html` es la entrada en **inglés** y `docs/es.html` la versión completa en **español**. El selector **Language / Idioma** está junto a los controles de apariencia. Conserva el tema activo, otros parámetros de la URL y la sección al cambiar de idioma. Cada página mantiene su idioma al recargar; no se detecta ni se guarda un idioma automáticamente, por lo que la entrada principal siempre abre en inglés.

La galería incorpora un selector **Idioma del portafolio** para previsualizar ambos idiomas con cualquiera de los diez temas. El enlace desde el portafolio conserva idioma y tema. El CV continúa en inglés y las capturas conservan los textos de sus productos; los botones de descarga en español indican el idioma del CV.

Ambas páginas están incluidas en la entrega y funcionan como archivos estáticos. Sin JavaScript, los enlaces English / Español del encabezado permiten cambiar de versión. Tienen etiquetas `lang`, metadatos y enlaces `hreflang` apropiados, así como descripciones de imágenes y nombres accesibles traducidos.

Para editar el contenido: modifica `docs/index.html`, actualiza las traducciones en `scripts/build_spanish.py` y regenera la página española:

```powershell
rtk proxy python scripts/build_spanish.py
```

El generador usa la biblioteca estándar de Python y falla si aparece texto nuevo sin traducción. No forma parte de la ejecución del sitio ni es necesario ejecutarlo para publicar los archivos ya entregados.

## Diez alternativas de color

Abre `docs/index.html`: el encabezado incluye botones **Dark / Light** y un selector **Theme** con cinco paletas. El modo cambia sin perder la familia de color; los nombres se adaptan al modo. La primera visita usa **Midnight Dark**. La elección se recuerda en el navegador si el almacenamiento está disponible. Sin JavaScript, Midnight sigue aplicado y los controles se ocultan.

Abre `docs/themes.html` para comparar las diez opciones en una galería. Sus controles de modo, paleta y tarjetas se mantienen sincronizados. Los botones de tamaño permiten comparar escritorio y móvil; «Abrir tema» abre el portafolio sin marco. Dentro del marco se ocultan los controles del encabezado para usar los de la galería.

| Claro | Oscuro | Identificador de paleta |
| --- | --- | --- |
| Silver | Graphite | `silver` |
| Azure | Midnight | `azure` |
| Titanium | Carbon | `titanium` |
| Iris | Nebula | `iris` |
| Arctic | Deep Sea | `arctic` |

Las URLs son compartibles, por ejemplo `index.html?theme=azure-dark` o `index.html?theme=silver-light`. La galería también conserva el tema en su URL. Prioridad del portafolio: tema válido de la URL → preferencia válida guardada en `localStorage` → Midnight Dark. No se escriben cookies ni se transmite esta preferencia. Las capturas conservan los colores de sus productos.

Midnight Dark ya está definido en `<html data-theme="azure-dark">`, en las metas de color y en el fallback de `theme.js`.

Verificación del 29 de octubre de 2026: las diez combinaciones aplicadas desde los controles del portafolio; modo, paleta, recarga, preferencia guardada y controles de galería comprobados. Portafolio revisado a 360 y 1280 px sin desbordamiento horizontal; capturas cargadas y detalle Windows operable. Los pares de texto y fondo definidos en las diez paletas superan 4,5:1 de contraste (mínimo calculado 4,53:1). Esto es una comprobación de paletas, no una auditoría completa de accesibilidad. Las metas se adaptan al tema activo.

## Formación y certificaciones

La formación académica destaca por igual el magíster en Innovación (PUC), la Ingeniería en Automatización y Robótica (UNAB) y el título de Técnico en Electrónica de la Universidad Técnica Federico Santa María (UTFSM). Debajo, con menor énfasis, aparecen Smart Cities, Desarrollo Ágil de Negocios, mantenimiento eléctrico/electrónico del Ejército de Tierra de España y energías renovables en Southbank, Australia.

El bloque de certificaciones incorpora Scrum Product Owner Professional Certificate (Certiprof, mayo de 2021) y Facilitating Productive Thinking (ThinkX · Creative Thinking). Los nombres se contrastaron con LinkedIn y la solicitud del titular; no se añadieron fechas ni enlaces de credenciales que no estuvieran disponibles. La sección se revisó en inglés y español, en escritorio y a 360 px.

## Capturas de los productos

KiMouse muestra touchpad y teclado; KiBoard muestra perfiles automáticos y launcher, con el editor de Windows dentro de un detalle desplegable. **AgroERP Manager** identifica la aplicación operativa y **AgroERP Website** su landing pública. Las capturas se pueden abrir a resolución original y conservan su proporción. Se sustituyeron las imágenes promocionales y el bloque de logotipo de las fichas por estas capturas. Procedencia y archivos originales: [ASSETS.md](ASSETS.md).

## Publicar en GitHub Pages

1. Crea un repositorio o usa uno existente. Sube **el contenido de esta carpeta**, conservando `docs/` en la raíz del repositorio.
2. En GitHub abre **Settings → Pages**.
3. Selecciona **Deploy from a branch**, la rama donde subiste los archivos (habitualmente `main`) y la carpeta **/docs**. Guarda.
4. Espera a que termine el despliegue y abre **Visit site** desde Pages.

Las rutas son relativas; funcionan tanto en `https://usuario.github.io/repositorio/` como en un repositorio personal `usuario.github.io`. `docs/.nojekyll` evita el procesamiento Jekyll. No se necesita un workflow propio.

Referencia: [crear un sitio con GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

## Vista local

Abre `docs/index.html` en un navegador. También puedes servir la carpeta con Python:

```powershell
rtk proxy python -m http.server 4173 --bind 127.0.0.1 --directory docs
```

Abre `http://127.0.0.1:4173`. Detén el servidor con Ctrl+C.

## Editar

- `docs/index.html`: contenido, proyectos, experiencia y enlaces.
- `docs/es.html`: versión española generada; `docs/language.js`: cambio de idioma.
- `docs/styles.css`: colores, tipografía, espaciado y adaptación a móvil.
- `docs/themes.css` y `docs/theme.js`: paletas y selección por URL.
- `docs/themes.html`, `docs/theme-gallery.css` y `docs/theme-gallery.js`: galería de comparación.
- `docs/assets/`: retrato, imágenes de proyectos, favicon y CV público.

Los detalles de proyectos y experiencia anterior usan `<details>` nativo: funcionan con teclado y sin JavaScript. No hay formulario; el contacto abre el email del visitante mediante `mailto:`.

El CV es una copia del documento aportado. Las imágenes proceden del portafolio y los recursos de los proyectos del titular. El contenido se basa en los perfiles revisados el 28 de octubre de 2026 y en la documentación de KiBoard y del sitio AgroERP; no se incorporaron notas privadas ni autoevaluaciones de plataformas. No se especifica el lenguaje/framework interno de KiMouse porque no estaba confirmado.

KiBoard incluye sus enlaces oficiales a [Google Play](https://play.google.com/store/apps/details?id=com.kiboard.kiboard_app) y [Microsoft Store](https://apps.microsoft.com/detail/9MTQZQJ9GDT4). El usuario confirmó que estas son las tiendas solicitadas. La plataforma AgroERP y su sitio público se presentan como dos proyectos relacionados, con enlace a [www.agroerp.cl](https://www.agroerp.cl/).

La sección de trabajo también resume ingeniería inversa de electrónica militar legada en FAMAE y de software sin documentación en Comscore. KiMouse y KiBoard indican la gestión completa de publicación en Google Play. El perfil personal de [GitHub](https://github.com/ricardomendezv) se confirmó mediante la cuenta conectada y está enlazado desde contacto.

Las nuevas descripciones y las dos menciones de publicación en Google Play se verificaron en el navegador; la sección de ingeniería inversa se adapta a una columna a 360 px y el sitio no presenta desbordamiento horizontal. Las propuestas de futuros proyectos se entregan en la investigación, no como trabajos terminados en la web.

No se añadió URL canónica ni imagen Open Graph absoluta porque la URL final aún no está definida. Se pueden completar al publicar. Revisa el email y el CV antes de compartir el sitio públicamente.

## Comprobación de archivos

```powershell
rtk proxy python tests/verify_site.py
rtk proxy node tests/verify_themes.cjs
rtk proxy node tests/verify_language.cjs
```

Comprueba referencias locales, anclas, recursos, enlaces de contacto, proyectos, estructura semántica y ausencia de archivos de investigación en el sitio. La revisión visual en navegador complementa esta comprobación.

La versión bilingüe se verificó el 29 de octubre de 2026: inglés por defecto; cambio EN/ES conservando tema claro/oscuro y ancla; ambas vistas en la galería; textos españoles y controles revisados a 360 y 1440 px sin desbordamiento horizontal. La comprobación estática verifica correspondencia de enlaces, recursos y anclas entre idiomas, además de la cobertura de traducción y de etiquetas accesibles.

Validación realizada el 28 de octubre de 2026: comprobación de archivos aprobada; revisión inicial a 360, 768 y 1440 px sin desbordamiento horizontal y nuevas fichas comprobadas en móvil y escritorio; imágenes cargadas; detalles nativos operables con ratón y teclado; nueve recursos servidos por HTTP idénticos a los archivos locales, incluido el CV. Las fichas de Google Play y Microsoft Store se comprobaron, y www.agroerp.cl abrió correctamente y redirigió a agroerp.cl. No se ejecutó una auditoría Lighthouse ni se publicó en una cuenta de GitHub.
