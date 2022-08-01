// Copyright (c) 2022 Ultimaker B.V.
// pyArcus is released under the terms of the LGPLv3 or higher.

#ifndef ARCUS_PYTHON_MESSAGE_H
#define ARCUS_PYTHON_MESSAGE_H

#include "Arcus/Types.h"
#include <Python.h>

namespace google
{
namespace protobuf
{
class Descriptor;
class Reflection;
} // namespace protobuf
} // namespace google

namespace Arcus
{
/**
 * A simple wrapper around a Protobuf message so it can be used from Python.
 *
 * This class wraps a Protobuf message and makes it possible to get and set
 * values from the message. Message properties are exposed as Python properties
 * so can be set using things like `message.data = b"something"` from Python.
 *
 * Repeated messages are supported, using addRepeatedMessage, repeatedMessageCount
 * and getRepeatedMessage. A repeated message is returned as a PythonMessage object
 * so exposes the same API as the top level message.
 */
class PythonMessage
{
public:
    PythonMessage(google::protobuf::Message* message);
    PythonMessage(const MessagePtr& message);
    virtual ~PythonMessage();

    /**
     * Get the message type name of this message.
     */
    std::string getTypeName() const;

    /**
     * Python property interface.
     */
    bool __hasattr__(const std::string& field_name) const;
    PyObject* __getattr__(const std::string& field_name) const;
    void __setattr__(const std::string& name, PyObject* value);

    /**
     * Add an instance of a Repeated Message to a specific field.
     *
     * \param field_name The name of the field to add a message to.
     *
     * \return A pointer to an instance of PythonMessage wrapping the new Message in the field.
     */
    PythonMessage* addRepeatedMessage(const std::string& field_name);

    /**
     * Get the number of messages in a repeated message field.
     */
    int repeatedMessageCount(const std::string& field_name) const;

    /**
     * Get a specific instance of a message in a repeated message field.
     *
     * \param field_name The name of a repeated message field to get an instance from.
     * \param index The index of the item to get in the repeated field.
     *
     * \return A pointer to an instance of PythonMessage wrapping the specified repeated message.
     */
    PythonMessage* getRepeatedMessage(const std::string& field_name, int index);

    /**
     * Get a specific instance of a message in a message field.
     *
     * \param field_name The name of a repeated message field to get an instance from.
     *
     * \return A pointer to an instance of PythonMessage wrapping the specified repeated message.
     */
    PythonMessage* getMessage(const std::string& field_name);

    /**
     * Get the value of a certain enumeration.
     *
     * \param enum_value The fully-qualified name of an Enum value.
     *
     * \return The integer value of the specified enum.
     */
    int getEnumValue(const std::string& enum_value) const;

    /**
     * Internal.
     */
    MessagePtr getSharedMessage() const;

private:
    MessagePtr _shared_message;
    google::protobuf::Message* _message;
    const google::protobuf::Reflection* _reflection;
    const google::protobuf::Descriptor* _descriptor;
};
} // namespace Arcus

#endif // ARCUS_PYTHON_MESSAGE_H
