const express = require('express');
const axios = require('axios');

const app = express();
const port = 3000;

app.get('/api/check-link', async (req, res) => {
  const { url } = req.query;

  if (!url) {
    return res.status(400).json({ error: 'URL is required' });
  }

  try {
    // Make a request but do not follow redirects
    const response = await axios.get(url, {
      maxRedirects: 0,
      validateStatus: () => true, // Accept all status codes
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': new URL(url).origin
      }
    });

    if (response.status >= 200 && response.status < 300) {
      res.json({ status: 'Working', details: `Status: ${response.status}` });
    } else if (response.status >= 300 && response.status < 400) {
      res.json({ status: 'Redirecting', details: response.headers.location });
    } else {
      res.json({ status: 'Broken', details: `Status: ${response.status} (${response.statusText})` });
    }
  } catch (error) {
    res.json({ status: 'Broken', details: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});

