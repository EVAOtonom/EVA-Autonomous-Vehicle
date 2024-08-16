// Auto-generated. Do not edit!

// (in-package evaotonom.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class sign {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.integer_value = null;
      this.float_value = null;
    }
    else {
      if (initObj.hasOwnProperty('integer_value')) {
        this.integer_value = initObj.integer_value
      }
      else {
        this.integer_value = 0;
      }
      if (initObj.hasOwnProperty('float_value')) {
        this.float_value = initObj.float_value
      }
      else {
        this.float_value = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type sign
    // Serialize message field [integer_value]
    bufferOffset = _serializer.int8(obj.integer_value, buffer, bufferOffset);
    // Serialize message field [float_value]
    bufferOffset = _serializer.float32(obj.float_value, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type sign
    let len;
    let data = new sign(null);
    // Deserialize message field [integer_value]
    data.integer_value = _deserializer.int8(buffer, bufferOffset);
    // Deserialize message field [float_value]
    data.float_value = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 5;
  }

  static datatype() {
    // Returns string type for a message object
    return 'evaotonom/sign';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '86552f94e8d05479ea1a2f8469e502c6';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int8 integer_value
    float32 float_value
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new sign(null);
    if (msg.integer_value !== undefined) {
      resolved.integer_value = msg.integer_value;
    }
    else {
      resolved.integer_value = 0
    }

    if (msg.float_value !== undefined) {
      resolved.float_value = msg.float_value;
    }
    else {
      resolved.float_value = 0.0
    }

    return resolved;
    }
};

module.exports = sign;
