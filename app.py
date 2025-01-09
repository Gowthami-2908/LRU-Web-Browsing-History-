from flask import Flask, request, jsonify
from collections import OrderedDict
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  

# LRU Cache Implementation
class RecentUrlsCache:
    def __init__(self, max_capacity: int):
        """Initialize the cache with a specified capacity."""
        self.max_capacity = max_capacity
        self.urls_cache = OrderedDict()  

    def retrieve_url(self, key: str) -> str:
        """Fetch a URL from the cache and mark it as recently accessed."""
        if key not in self.urls_cache:
            return None  # Return None if the URL is not in the cache
        # Move the accessed URL to the end to mark it as the most recently used
        self.urls_cache.move_to_end(key)
        return self.urls_cache[key]

    def store_url(self, key: str, value: str):
        """Store a URL in the cache, and evict the least recently used if necessary."""
        if key in self.urls_cache:
            # If the URL already exists, move it to the most recent position
            self.urls_cache.move_to_end(key)
        self.urls_cache[key] = value
        
        # Check if the cache exceeds the maximum capacity and remove the least recently used item
        if len(self.urls_cache) > self.max_capacity:
            self.urls_cache.popitem(last=False)

    def get_all_urls(self):
        """Return all URLs in the cache, ordered from most recently used to least used."""
        return list(self.urls_cache.items())

# Initialize the cache with a maximum capacity of 5 URLs
url_cache = RecentUrlsCache(5)

# Route to retrieve the entire history of URLs
@app.route('/history', methods=['GET'])
def get_browsing_history():
    """Return the list of URLs in the cache."""
    history = url_cache.get_all_urls()
    return jsonify(history)  # Return the list as JSON response

# Route to add a new URL to the browsing history
@app.route('/history', methods=['POST'])
def add_to_browsing_history():
    """Add a new URL to the cache."""
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400  # If URL is missing, return an error response
    
    url_cache.store_url(url, url)  # Store the URL in the cache
    return jsonify({"message": "URL successfully added to history!"}), 201

if __name__ == '__main__':
    # Start the Flask server on localhost:5000
    app.run(debug=True)
