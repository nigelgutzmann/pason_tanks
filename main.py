import sys
import connect

TEAM_NAME = "ThinkTank2.0"
PASSWORD = "th1nk"
MATCH_TOKEN = ""
CLIENT_TOKEN = ""
SERVER_HOST = ""


def main(argv):
    global TEAM_NAME, PASSWORD, MATCH_TOKEN, CLIENT_TOKEN, SERVER_HOST
    if len(argv) != 2:
        raise Exception("Usage: python main.py <match_token> <server_host>")

    MATCH_TOKEN = argv[0]
    SERVER_HOST = argv[1]
    (CLIENT_TOKEN, command_channel, state_channel) = connect.connect_to_game(password=PASSWORD,
                                                                             team=TEAM_NAME,
                                                                             token=MATCH_TOKEN,
                                                                             host=SERVER_HOST
                                                                             )
    while True:
        state = state_channel.recv()
        print state


if __name__ == "__main__":
    main(sys.argv[1:])
