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
def handle_posts():
    if request.method == 'POST':
        data = request.json
        missing_data = data_blue_print.difference(data.keys())

        if missing_data:
            return jsonify({'missing-items': list(missing_data)}), 404

        title = data['title']
        content = data['content']
        if POSTS:
            max_post = max(POSTS, key=lambda x: x['id'])
            _id = max_post['id'] + 1
        else:
            _id = 1
        new_post = {"id": _id, "title": title, "content": content}
        POSTS.append(new_post)

        return jsonify(new_post), 201

    if request.method == 'GET':
        sort_type = request.args.get('sort')
        sort_direction = request.args.get('direction')

        if not sort_type or not sort_direction:
            return jsonify(POSTS), 200

        if sort_type not in data_blue_print or sort_direction not in ['asc', 'desc']:
            return jsonify({"message": "Invalid sort parameters"}), 400

        reverse = (sort_direction == 'desc')
        sorted_posts = sorted(POSTS, key=lambda x: x[sort_type], reverse=reverse)
        return jsonify(sorted_posts), 200



@app.route('/api/posts/<int:_id>', methods=['DELETE', 'PUT'])
def update_db(_id):
    if request.method == 'DELETE':
        for i in range(len(POSTS)):
            if POSTS[i]['id'] == _id:
                del POSTS[i]

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


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    search_title = request.args.get('title')
    search_content = request.args.get('content')
    results = [
        post for post in POSTS
        if (search_title.lower() in post['title'].lower() if search_title else True) and
           (search_content.lower() in post['content'].lower() if search_content else True)
    ]

    if results:
        return jsonify(results), 200
    else:
        return jsonify({"message": f"No posts found that match your queries"}), 404


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001, debug=False)
