# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth_notify.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)


_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x11\x61uth_notify.proto\x12\x11google.golang.org""\n\x0fUserDataRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t"B\n\x10UserDataResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x11\n\ttelephone\x18\x03 \x01(\t2f\n\nAuthNotify\x12X\n\x0bGetUserData\x12".google.golang.org.UserDataRequest\x1a#.google.golang.org.UserDataResponse"\x00\x62\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "auth_notify_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _USERDATAREQUEST._serialized_start = 40
    _USERDATAREQUEST._serialized_end = 74
    _USERDATARESPONSE._serialized_start = 76
    _USERDATARESPONSE._serialized_end = 142
    _AUTHNOTIFY._serialized_start = 144
    _AUTHNOTIFY._serialized_end = 246
# @@protoc_insertion_point(module_scope)
