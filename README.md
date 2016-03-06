# python-sockets
Pet project to play with sockets in Python.
You simply need to have installed Python 2.7 in order to run it.

## Server

To run the server do the following:

- Open a terminal.
- Go to the project directory: `cd /path/to/project/`
- Type the following command: `python server.py`

The server is ready to accept incoming connections from clients.

## Client

To run a client do the following:

- Open a terminal.
- Go to the project directory: `cd /path/to/project/`
- Type the following command: `python client.py <server_ip> <server_port>`. For example, `python client.py localhost 5000`.
- If the connection is sucessful, the client should receive the following message from the server: 

> Connected to remote host. Start sending messages

> \<server response> Entered room

Now you can begin sending messages to the server. They should be echoed back to the client.

> \<You> This is a test

> \<server response> This is a test

You should be able to start as many clients as you want (up to 10).

### Unit Tests

Some unit tests are included in order to ensure the basic funcionality.

If you want to run `test_client.py` you need to start the server first (as it was mentioned above).

- `python test_server.py`
- Start the server: `python server.py`
- `python test_client.py` 