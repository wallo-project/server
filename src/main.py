from threading import Thread
from api.app import app
import uvicorn


def main() -> None:
    api_thread: Thread = Thread(target=uvicorn.run(app, port=8080))
    #network_server_thread: Thread = Thread()

    api_thread.run()

if __name__ == '__main__':
    main()