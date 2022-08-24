import binascii
import struct
from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.type_maps import get_type_map


class Resource:
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        self.type_hash = struct.unpack('<Q', stream.read(8))[0]
        self.version = version
        little_endian_type = '{0:X}'.format(self.type_hash)
        type_map = get_type_map(version)
        if little_endian_type in type_map:
            self.type = type_map[little_endian_type]
        else:
            self.type = 'Unknown Type'
        self.size = struct.unpack('<I', stream.read(4))[0]
        self.uuid = stream.read(16)

    def __str__(self):
        return '{}: {}'.format(self.type, binascii.hexlify(self.uuid).decode('ASCII'))

    def __repr__(self):
        return self.__str__()
