from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]
data_blue_print = {'content', 'title'}

@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':

        data = request.json
        missing_data = data_blue_print.difference(set(data.keys()))

        if missing_data:
            return jsonify({'missing-item': key for key in missing_data}), 404

        title = ['title']
        content = data['content']
        _id = len(POSTS) + 1
        new_post  = {"id": _id, "title": title, "content": content}
        POSTS.append(new_post)

        return jsonify(new_post)
    return jsonify(POSTS)

@app.route('/api/posts/<int:_id>', methods=['DELETE', 'PUT'])
def update_db(_id):
    if request.method == 'DELETE':
        if _id <= len(POSTS):
            del POSTS[_id - 1]
            return jsonify({
        "message": f"Post with id {_id} has been deleted successfully."
    }), 200
        else:
            return jsonify({
                "message": f"Post with id {_id} not found"
            }), 404

    elif request.method == 'PUT':
        if _id <= len(POSTS):
            data = request.json


            for key, value in data.items():
                POSTS[_id - 1][key] = value

            keys = list(data.keys())
            message = ' and '.join([' '.join(keys[:-1]), keys[-1]]) if len(keys) > 1 else ' '.join(keys)

            return jsonify({
                "message": f" {message} for post with id {_id} has been updated successfully."
            }), 200

        else:
            return jsonify({
                "message": f"Post with id {_id} not found"
            }), 404




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
