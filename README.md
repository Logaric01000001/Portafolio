# Logaric — portfolio

A bilingual, responsive portfolio for Linux tools, software projects and security learning. Built with static HTML and CSS; no build step, external fonts, analytics or runtime dependencies.

## Preview

```bash
python -m http.server 8080 --directory docs --bind 127.0.0.1
```

Open `http://127.0.0.1:8080` for English, or `/es/` for Spanish. This command only serves the static portfolio; it does not run the archived utility script.

## GitHub Pages

In repository Settings → Pages, select **Deploy from a branch**, then **main /docs**. A public deployment URL must be verified after Pages finishes; the repository alone does not establish that hosting is live.

## Content

- `docs/index.html`: English portfolio.
- `docs/es/index.html`: Spanish portfolio.
- `docs/style.css`: responsive layout, visible keyboard focus and reduced-motion support.
- `docs/assets/`: brand banner, SVG favicon and an existing screenshot from Antena.
- `Proyectos/Update/update.py`: original Arch maintenance script, preserved unchanged. It can change mirrors, upgrade packages and remove orphans/cache; inspect it before use. It is not invoked by the website.

Project claims link to public source. Antena's hardware limitations and EM's prototype status are explicit. No private project or personal contact data is included.

The Antena screenshot comes from the public GPL-3.0-or-later project [antena-arch](https://github.com/Logaric01000001/antena-arch); see its license and documentation. The banner was created for the Logaric identity using an image generation tool. No production medical integration, client testimonial or performance benchmark is claimed.
