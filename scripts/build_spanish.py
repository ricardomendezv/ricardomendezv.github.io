"""Generate the static Spanish page; fail if new English copy lacks a translation."""
from html.parser import HTMLParser
from pathlib import Path
import re

TRANSLATIONS = {
    "Ricardo Mendez Vargas — Software & Data Engineer": "Ricardo Mendez Vargas — Ingeniero de Software y Datos",
    "Skip to content": "Ir al contenido",
    "Work": "Proyectos", "Expertise": "Especialidades", "Experience": "Experiencia", "About": "Sobre mí",
    "Let's talk": "Conversemos", "Appearance": "Apariencia", "Dark": "Oscuro", "Light": "Claro", "Theme": "Tema", "Language": "Idioma",
    "Software & Data Engineer · Chile": "Ingeniero de Software y Datos · Chile",
    "Complex problems.": "Problemas complejos.", "Working solutions.": "Soluciones que funcionan.",
    "I turn data, software, and applied AI into useful products. From understanding the problem to building, shipping, and keeping things running.": "Transformo datos, software e IA aplicada en productos útiles. Desde entender el problema hasta desarrollar, publicar y mantener la solución en funcionamiento.",
    "Explore my work": "Ver mis proyectos", "Download CV": "Descargar CV (inglés)",
    "Python, PySpark, Snowflake & a practical approach to AI.": "Python, PySpark, Snowflake y un enfoque práctico de la IA.",
    "Hello, I'm Ricardo": "Hola, soy Ricardo", "An engineer who connects": "Un ingeniero que conecta", "the details to the bigger picture.": "los detalles con la visión global.",
    "Currently": "Actualmente", "Software Engineer at Comscore": "Ingeniero de Software en Comscore",
    "Data engineering": "Ingeniería de datos", "Applied AI": "IA aplicada", "Product development": "Desarrollo de productos", "From concept to production": "De la idea a producción",
    "03 / Selected work": "03 / Proyectos destacados", "Built to be": "Hechos para", "used.": "usarse.",
    "Real products. Different challenges.": "Productos reales. Desafíos distintos.", "A hands-on role from idea to delivery.": "Participación directa, de la idea a la entrega.",
    "Android app · Interface captures": "App Android · Capturas de interfaz", "Touchpad": "Panel táctil", "Keyboard": "Teclado", "Mobile & Bluetooth": "Móvil y Bluetooth",
    "Your phone. A mouse.": "Tu teléfono. Un mouse.", "One less thing to carry.": "Una cosa menos que llevar.",
    "An Android app that turns a phone into a Bluetooth mouse and keyboard for compatible devices, without Wi-Fi or a desktop companion app.": "Una app Android que convierte el teléfono en mouse y teclado Bluetooth para dispositivos compatibles, sin Wi-Fi ni una aplicación adicional en el computador.",
    "Google Play, end to end.": "Google Play, de principio a fin.",
    "Managed the complete publication process: Play Console setup, store listing, testing, policy declarations, and releases.": "Gestioné todo el proceso de publicación: configuración de Play Console, ficha de la tienda, pruebas, declaraciones de políticas y lanzamientos.",
    "AI-assisted development": "Desarrollo asistido por IA", "My role & what shipped": "Mi participación y resultados",
    "I independently handled requirements, UX, implementation, debugging, device testing, tester feedback, and publication on Google Play.": "Me encargué de forma independiente de los requisitos, la experiencia de usuario, el desarrollo, la depuración, las pruebas en dispositivos, la incorporación de comentarios y la publicación en Google Play.",
    "The app includes touchpad gestures, clicks, scrolling, keyboard input, shortcuts, and a configurable mouse jiggler. I used AI-assisted development and rapid prototyping throughout the process.": "La app incluye gestos de panel táctil, clics, desplazamiento, entrada de teclado, atajos y movimiento automático del mouse configurable. Utilicé desarrollo asistido por IA y prototipado rápido durante todo el proceso.",
    "View on Google Play": "Ver en Google Play", "Automatic profiles": "Perfiles automáticos", "App launcher": "Lanzador de aplicaciones", "Mobile & desktop": "Móvil y escritorio",
    "Your PC.": "Tu PC.", "One tap away.": "A un toque de distancia.",
    "A shortcut deck that connects an Android phone or tablet to a Windows PC. App-aware controls, custom macros, a launcher, and OBS actions over the local network.": "Un panel de atajos que conecta un teléfono o tablet Android con un PC Windows. Controles según la aplicación activa, macros personalizadas, un lanzador y acciones de OBS a través de la red local.",
    "Managed the Android app's full Play Console workflow, from store assets and policy declarations to testing and release management.": "Gestioné el proceso completo de la app Android en Play Console: recursos de la ficha, declaraciones de políticas, pruebas y gestión de versiones.",
    "Product & engineering": "Producto e ingeniería",
    "The product combines a Flutter mobile app with a Windows companion built with Tauri, Rust, and Svelte. A shared protocol connects device discovery, pairing, live layouts, and actions.": "El producto combina una app móvil en Flutter con una aplicación Windows desarrollada con Tauri, Rust y Svelte. Un protocolo compartido conecta el descubrimiento de dispositivos, el emparejamiento, los paneles en tiempo real y las acciones.",
    "Automatic profiles follow the foreground PC app; a visual editor supports custom decks and multi-step macros. The Android app requires the Windows 11 x64 companion and both devices on the same local network.": "Los perfiles automáticos siguen la aplicación activa del PC. Un editor visual permite crear paneles y macros de varios pasos. La app Android requiere el complemento para Windows 11 x64 y ambos dispositivos en la misma red local.",
    "Android source": "Código de Android", "Windows companion screenshot": "Captura de la aplicación Windows", "Windows companion · Deck editor": "Aplicación Windows · Editor de paneles",
    "Manager · Web application": "Manager · Aplicación web", "Manager dashboard · Application interface": "Panel de Manager · Interfaz de la aplicación", "Web application": "Aplicación web",
    "Daily work, connected": "El trabajo diario, conectado", "to the business.": "con el negocio.",
    "The operational web application for agricultural companies and contractors in Chile. Worker records, activities, payments, clients, and suppliers in one workflow.": "La aplicación de gestión operativa para empresas y contratistas agrícolas de Chile. Trabajadores, actividades, pagos, clientes y proveedores en un mismo flujo de trabajo.",
    "Business automation": "Automatización de procesos",
    "My contribution covered requirements, system and data-model design, development with Python and Django, workflow implementation, and deployment.": "Mi participación abarcó el levantamiento de requisitos, el diseño del sistema y del modelo de datos, el desarrollo con Python y Django, la implementación de procesos y el despliegue.",
    "The platform connects daily work logs and client-specific rates with payment orders, deductions, advances, purchases, and operational reports.": "La plataforma vincula los registros diarios de trabajo y las tarifas por cliente con órdenes de pago, descuentos, anticipos, compras y reportes operativos.",
    "Learn about AgroERP Manager": "Conocer AgroERP Manager", "Website · Public landing page": "Website · Sitio público", "www.agroerp.cl · Live website capture": "www.agroerp.cl · Captura del sitio publicado", "Website design & development": "Diseño y desarrollo web",
    "The product's": "La primera impresión", "first impression.": "del producto.",
    "The public website for AgroERP, separate from the ERP application itself. A responsive landing page that introduces the product, explains its features, and guides visitors to a demo enquiry.": "El sitio público de AgroERP, independiente de la aplicación ERP. Una landing adaptable a distintos dispositivos que presenta el producto, explica sus funciones y orienta a los visitantes a solicitar una demostración.",
    "Website scope": "Alcance del sitio web",
    "A custom WordPress theme brings together product features, interface previews, pricing, frequently asked questions, and a contact flow.": "Un tema WordPress a medida reúne las funciones del producto, vistas de la interfaz, precios, preguntas frecuentes y un flujo de contacto.",
    "Editable content through WordPress keeps the public site manageable independently of the Django ERP platform.": "El contenido editable desde WordPress permite administrar el sitio público de forma independiente de la plataforma ERP en Django.",
    "Visit www.agroerp.cl": "Visitar www.agroerp.cl", "Other engineering work / Reverse engineering": "Otros trabajos / Ingeniería inversa", "Understanding undocumented systems.": "Entender sistemas sin documentación.",
    "Legacy military electronics — FAMAE": "Electrónica militar legada — FAMAE",
    "I reverse-engineered military electronic hardware to reconstruct undocumented circuit functions, interfaces, and signal paths. The work combined schematic analysis, measurements, and functional testing with fault diagnosis, recovered documentation, test fixtures, and alternatives for obsolete components.": "Realicé ingeniería inversa de hardware electrónico militar para reconstruir funciones de circuitos, interfaces y recorridos de señales sin documentación. El trabajo combinó análisis de esquemas, mediciones y pruebas funcionales con diagnóstico de fallas, recuperación de documentación, bancos de prueba y alternativas para componentes obsoletos.",
    "Legacy software — Comscore": "Software legado — Comscore",
    "I reconstructed business logic, data flows, and dependencies in undocumented software to support troubleshooting, modernization, and integration with new services.": "Reconstruí la lógica de negocio, los flujos de datos y las dependencias de software sin documentación para facilitar el diagnóstico, la modernización y la integración con nuevos servicios.",
    "Beyond the product launch": "Más allá del lanzamiento", "Built to ship.": "Listo para entregar.", "Engineered to run.": "Diseñado para operar.",
    "At Comscore, I work on production data platforms for digital audience measurement: collecting, processing, and making data useful at scale.": "En Comscore trabajo en plataformas de datos en producción para medir audiencias digitales: recopilar, procesar y convertir datos en información útil a escala.",
    "More about my experience": "Más sobre mi experiencia", "Distributed data": "Datos distribuidos",
    "Web data collection, international SERP extraction, and PySpark / Hadoop processing with Snowflake and Snowpark.": "Recolección de datos web, extracción internacional de resultados de búsqueda y procesamiento con PySpark y Hadoop, junto con Snowflake y Snowpark.",
    "Useful intelligence": "Inteligencia útil",
    "AI-powered capabilities, agent workflows, and Streamlit tools for self-service exploration and reporting.": "Funciones basadas en IA, flujos con agentes y herramientas en Streamlit para explorar datos y generar reportes de forma autónoma.",
    "Production delivery": "Operación en producción",
    "Legacy software investigation, containerized services, and repeatable deployments with Docker, Swarm, Portainer, and CI/CD.": "Análisis de software legado, servicios en contenedores y despliegues repetibles con Docker, Swarm, Portainer y CI/CD.",
    "02 / How I can help": "02 / Cómo puedo aportar", "The right tool.": "La herramienta adecuada.", "A useful outcome.": "Un resultado útil.", "I connect engineering decisions": "Conecto las decisiones de ingeniería", "to what the business actually needs.": "con lo que el negocio realmente necesita.",
    "& analytics": " y analítica",
    "Build and improve data collection, ETL pipelines, distributed processing, and internal analytics tools.": "Desarrollo y mejoro la recolección de datos, los procesos ETL, el procesamiento distribuido y las herramientas internas de análisis.",
    "& automation": " y automatización",
    "Integrate language models and agents into existing workflows, with attention to validation, deployment, and local versus cloud trade-offs.": "Integro modelos de lenguaje y agentes en procesos existentes, considerando la validación, el despliegue y las diferencias entre ejecución local y en la nube.",
    "AI agents / LLM integration / Ollama / LM Studio / AWS": "Agentes de IA / Integración de LLM / Ollama / LM Studio / AWS", "& integration": " e integración",
    "Turn business requirements into working applications. Connect systems and reconstruct undocumented software behavior.": "Transformo requisitos de negocio en aplicaciones funcionales. Conecto sistemas y reconstruyo el comportamiento de software sin documentación.",
    "Django / APIs / Docker / CI/CD / Reverse engineering": "Django / APIs / Docker / CI/CD / Ingeniería inversa",
    "01 / Experience": "01 / Experiencia", "A career in": "Una trayectoria", "making it work.": "resolviendo desafíos.",
    "From electronics and IoT to software, data platforms, and applied AI.": "Desde la electrónica y el IoT hasta el software, las plataformas de datos y la IA aplicada.",
    "Get the full CV": "Ver CV completo (inglés)", "Dec 2022": "Dic 2022", "— Present": "— Actualidad", "Current": "Actual", "Software Engineer": "Ingeniero de Software", "· Remote": "· Remoto",
    "Data collection and analytics pipelines, distributed processing, internal tools, AI workflows, and production operations.": "Recolección y análisis de datos, procesamiento distribuido, herramientas internas, flujos con IA y operación de sistemas en producción.",
    "Jan 2026": "Ene 2026", "Independent Product Developer": "Desarrollador de Productos Independiente", "Self-employed": "Independiente",
    "KiMouse and KiBoard: mobile and desktop products, UX design, AI-assisted engineering, testing, complete Google Play publication management, and release iterations.": "KiMouse y KiBoard: productos móviles y de escritorio, diseño de experiencia de usuario, desarrollo asistido por IA, pruebas, gestión completa de publicación en Google Play y mejora continua de versiones.",
    "IT & IoT Project Developer": "Desarrollador de Proyectos TI e IoT",
    "Agricultural ERP development with Python and Django, reporting tools, Google Cloud deployments, IoT architecture, and firmware.": "Desarrollo de ERP agrícola con Python y Django, herramientas de reportes, despliegues en Google Cloud, arquitectura IoT y firmware.",
    "Electronics & Innovation": "Electrónica e Innovación",
    "Progressed from Electronics Engineer to Supervisor and Head of Electronics & Innovation. Led teams and the GPS equipment roadmap; developed device integrations, software, and firmware.": "Pasé de Ingeniero Electrónico a Supervisor y Jefe de Electrónica e Innovación. Lideré equipos y la planificación de equipos GPS; desarrollé integraciones de dispositivos, software y firmware.",
    "Earlier experience": "Experiencia anterior", "Electronics Project Specialist": "Especialista en Proyectos Electrónicos",
    "Reverse engineering of legacy military electronics, hardware diagnostics, recovered technical documentation, test fixtures, and repair validation tools.": "Ingeniería inversa de electrónica militar legada, diagnóstico de hardware, recuperación de documentación técnica, bancos de prueba y herramientas para validar reparaciones.",
    "Electronics Technician — CostaDigital": "Técnico Electrónico — CostaDigital", "04 / A little about me": "04 / Sobre mí", "A broader perspective.": "Una mirada más amplia.", "A hands-on mindset.": "Un enfoque práctico.",
    "My background connects software, data, and physical systems. I enjoy understanding how a business works, finding the technical bottleneck, and carrying a solution through implementation and operation.": "Mi trayectoria conecta software, datos y sistemas físicos. Me gusta entender cómo funciona un negocio, identificar los problemas técnicos y acompañar una solución desde su implementación hasta su operación.",
    "Based in Chile. Working in Spanish and English. Open to remote software and data engineering opportunities with international teams.": "Vivo en Chile y trabajo en español e inglés. Busco oportunidades remotas de ingeniería de software y datos con equipos internacionales.",
    "Academic education": "Formación académica", "Master's Degree in Innovation": "Magíster en Innovación", "Engineering in Automation & Robotics": "Ingeniería en Automatización y Robótica",
    "Electronics Technician": "Técnico en Electrónica", "Further education": "Formación complementaria", "Certifications": "Certificaciones",
    "Diploma in Design and Technology for Smart Cities": "Diplomado en Diseño y Tecnología para Smart Cities",
    "Diploma in Agile Business Development": "Diplomado en Desarrollo Ágil de Negocios",
    "Electrical & Electronic Maintenance of Armoured Weaponry": "Mantenimiento Eléctrico y Electrónico de Armamento Blindado",
    "Ejército de Tierra, Spain": "Ejército de Tierra, España",
    "Certificates II & IV in Renewable Energy": "Certificados II y IV en Energías Renovables",
    "Certiprof · May 2021": "Certiprof · mayo de 2021",
    "Have something in mind?": "¿Tienes algo en mente?", "Let's make": "Hagamos que", "it work.": "funcione.",
    "A data challenge, a product idea, or a team that could use another pair of hands. I'd like to hear about it.": "Un desafío con datos, una idea de producto o un equipo que necesite apoyo. Me gustaría conocer tu proyecto.",
    "Or find me on": "También puedes encontrarme en", "Explore color themes": "Explorar temas de color", "Back to top": "Volver al inicio",
}

