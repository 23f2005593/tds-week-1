---
marp: true
theme: vishal
paginate: true
html: true
size: 16:9
header: 'Product Docs — v1.0'
footer: '© 2025 Your Company'
# Enable KaTeX by running marp-cli with --katex when exporting
---

<!-- _class: lead -->
# Product Documentation Presentation
**Modern, version-controlled, multi-format**

**Contact:** <23f2005593@ds.study.iitm.ac.in>

> Built with Marp Markdown so you can maintain docs in Git and export to HTML/PDF/PPTX with one command.

---

## Why Marp for Product Docs?

- **Markdown-first** authoring → easy reviews, diffs, & PRs
- **One source → many outputs** (HTML, PDF, PPTX)
- **Custom themes** via CSS for consistent branding
- **Portable math/code** blocks for engineers & PMs
- **Automatable** in CI to ship docs alongside releases

---

<!--
backgroundImage: url('./bg.svg')
backgroundSize: cover
color: #eaf2ff
-->
# Architecture Overview

- Core Services: Auth, API Gateway, Data Pipeline
- Storage: OLTP (Postgres) + OLAP (Columnar)
- Messaging: Kafka for async workflows
- Observability: Traces, Metrics, Logs

_This slide uses a **background image** via Marp directives._

---

## Complexity Cheat Sheet (with Math)

Consider mergesort complexity:

$$
T(n) = 2T\left(\frac{n}{2}\right) + O(n)
$$

Master Theorem gives:

$$
T(n) = O(n \log n)
$$

Also remember amortized queue via two stacks:

$$
\text{amortized push/pop} = O(1)
$$

> Export with `--katex` to render equations.

---

## Config Snippet (YAML)

```yaml
# config/app.yml
service:
  name: product-svc
  replicas: 3
  rolloutStrategy: blue-green
observability:
  tracing: true
  metrics:
    exporter: otlp
    endpoint: https://telemetry.example.com
```

Notes:

- Values can be templatized per environment.
- Keep secrets out of the repo (use a vault).

---

## Code Sample (TypeScript SDK)

```ts
// src/sdk/client.ts
export async function createSession(token: string) {
  const res = await fetch("/v1/session", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
```

- Ship code examples inline with docs.
- Keep examples tested via doctest/CI where possible.

---

## Theming & Styling Controls

Use Marp **directives** per slide:

- `<!-- _class: lead -->` for the title slide
- `<!-- color: #eaf2ff -->` to override text color
- `<!-- backgroundImage: url('./bg.svg') -->` for imagery
- Global pagination via `paginate: true` in front matter

Custom theme: **theme-vishal.css** (see repo).

---

## Export Commands

HTML:

```bash
npx @marp-team/marp-cli slides.md --theme theme-vishal.css --html --katex -o slides.html
```

PDF:

```bash
npx @marp-team/marp-cli slides.md --theme theme-vishal.css --pdf --katex -o slides.pdf
```

PPTX:

```bash
npx @marp-team/marp-cli slides.md --theme theme-vishal.css --pptx --katex -o slides.pptx
```

Automate in CI to publish with every tag.

---

## Questions & Contact

Reach me at **23f2005593@ds.study.iitm.ac.in**

- Repo contains: `slides.md`, `theme-vishal.css`, `bg.svg`
- Add more slides as your product evolves.
- Version-control everything, including exported assets via releases.

Thanks!
