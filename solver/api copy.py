from flask import Flask, request
from celery import Celery


app = Flask(__name__)
celery = Celery('tasks', broker='amqp://guest:guest@rabbit:5672//')

@app.route('/start_task', methods=['POST'])
def start_task():
    # Get arguments from the request data
    print("Test")
    print(request.get_json(force=True))
    data = request.get_json(force=True)
    arg = data.get('arg')

    # Pass the argument to the task
    task = long_running_task.delay(arg)
    return {'task_id': task.id}, 202

@celery.task(bind=True)
def long_running_task(self, arg):
    # Your long running task here
    # You can now use 'arg' in your task
    print(arg)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


if __name__ == "__main__":
    print("ydgdsa")
    app.run(host='0.0.0.0', port=5000)