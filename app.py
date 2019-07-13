from flask import (
    Flask, jsonify, request
)
import requests

from assign_tasks import find_assignees

app = Flask(__name__)

TOKEN = 'bUhC8AMDCOjkrsz0a453g9gZdq3TSxpglFH0JeEgUDw5EUWMhIEZNekZ4faC'

@app.route('/tasks', methods=['POST'])
def assign_tasks():
    #if (
    #    request.method != 'POST' or
    #    request.headers['content-type'] != 'application/json'
    #):
    #    return jsonify(['NOK']), 405

    tasks = request.data
    tasks_with_assignees = find_assignees(tasks)

    submit_url = 'http://airhack-api.herokuapp.com/api/submitTasks'
    response = requests.post(
        submit_url,
        headers={'Authorization': 'Bearer ' + TOKEN},
        json=tasks_with_assignees,
    )

    print(response.json())
    return jsonify(tasks_with_assignees)


if __name__ == '__main__':
    app.run(debug=True)
