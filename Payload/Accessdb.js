const url = 'https://example.com/database'; // Manually entered URL
const payload = {
  method: 'GET',
  url: url,
  headers: {
    'Content-Type': 'application/json'
  }
};

// Make a request to the database URL
fetch(url, payload)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
