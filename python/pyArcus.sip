// Copyright (c) 2022 Ultimaker B.V.
// pyArcus is released under the terms of the LGPLv3 or higher.

%Module(name = pyArcus, call_super_init = True)

%Include Types.sip
%Include SocketListener.sip
%Include PythonMessage.sip
%Include Error.sip

%ModuleHeaderCode
using namespace Arcus;
%End

class Socket
{
    %TypeHeaderCode
    #include "Arcus/Socket.h"
    %End

public:
    Socket();
    virtual ~Socket();

    SocketState getState() const;

    Error getLastError() const;
    void clearError();

    void addListener(SocketListener* listener /TransferThis/);
    void removeListener(SocketListener* listener);

    void connect(const std::string& address, int port);
    void listen(const std::string& address, int port);
    void close() /ReleaseGIL/;
    void reset() /ReleaseGIL/;

    bool sendMessage(MessagePtr message);
    MessagePtr takeNextMessage();
    MessagePtr createMessage(const std::string& type_name);

    bool registerAllMessageTypes(const std::string& file_name);

    void dumpMessageTypes();

private:
    Socket(const Socket&);
    Socket& operator=(const Socket&);
};

