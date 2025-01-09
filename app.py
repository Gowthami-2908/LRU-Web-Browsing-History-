from flask import Flask, request, jsonify
from collections import OrderedDict
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# LRU Cache Implementation
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: str) -> str:
        """Retrieve a value from the cache and mark it as recently used."""
        if key not in self.cache:
            return None
        # Move to the end to mark it as recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: str, value: str):
        """Add a new key-value pair to the cache and maintain the LRU order."""
        if key in self.cache:
            # Update the value and move it to the end (most recent)
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Pop the first (least recently used) item
            self.cache.popitem(last=False)

    def get_all(self):
        """Return all cache items in the order of most recently used to least recently used."""
        return list(self.cache.items())

# Initialize LRU cache with a capacity of 5 URLs
cache = LRUCache(5)

# Route to get all browsing history
@app.route('/history', methods=['GET'])
def get_history():
    # Get the full browsing history from the cache
    history = cache.get_all()
    return jsonify(history)

# Route to add a URL to the browsing history
@app.route('/history', methods=['POST'])
def add_history():
    # Get the URL from the incoming JSON request
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400  # If URL is missing, return error
    
    # Add the URL to the cache
    cache.put(url, url)
    return jsonify({"message": "URL added successfully!"}), 201

if __name__ == '__main__':
    # Run the Flask app on localhost:5000
    app.run(debug=True)
