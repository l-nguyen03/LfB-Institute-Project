import time
import zmq

context = zmq.Context()
socket1 = context.socket(zmq.REP)
socket2 = context.socket(zmq.REP)
socket1.bind("tcp://*:5555")
socket2.bind("tcp://*:5556")

poller = zmq.Poller()
poller.register(socket1, zmq.POLLIN)
poller.register(socket2, zmq.POLLIN)

while True:
    try:
        # Wait for incoming messages from the two sources
        socks = dict(poller.poll())

        if socket1 in socks and socks[socket1] == zmq.POLLIN:
            # Received a message from Source 1
            message = socket1.recv()
            print(f"Received request from Face recognition Source: {message}")

            # Perform the necessary operations to respond to the message from Source 1
            # ...

            # Send a response back to Source 1
            response = b"Response for Source 1"
            socket1.send(response)

        if socket2 in socks and socks[socket2] == zmq.POLLIN:
            # Received a message from Source 2
            message = socket2.recv()
            print(f"Received request from Audio Source: {message}")

            # Perform the necessary operations to respond to the message from Source 2
            # ...

            # Send a response back to Source 2
            response = b"Response for Source 2"
            socket2.send(response)

    except KeyboardInterrupt:
        # Manually exit the program if Ctrl+C is pressed
        break

socket1.close()
socket2.close()
context.term()
