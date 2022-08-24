import binascii
import os
import struct
from typing import TypeVar, Generic, BinaryIO, Dict

import pydecima
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource
from pydecima._utils import parse_hashed_string

T = TypeVar('T')


class Ref(Generic[T]):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        self.version = version
        self.type: int = struct.unpack('<B', stream.read(1))[0]
        if self.type > 0:
            self.hash: bytes = stream.read(16)
        if self.type in [2, 3]:
            self.path: str = parse_hashed_string(stream)

    def follow(self, resource_dict: Dict[bytes, Resource]) -> T:
        if self.type == 0:
            return None
        if self.hash in resource_dict:
            return resource_dict[self.hash]
        elif hasattr(self, 'path'):
            full_path = os.path.join(pydecima.reader.game_root, self.path) + '.core'
            pydecima.reader.read_objects(full_path, resource_dict)
            if self.hash in resource_dict:
                return resource_dict[self.hash]
        raise Exception('Resource not in list: {}'.format(self.__str__()))

    def __str__(self):
        ret = 'Type {} Ref: '.format(self.type)
        if hasattr(self, 'hash'):
            ret += binascii.hexlify(self.hash).decode('ASCII')
        if hasattr(self, 'path'):
            ret += ', ' + self.path
        return ret

    def __repr__(self):
        return self.__str__()