TRANSLATIONS.update({
    "I build production data pipelines at Comscore and develop software from requirements to release. My work connects Python, SQL, distributed processing, and applied AI with practical business needs.": "Desarrollo pipelines de datos en producción en Comscore y software desde los requisitos hasta su publicación. Conecto Python, SQL, procesamiento distribuido e IA aplicada con necesidades concretas del negocio.",
    "Chile · Remote opportunities · Spanish & English": "Chile · Oportunidades remotas · Español e inglés",
    "View experience": "Ver experiencia",
    "Software & Data Engineer": "Ingeniero de Software y Datos",
    "10+ years across software, data, electronics, and technical project leadership.": "Más de 10 años de trayectoria en software, datos, electrónica y liderazgo de proyectos técnicos.",
    "Build ETL (Extract, Transform, Load) pipelines, web scraping and distributed data processing for analytics and reporting.": "Desarrollo pipelines ETL (extracción, transformación y carga), web scraping y procesamiento distribuido de datos para analítica y reportes.",
    "Integrate large language models (LLMs) and AI agents into workflows. Evaluate local and cloud models for generative AI applications and automation.": "Integro modelos de lenguaje de gran tamaño (LLM) y agentes de IA en flujos de trabajo. Evalúo modelos locales y en la nube para aplicaciones de IA generativa y automatización.",
    "LLM integration / AI agents / Ollama / LM Studio / Amazon Bedrock / Amazon Web Services (AWS)": "Integración de LLM / Agentes de IA / Ollama / LM Studio / Amazon Bedrock / Amazon Web Services (AWS)",
    "Build backend applications and APIs, design data models, and deploy containerized services with continuous integration and deployment (CI/CD).": "Desarrollo aplicaciones backend y APIs, diseño modelos de datos y despliego servicios en contenedores con integración y despliegue continuos (CI/CD).",
    "Django / Docker / Docker Swarm / Portainer / Google Cloud (GCP) / CI/CD / Reverse engineering": "Django / Docker / Docker Swarm / Portainer / Google Cloud (GCP) / CI/CD / Ingeniería inversa",
    "Develop and operate international web data collection and SERP extraction pipelines for digital audience measurement.": "Desarrollo y opero pipelines internacionales de recolección web y extracción de resultados de búsqueda (SERP) para medir audiencias digitales.",
    "Optimize Apache Spark / PySpark and Hadoop processing with Snowflake and Snowpark; build Streamlit tools for self-service analytics.": "Optimizo el procesamiento con Apache Spark / PySpark y Hadoop, junto con Snowflake y Snowpark; desarrollo herramientas Streamlit para analítica de autoservicio.",
    "Develop AI agent workflows, investigate legacy software, and deploy services with Docker, Docker Swarm, Portainer, and CI/CD.": "Desarrollo flujos con agentes de IA, analizo software legado y despliego servicios con Docker, Docker Swarm, Portainer y CI/CD.",
    "Delivered AgroERP with Python and Django, from requirements and data modeling to deployment on Google Cloud. Built reporting tools with Node-RED and JavaScript, alongside IoT architecture and firmware.": "Desarrollé AgroERP con Python y Django, desde los requisitos y el modelado de datos hasta su despliegue en Google Cloud. Creé herramientas de reportes con Node-RED y JavaScript, además de arquitectura IoT y firmware.",
})

