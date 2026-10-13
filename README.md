# Link Checker

A web application for finding **broken** and **redirected** links inside your course's HTML and JSON files. Point it at a folder (or a handful of files), and it scans every link, reports which ones are dead or redirecting, and lets you export the results to CSV.

It is a browser-based re-imagining of the original Python `Broken-Link-Checker` script: instead of running a command-line tool, you get an interactive UI with live progress, filterable results, and one-click CSV export.

## What It Does

- **Scans `.html` and `.json` files** for links.
  - In HTML files it reads every `<a>` tag and collects the `href` (only `http://` / `https://` links) plus the anchor text.
  - In JSON files it looks for a `links` array and reads each entry's `url`. If no `links` array is present (or the JSON can't be parsed), it falls back to a regex that pulls any `http(s)` URL out of the raw content.
- **Deduplicates links** and tracks, for each unique URL, which file(s) it came from and what link text(s) it was used with.
- **Checks every link** over the network and classifies it:
  - **OK** — the link resolves (HTTP 2xx).
  - **Broken** — the link fails (HTTP 4xx/5xx, DNS error, timeout, etc.). The specific error is shown in the *Details* column.
  - **Redirecting** — the link returns a 3xx and points somewhere else. The destination is shown (and clickable) in the *Details* column.
  - **Redirecting secure** — a special case of a redirect where an `http://` link simply upgrades to the identical `https://` URL. These are usually harmless and are called out separately so you can ignore them.
- **Reference-directory matching (optional).** When you select a single JSON file, you can also point the app at a directory of HTML files. It matches each link's ID in the JSON against `data-linkapi-id` attributes in those HTML files to work out which links are actually used on the pages, where they appear, and their surrounding text. Links in the JSON that aren't referenced anywhere are flagged as **Not Used!**.
- **Reports and exports.** Results are shown in a sortable, filterable table with **Broken / Redirects / All** tabs and a live statistics panel (total, checked, broken, redirects). You can hide/show columns and download the current tab as a CSV file.

## How to Use It

1. **Select your sources.** Click **Directory** to pick a whole folder, or **Files** to pick individual files. Only `.html` and `.json` files are scanned.
2. **(Optional) Select a reference directory.** If you selected a single JSON file, a second step appears. Pick the directory of HTML files that use those links so the app can match link IDs to their on-page context.
3. **(Optional) Enter a site name.** This is only used to name the exported CSV file.
4. **Start the link check.** The app checks each link in turn and updates the progress bar.
5. **Review the results.** Use the **Broken**, **Redirects**, and **All** tabs to filter, click any column header to sort, and use **Show Column Controls** to toggle columns.
6. **Export.** Click **CSV** to download the currently selected tab. The file is named `<site-name>-<category>-<date>.csv` (e.g. `my-site-broken_links-2026-10-13.csv`).

> **Tip:** For redirects, click the destination URL in the *Details* column to open it. If a "redirected" link lands on something unrelated or suspicious, treat the original URL as a problem link and include it in your broken-link report.

## Technologies

| Layer | Technology | Purpose |
| --- | --- | --- |
| UI framework | [Vue 3](https://vuejs.org/) (Composition API, `<script setup>`) | Reactive single-page interface |
| Build tool / dev server | [Vite](https://vite.dev/) | Fast dev server and production bundling; proxies `/api` to the local server |
| Link-check server | [Express](https://expressjs.com/) | Small local Node server that performs the actual HTTP requests |
| HTTP client (server) | [Axios](https://axios-http.com/) | Makes the request for each link without following redirects |
| Styling | [Sass](https://sass-lang.com/) (SCSS, BEM naming) | Component styles |
| Process runner | [concurrently](https://www.npmjs.com/package/concurrently) | Runs the Express server and Vite dev server together |
| Documentation | [JSDoc](https://jsdoc.app/) | Generates HTML docs from the source comments |
| Runtime | [Node.js](https://nodejs.org/) | v22.12.0 or higher recommended |

**Why a local server?** Browsers block most cross-origin requests (CORS), so the app can't check arbitrary URLs directly from the page. The Express server runs locally and performs each request with `maxRedirects: 0`, which is what lets it detect redirects without following them. Vite's dev server proxies `/api/*` to that server on port `3000`.

## Prerequisites

- [Node.js](https://nodejs.org/) (v22.12.0 or higher recommended). You can use [nvm](https://github.com/nvm-sh/nvm) to manage Node.js versions.
  ```bash
  nvm install 22.12.0
  nvm use 22.12.0
  ```

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd "Broken-Link-Checker"
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

## Usage

### Running the Development Server

To run the application in development mode, which includes a local server to handle link checking requests:

```bash
npm start
```

This will start the Vite development server and a Node.js Express server concurrently. You can access the application at the URL provided by Vite (usually `http://localhost:5173`).

### Building for Production

To build the application for production:

```bash
npm run build
```

This will create a `dist` directory with the production-ready files. You can then serve the contents of the `dist` directory with a static file server.

### Previewing the Production Build

To preview the production build locally:

```bash
npm run preview
```

### Generating Documentation

To generate html pages that document all functions:
```bash
./node_modules/.bin/jsdoc src/js/LinkChecker.js
```
- This will create a folder named `out` and you can run the html pages on the browser for a quick overview.
- Documentation can also be found inline in `src/js/LinkChecker.js`

## Project Structure

```
├── index.html              # App entry point
├── server.cjs              # Express server that checks links (/api/check-link)
├── vite.config.js          # Vite config (Vue plugin + /api proxy)
├── package.json
└── src/
    ├── main.js             # Vue app bootstrap
    ├── App.vue             # Root component
    ├── style.css           # Global styles
    ├── components/
    │   └── LinkChecker.vue # Main UI (source selection, stats, results table)
    ├── js/
    │   └── LinkChecker.js  # useLinkChecker() composable: scanning, checking, CSV export
    └── scss/               # SCSS partials (BEM) for each UI section
```

## Additional Links

- [Broken-Link-Checker (original Python project)](https://github.com/JoseBrouwer/Broken-Link-Checker)
- [Issues](https://github.com/JoseBrouwer/Broken-Link-Checker/issues)
- [Pull requests](https://github.com/JoseBrouwer/Broken-Link-Checker/pulls)

