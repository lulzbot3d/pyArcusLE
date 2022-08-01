// Copyright (c) 2022 Ultimaker B.V.
// pyArcus is released under the terms of the LGPLv3 or higher.

class PythonMessage
{
    %TypeHeaderCode
    #include "pyArcus/PythonMessage.h"
    %End

public:
    virtual ~PythonMessage();

    std::string getTypeName() const;

    bool __hasattr__(const std::string&) const /AllowNone/;
    PyObject* __getattr__(const std::string&) const /AllowNone, HoldGIL/;
    void __setattr__(const std::string&, PyObject*) /AllowNone/;
    %MethodCode
    sipCpp->__setattr__(*a0, a1);
    %End

    void __delattr__(const std::string&);
    %MethodCode
    PyErr_SetString(PyExc_NotImplementedError, "__delattr__ not supported on messages.");
    return 0;
    %End

    PythonMessage* addRepeatedMessage(const std::string& field_name) /TransferBack/;
    int repeatedMessageCount(const std::string& field_name) const;
    PythonMessage* getRepeatedMessage(const std::string& field_name, int index) /TransferBack/;
    PythonMessage* getMessage(const std::string& field_name) /TransferBack/;

    int getEnumValue(const std::string& enum_value) const;

private:
    PythonMessage();
};
