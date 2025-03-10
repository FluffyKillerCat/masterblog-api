from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        data_req = {'content', 'title'}
        data = request.json
        missing_data = data_req.difference(set(data.keys()))

        if missing_data:
            return jsonify({'missing-item': key for key in missing_data}), 404

        title = ['title']
        content = data['content']
        _id = len(POSTS) + 1
        new_post  = {"id": _id, "title": title, "content": content}
        POSTS.append(new_post)

        return jsonify(new_post)
    return jsonify(POSTS)

@app.route('/api/posts/<int:_id>', methods=['DELETE'])
def delte_post(_id):
    if _id <= len(POSTS):
        del POSTS[_id - 1]
        return jsonify({
    "message": f"Post with id {_id} has been deleted successfully."
}), 200
    else:
        return jsonify({
            "message": f"Post with id {_id} not found"
        }), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
