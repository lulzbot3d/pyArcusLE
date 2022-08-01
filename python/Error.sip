// Copyright (c) 2022 Ultimaker B.V.
// pyArcus is released under the terms of the LGPLv3 or higher.

enum class ErrorCode
{
    UnknownError,
    CreationError,
    ConnectFailedError,
    BindFailedError,
    AcceptFailedError,
    SendFailedError,
    ReceiveFailedError,
    UnknownMessageTypeError,
    ParseFailedError,
    ConnectionResetError,
    MessageRegistrationFailedError,
    InvalidStateError,
    InvalidMessageError,
    Debug,
};

class Error
{
    %TypeHeaderCode
    #include "Arcus/Error.h"
    %End

public:
    Error();
    Error(ErrorCode error_code, const std::string& error_message);
    Error(const Error& error);

    ErrorCode getErrorCode() const;
    std::string getErrorMessage() const;
    bool isFatalError() const;
    bool isValid() const;
    void setFatalError(bool fatal);

    PyObject* __repr__();
    %MethodCode
    return PyUnicode_FromString(sipCpp->toString().c_str());
    %End
};
