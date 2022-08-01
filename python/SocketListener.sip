// Copyright (c) 2022 Ultimaker B.V.
// pyArcus is released under the terms of the LGPLv3 or higher.

class SocketListener
{
    %TypeHeaderCode
    #include "Arcus/SocketListener.h"
    %End

public:
    SocketListener();
    virtual ~SocketListener();

    Socket* getSocket();

    virtual void stateChanged(SocketState newState) = 0 /HoldGIL/;
    virtual void messageReceived() = 0 /HoldGIL/;
    virtual void error(const Error& error) = 0 /HoldGIL/;
};
