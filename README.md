# Invoicely.AI — Frontend

A clean, production-grade landing page for the [Invoice Data Extraction System](https://github.com/Dannywinson1/Invoice-Data-Extraction-System).

## Files

```
frontend/
├── index.html   # Main page
├── style.css    # Full design system & styles
├── app.js       # Demo interactions & animations
└── README.md    # This file
```

## Features

- **Interactive demo** — simulates the full extraction pipeline with animated step indicators and live JSON output
- **Responsive** — works on mobile, tablet, and desktop
- **No dependencies** — pure HTML, CSS, and vanilla JS (Google Fonts only)
- **GitHub-linked** — all CTAs point to the live repo

## How to use

### Option 1: Drop it in your existing repo

Copy `index.html`, `style.css`, and `app.js` into a `/frontend` folder (or root) of your repo and push.

```bash
cp -r frontend/ /path/to/Invoice-Data-Extraction-System/frontend/
```

### Option 2: GitHub Pages (recommended)

1. Push these files to the root of a new branch called `gh-pages`  
   (or put them in `/docs` on `main`)
2. Go to your repo → **Settings → Pages**
3. Set source to `main` branch, `/docs` folder (or `gh-pages` branch)
4. Your site will be live at `https://dannywinson1.github.io/Invoice-Data-Extraction-System/`

### Option 3: Deploy to Vercel / Netlify (1-click)

- **Vercel**: Connect repo, set output directory to `frontend/`, deploy
- **Netlify**: Drag and drop the folder at [app.netlify.com/drop](https://app.netlify.com/drop)

## Customization

- Update the GitHub URL in `index.html` if you fork the repo
- Replace sample data in `app.js` (`SAMPLES` array) with real examples from your system
- Connect the upload zone to your real Python backend by replacing `runExtraction()` with a `fetch()` call to your API

## Built by

Danny Tang · Lead Software Engineer · [LinkedIn](https://www.linkedin.com/in/danny-tang1/)