ATTRIBUTES = {
    "Software & Data Engineer in Chile: Python, SQL, Apache Spark, Snowflake, Django, LLM integration and Docker. Comscore experience and published Android/Windows products.": "Ingeniero de Software y Datos en Chile: Python, SQL, Apache Spark, Snowflake, Django, integración de LLM y Docker. Experiencia en Comscore y productos publicados para Android/Windows.",
    "Software & Data Engineer: production data pipelines, applied AI, and published products. Based in Chile; working in Spanish and English.": "Ingeniero de Software y Datos: pipelines en producción, IA aplicada y productos publicados. En Chile; trabajo en español e inglés.",
    "Software and data engineer based in Chile. Explore KiMouse, KiBoard for Android and Windows, AgroERP Manager, AgroERP Website, and production engineering experience.": "Ingeniero de software y datos en Chile. Conoce KiMouse, KiBoard para Android y Windows, AgroERP Manager, AgroERP Website y mi experiencia en sistemas en producción.",
    "Data systems, practical AI, and software from idea to production. Selected work and experience.": "Sistemas de datos, IA práctica y software desde la idea hasta producción. Proyectos y experiencia profesional.",
    "Ricardo Mendez Vargas, home": "Ricardo Mendez Vargas, inicio", "Main navigation": "Navegación principal", "Meet Ricardo": "Conoce a Ricardo",
    "Open full KiMouse touchpad screenshot": "Abrir captura completa del panel táctil de KiMouse", "Open full KiMouse keyboard screenshot": "Abrir captura completa del teclado de KiMouse",
    "Actual KiMouse Android touchpad interface, with connection status and left and right mouse buttons": "Interfaz de KiMouse para Android con panel táctil, estado de conexión y botones izquierdo y derecho del mouse",
    "Actual KiMouse keyboard interface with modifier keys and the Android on-screen keyboard": "Interfaz de teclado de KiMouse con teclas modificadoras y teclado en pantalla de Android",
    "KiMouse technologies": "Tecnologías de KiMouse", "KiBoard technologies": "Tecnologías de KiBoard", "KiBoard downloads": "Descargas de KiBoard",
    "Open full KiBoard automatic profile screenshot": "Abrir captura completa del perfil automático de KiBoard", "Open full KiBoard launcher screenshot": "Abrir captura completa del lanzador de KiBoard",
    "KiBoard Android interface showing an automatic shortcut profile for ChatGPT and Codex": "Interfaz de KiBoard para Android con un perfil automático de atajos para ChatGPT y Codex",
    "KiBoard Android launcher interface showing application buttons including Chrome, Spotify, Terminal and Paint": "Lanzador de KiBoard para Android con botones de aplicaciones como Chrome, Spotify, Terminal y Paint",
    "Open full KiBoard Windows editor screenshot": "Abrir captura completa del editor de KiBoard para Windows", "KiBoard Windows companion with deck editor, button library and action configuration": "Aplicación KiBoard para Windows con editor de paneles, biblioteca de botones y configuración de acciones",
    "Open full AgroERP Manager screenshot": "Abrir captura completa de AgroERP Manager", "AgroERP Manager application dashboard with daily work, worker, client and payment administration modules": "Panel de AgroERP Manager con módulos de trabajos diarios, trabajadores, clientes y administración de pagos",
    "AgroERP technologies": "Tecnologías de AgroERP", "AgroERP website technologies": "Tecnologías del sitio web de AgroERP", "Open full AgroERP Website screenshot": "Abrir captura completa de AgroERP Website",
    "Actual agroerp.cl website showing its agricultural software headline, product preview and request-a-demo button": "Sitio agroerp.cl con su presentación de software agrícola, vista del producto y botón para solicitar una demostración",
}

