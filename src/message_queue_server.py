import argparse
import json

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask import Response
from flask import request

from src import raft

SCHEDULER_INTERVAL = 60
app = Flask(__name__)
node = None
queue = []

SUCCESS_RESPONSE = json.dumps({'status': 'succeeded'})
FAIL_RESPONSE = json.dumps({'status': 'succeeded'})


def run_background_tasks():
    if node.check_heartbeat_timeout():
        initiate_leader_election()


scheduler = BackgroundScheduler()


def initiate_leader_election():
    print(f'initiating leader election!')
    for sibling_server in node.sibling_nodes:
        pass


# TODO: topics
@app.route('/messageQueue/message', methods=['GET'])
def get_message():
    """
    Removes the first message in the queue and returns it to client (FIFO). If queue is empty, 403-not found response is
    returned.
    :return:
    """
    if queue:
        return Response(json.dumps(queue.pop(0)), status=200, mimetype='application/json')
    else:
        return Response(FAIL_RESPONSE, status=403, mimetype='application/json')


@app.route('/messageQueue/message', methods=['PUT'])
def put_message():
    """
    Adds the message to end of the queue.
    :return:
    """
    message = json.loads(request.get_data().decode('utf-8'))
    queue.append(message)
    return Response(SUCCESS_RESPONSE, status=201, mimetype='application/json')


@app.route('/heartbeats/heartbeat', methods=['POST'])
def post_heartbeat():
    """
    Leader calls this endpoint to send periodic heartbeats.
    :return:
    """
    pass
    # TODO


@app.route('/logs/sync', methods=['POST'])
def sync_logs():
    """
    Leader sends logs data for syncing.
    :return:
    """
    pass
    # TODO


@app.route('/election/vote', methods=['POST'])
def vote_leader():
    """
    A candidate calls this api for requesting votes for leader election.
    :return:
    """
    pass
    # TODO


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=str, help="host of the message queue server")
    parser.add_argument("port", type=str, help="port of the message queue server")
    parser.add_argument("sibling_nodes", nargs='+', help="other nodes addresses")
    args = parser.parse_args()
    node = raft.Node(args.sibling_nodes)
    scheduler.add_job(func=run_background_tasks, trigger="interval", seconds=SCHEDULER_INTERVAL)
    scheduler.start()
    app.run(host=args.host, port=args.port)