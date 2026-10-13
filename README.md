# Link Checker

This is a Vue 3 application built with Vite that allows you to check for broken and redirected links within your HTML and JSON files.

## Prerequisites

- [Node.js](https://nodejs.org/) (v22.12.0 or higher recommended). You can use [nvm](https://github.com/nvm-sh/nvm) to manage Node.js versions.
  ```bash
  nvm install 22.12.0
  nvm use 22.12.0
  ```

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://dev.azure.com/fcim/_git/Link%20Checker
    cd "Link Checker"
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