UNCHANGED = {
    "Python · SQL · Apache Spark / PySpark · Snowflake · Django · Docker",
    "Python / SQL / Apache Spark (PySpark) / Hadoop / Snowflake / Snowpark / Streamlit",
    "rm", "Ricardo Mendez Vargas", "English", "Español", "Midnight", "Graphite", "Carbon", "Nebula", "Deep Sea",
    "KiMouse", "KiBoard", "Android", "Bluetooth HID", "Flutter / Dart", "Tauri / Rust", "Svelte", "Google Play", "Microsoft Store",
    "AgroERP Manager", "AgroERP Website", "Python", "Django", "WordPress", "PHP", "HTML / CSS / JavaScript", "Software",
    "Python / SQL / PySpark / Snowflake / Streamlit", "Comscore, Inc.", "May 2017", "Nov 2022", "INTELIX Chile", "Jun 2011",
    "Redd System / Tastets System", "Jul 2009 — Jun 2011", "FAMAE", "Mar 2006 — Jun 2008", "Pontificia Universidad Católica de Valparaíso",
    "Pontificia Universidad Católica de Chile", "Universidad Andrés Bello", "ricardo.mendez@gmail.com", "GitHub", "LinkedIn", "Upwork", "Freelancer", "© 2026 Ricardo Mendez Vargas",
    "Universidad Técnica Federico Santa María (UTFSM)", "Pontificia Universidad Católica de Chile · 2017", "Universidad del Desarrollo · 2020–2021",
    "Southbank Institute of Technology, Australia · 2008–2009", "Scrum Product Owner Professional Certificate", "Facilitating Productive Thinking", "ThinkX · Creative Thinking",
}


