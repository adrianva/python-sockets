# python-sockets
Pet project to play with sockets in Python
You simply need to have installed Python 2.7 in order to run it

## Server

To run the server do the follwing:

- Open a terminal.
- Go to the project directory: `cd /path/to/project/`
- Type the following command: `python server.py`

The server is ready to accept incoming connections from clients.

## Client

To run a client do the following:

- Open a terminal.
- Go to the projecet directory: `cd /path/to/project/`
- Type the following command: `python client.py <server_ip> <server_port>`. For example, `python client.py localhost 5000`.
- If the connection is sucessful, the client should receive the following message from the server: 

> Connected to remote host. Start sending messages

> \<server response> Entered room

Now you can begin sending messages to the server. They should be echoed back to the client.

> \<You> This is as test

> \<server response> This is as test


