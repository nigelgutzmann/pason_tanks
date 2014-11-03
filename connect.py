import zmq
import json

def connect_to_game(password="", team="", token="", host=""):
    state_channel = connect_to_state_channel(host)
    (client_token, command_channel) = connect_to_command_channel(password, team, token, host)
    return (client_token, command_channel, state_channel)

def conenct_to_command_channel(password, team, token, host):
    """
    The command channel exists on port 5557. It uses request/response
    """
    context = zmq.Context()
    request_socket = context.socket(zmq.REQ)
    request_socket.connect('tcp://%s:5557' % host)

    # now that we are connected, we need to send the MATCH_CONNECT
    client_token = connect_to_match(request_socket, password, team, token, host)
    return (client_token, request_socket)


def connect_to_state_channel(host):
    """
    The state channel exists on port 5556. It uses pub/sub.
    """
    context = zmq.Context()
    subscriber_socket = context.socket(zmq.SUB)
    subscriber_socket.connect("tcp://%s:5556" % host)
    return subscriber_socket


def connect_to_match(command_channel, password, team, token, host):
    print "Sending match connect request..."
    command_channel.send(json.dumps({
        'comm_type': 'MatchConnect',
        'match_token': token,
        'team_name': team,
        'password': password
    }))
    response = socket.recv()

    print "Received reply: "
    print response

    response_data = json.loads(response)

    client_token = None
    try:
        client_token = response_data['client_token']
    except:
        command_channel.close()
        connect_to_command_channel(password, team, token, host)

    print "Client token: " + client_token
    return client_token