class Spanish(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output = []
        self.missing = set()

    def handle_starttag(self, tag, attrs):
        text = self.get_starttag_text()
        for key, value in attrs:
            if key in ("alt", "aria-label") or tag in ("meta", "title") and key == "content":
                translated = ATTRIBUTES.get(value, TRANSLATIONS.get(value))
                if translated:
                    text = text.replace(f'{key}="{value}"', f'{key}="{translated}"')
                elif key in ("alt", "aria-label") and value not in UNCHANGED:
                    self.missing.add(value)
        if tag == "html":
            text = text.replace('lang="en"', 'lang="es"')
        if tag == "link" and dict(attrs).get("rel") == "canonical" or tag == "meta" and dict(attrs).get("property") == "og:url":
            text = text.replace('https://ricardomendezv.github.io/"', 'https://ricardomendezv.github.io/es.html"')
        if tag == "option" and dict(attrs).get("value") in ("en", "es"):
            text = re.sub(r"\sselected(?:=\"[^\"]*\")?", "", text)
            if dict(attrs)["value"] == "es":
                text = text[:-1] + " selected>"
        self.output.append(text)

    def handle_endtag(self, tag):
        self.output.append(f"</{tag}>")

    def handle_data(self, data):
        text = data.strip()
        if text in TRANSLATIONS:
            data = data.replace(text, TRANSLATIONS[text], 1)
        elif any(c.isalpha() for c in text) and text not in UNCHANGED:
            self.missing.add(text)
        self.output.append(data)

    def handle_entityref(self, name):
        self.output.append(f"&{name};")

    def handle_charref(self, name):
        self.output.append(f"&#{name};")

    def handle_decl(self, decl):
        self.output.append(f"<!{decl}>")

    def handle_comment(self, data):
        self.output.append(f"<!--{data}-->")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1] / "docs"
    page = Spanish()
    page.feed((root / "index.html").read_text(encoding="utf-8"))
    assert not page.missing, f"Untranslated copy: {sorted(page.missing)}"
    (root / "es.html").write_text("".join(page.output), encoding="utf-8")
    print("PASS: Spanish page generated; all text and accessibility labels accounted for.")
