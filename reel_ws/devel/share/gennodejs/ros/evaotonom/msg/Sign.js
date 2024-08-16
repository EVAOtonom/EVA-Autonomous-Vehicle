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

class Sign {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.sign_index = null;
      this.depth = null;
    }
    else {
      if (initObj.hasOwnProperty('sign_index')) {
        this.sign_index = initObj.sign_index
      }
      else {
        this.sign_index = 0;
      }
      if (initObj.hasOwnProperty('depth')) {
        this.depth = initObj.depth
      }
      else {
        this.depth = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Sign
    // Serialize message field [sign_index]
    bufferOffset = _serializer.int8(obj.sign_index, buffer, bufferOffset);
    // Serialize message field [depth]
    bufferOffset = _serializer.float32(obj.depth, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Sign
    let len;
    let data = new Sign(null);
    // Deserialize message field [sign_index]
    data.sign_index = _deserializer.int8(buffer, bufferOffset);
    // Deserialize message field [depth]
    data.depth = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 5;
  }

  static datatype() {
    // Returns string type for a message object
    return 'evaotonom/Sign';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9d6f7ebc229c76b7f8002caeee511826';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int8 sign_index
    float32 depth
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Sign(null);
    if (msg.sign_index !== undefined) {
      resolved.sign_index = msg.sign_index;
    }
    else {
      resolved.sign_index = 0
    }

    if (msg.depth !== undefined) {
      resolved.depth = msg.depth;
    }
    else {
      resolved.depth = 0.0
    }

    return resolved;
    }
};

module.exports = Sign;
