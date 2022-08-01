// Copyright (c) 2022 Ultimaker B.V.
// pyArcus is released under the terms of the LGPLv3 or higher.

// Convert a python str object to a std::string.
%MappedType std::string
{
%TypeHeaderCode
#include <string>
%End

%ConvertFromTypeCode
    // convert a std::string to a Python (unicode) string
    PyObject* newstring;
    newstring = PyUnicode_DecodeUTF8(sipCpp->c_str(), sipCpp->length(), NULL);
    if(newstring == NULL) {
        PyErr_Clear();
        newstring = PyBytes_FromString(sipCpp->c_str());
    }
    return newstring;
%End

%ConvertToTypeCode
    // Allow a Python string (or a unicode string) whenever a string is
    // expected.
    // If argument is a Unicode string, just decode it to UTF-8
    // If argument is a Python string, assume it's UTF-8
    if (sipIsErr == NULL)
        return (PyBytes_Check(sipPy) || PyUnicode_Check(sipPy));

    if (sipPy == Py_None)
    {
        *sipCppPtr = new std::string;
        return 1;
    }

    if (PyUnicode_Check(sipPy))
    {
        PyObject* s = PyUnicode_AsEncodedString(sipPy, "UTF-8", "");
        *sipCppPtr = new std::string(PyBytes_AS_STRING(s));
        Py_DECREF(s);
        return 1;
    }

    if (PyBytes_Check(sipPy))
    {
        *sipCppPtr = new std::string(PyBytes_AS_STRING(sipPy));
        return 1;
    }
    return 0;
%End
};

// Convert a MessagePtr (aka std::shared_ptr<google::protobuf::Message>) to a PythonMessage*
%MappedType MessagePtr
{
%TypeHeaderCode
#include <memory>
#include "pyArcus/PythonMessage.h"
%End

%ConvertFromTypeCode
    // Convert a Protobuf message to a Python object
    if(!(*sipCpp))
    {
        PyErr_SetString(PyExc_ValueError, "Unknown message type");
        return NULL;
    }

    const sipTypeDef* message_type = sipFindType("PythonMessage");

    PythonMessage* message = new PythonMessage(*sipCpp);

    sipTransferObj = Py_None;

    PyObject* msg = sipConvertFromType(message, message_type, sipTransferObj);
    if(!msg)
    {
        delete message;
        return NULL;
    }

    return msg;
%End

%ConvertToTypeCode
    // Convert a Python object to a Protobuf message
    const sipTypeDef* message_type = sipFindType("PythonMessage");

    if(sipIsErr == NULL)
    {
        return sipCanConvertToType(sipPy, message_type, SIP_NOT_NONE);
    }

    if(sipCanConvertToType(sipPy, message_type, SIP_NOT_NONE))
    {
        int iserr = 0;
        int state = 0;

        PythonMessage* message = reinterpret_cast<PythonMessage*>(sipConvertToType(sipPy, message_type, NULL, 0, &state, &iserr));

        if(iserr != 0)
        {
            PyErr_SetString(PyExc_ValueError, "Could not convert to Message");
            return 0;
        }

        MessagePtr msg = message->getSharedMessage();
        *sipCppPtr = new MessagePtr(msg);

        sipReleaseType(message, message_type, state);
    }

    return sipGetState(sipTransferObj);
%End

};

%UnitCode
#include "Arcus/Types.h"
%End

enum class SocketState
{
    Initial,
    Connecting,
    Connected,
    Opening,
    Listening,
    Closing,
    Closed,
    Error
};
