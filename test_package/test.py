import os
import sys

pdir = os.path.dirname(os.path.realpath(__file__))
from platform import system
if system() == "Windows":
    os.add_dll_directory(pdir)

import pyArcus
from threading import Thread
import time

sleep_msec = 250
port = 44444
ip = r"127.0.0.1"
proto_filename = "test.proto"


class Listener(pyArcus.SocketListener):

    num_messages_received = 0

    def __init__(self, sock) -> None:
        super().__init__()
        self._socket = sock

    #@override
    def stateChanged(self, state: pyArcus.SocketState) -> None:
        print(f"state changed: {state}", file=sys.stderr)

    #@override
    def messageReceived(self) -> None:
        message = self._socket.takeNextMessage()
        if message.getTypeName() != "test.proto.Progress":
            print(f"unkown message received? {message.getTypeName()}")
            return
        Listener.num_messages_received += 1
        print(f"message received: progress: {message.amount}", file=sys.stderr)

    #@override
    def error(self, error: pyArcus.Error) -> None:
        is_debug = error.getErrorCode() == pyArcus.ErrorCode.Debug
        print(f"{'debug' if is_debug else 'error'}: {error.getErrorMessage()}", file=(sys.stderr if is_debug else sys.stdout))
        # Yes, print errors to stdout and debug to stderr (since the test looks at the output).


def newSocket():
    full_proto_filename = os.path.join(pdir, proto_filename).replace("\\", "/")
    socket = pyArcus.Socket()
    socket.registerAllMessageTypes(full_proto_filename)
    return socket


def connectSend():
    socket = newSocket()
    listener = Listener(socket)
    socket.addListener(listener)
    socket.connect(ip, port)

    socket_state = pyArcus.SocketState.Closed
    while socket_state != pyArcus.SocketState.Connected and socket_state != pyArcus.SocketState.Error:
        print(".", file=sys.stderr, end="")
        time.sleep(sleep_msec/1000.0)
        socket_state = socket.getState()

    if socket_state != pyArcus.SocketState.Connected:
        return None

    return socket


def receive():
    socket = newSocket()
    listener = Listener(socket)
    socket.addListener(listener)
    socket.listen(ip, port)

    # About 4 seconds should be more than enough to do all tests:
    for _ in range(0, int(4000.0/sleep_msec)):
        print(".", file=sys.stderr, end="")
        time.sleep(sleep_msec/1000.0)


# Start thread to receive.
td = Thread(target = receive)
td.start()
time.sleep(0.5)

# Send messages to other thread via protobuf.
socket = connectSend()
if not socket:
    print("Failed to connect.")
    print("False")
    sys.exit(1)
print("Connected", file=sys.stderr)

# Send a number of messages.
total = 100.0
inc = 12.5
should_receive = int(total/inc)
for progress in range(0, should_receive):
    message = socket.createMessage("test.proto.Progress")
    message.amount = progress
    socket.sendMessage(message)
    print(f"{progress}", file=sys.stderr)
    time.sleep(sleep_msec/1000.0)

# Check result.
print("True" if Listener.num_messages_received == should_receive else "False")
