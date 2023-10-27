from flask import Flask , request, jsonify
from flask_cors import CORS

import sqlite3

app =Flask(__name__)
CORS(app)


# conn = sqlite3.connect('todolist.db')
# cursor = conn.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, title TEXT)''')
# conn.commit()
# conn.close()

@app.route('/todo', methods=['GET'])
def get_todo():
    conn = sqlite3.connect('todolist.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todo')
    items = cursor.fetchall()
    item_list = []
    for item in items:
        item_dict = {
            'id': item[0],
            'title': item[1],  
        }
        item_list.append(item_dict)

    conn.close()
    
    return jsonify(item_list)



# @app.route('/todo', methods=['GET'])

# def get_todo():
#     conn = sqlite3.connect('todolist.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM items')
#     items = cursor.fetchall()
#     item_list = []

#     for item in items:
#         item_dict = {
#             'id': item[0],
#             'name': item[1],
#             'description': item[2]
#         }
#         item_list.append(item_dict)

#     conn.close()
#     return jsonify(item_list)
    
    # # print(items)
    # conn.close()
    # return jsonify(items)

@app.route('/todo', methods=['POST'])
def create_item():
    todo_data = request.get_json()
    conn = sqlite3.connect('todolist.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todo (title) VALUES (?)',(todo_data['title'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item created successfully"}), 201


@app.route('/todo/<int:todo_id>', methods=['PUT'])
def update_item(todo_id):
    todo_data = request.get_json()
    conn = sqlite3.connect('todolist.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE todo SET title=? WHERE id=?', (todo_data['title'], todo_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item updated successfully"})


@app.route('/todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = sqlite3.connect('todolist.db')
    cursor = conn.cursor()
    # print(todo_id)
    cursor.execute('DELETE FROM todo WHERE id=?', (todo_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)