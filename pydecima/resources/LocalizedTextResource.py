import struct
from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion

from pydecima.resources.Resource import Resource
from pydecima.enums.ETextLanguages import ETextLanguages


class LocalizedTextResource(Resource):
    @staticmethod
    def read_fixed_string(stream: BinaryIO):
        size = struct.unpack('<H', stream.read(2))[0]
        return stream.read(size).decode('UTF8')

    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.language = [LocalizedTextResource.read_fixed_string(stream) for _ in ETextLanguages]

    def __str__(self):
        return self.language[ETextLanguages.English].strip()

    def __repr__(self):
        return self.language[ETextLanguages.English].__repr__()
