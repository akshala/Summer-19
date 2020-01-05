from flask import Flask, render_template, jsonify, abort, make_response
from flask import request, url_for
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)

tasks = [ # database - used dictionary for temporary should be mySQL
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks/', methods=['GET']) #returns the entire database
@auth.login_required
def getTasks():
    return jsonify({'tasks' : [make_public_task(task) for task in tasks]}) 
    
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET']) # returns tasks of a specific id
@auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': make_public_task(task[0])})

@app.errorhandler(404) # incase id is not found - handling of 404 error
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['POST']) # adding another task
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json: # if there is no title in task or input is not of json format
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': make_public_task(task)}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT']) # updating a task
@auth.login_required
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        print('Blank request.json')
        abort(400)
    # if 'title' in request.json and type(request.json['title']) != unicode: # checking if title is of correct format
    #     print('Error in title')
    #     abort(400)
    # if 'description' in request.json and type(request.json['description']) is not unicode: # checking if description is of correct format
    #     print('Error in desc')
    #     abort(400)
    # if 'done' in request.json and type(request.json['done']) is not bool: # checking if done is of correct format
    #     print('Error in done')
    #     abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': make_public_task(task[0])})

@app.errorhandler(400) # incase id is not found - handling of 404 error
def not_found(error):
    return make_response(jsonify({'error': str(error)}), 400)

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE']) # deleting a task
@auth.login_required
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

def make_public_task(task): # instead of task id customer gets uri
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@auth.get_password
def get_password(username):
    if username == 'akshala':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

if __name__ == "__main__":
    app.run()