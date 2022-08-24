from io import BytesIO
import struct
from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.ImageStruct import ImageStruct
from pydecima._utils import parse_hashed_string


class UITexture(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name_1 = parse_hashed_string(stream)
        self.name_2 = parse_hashed_string(stream)
        assert self.name_1 == self.name_2, f"UITexture names don't match: {self.name_1}, {self.name_2}"
        self.initial_width = struct.unpack('<I', stream.read(4))[0]
        self.initial_height = struct.unpack('<I', stream.read(4))[0]
        self.sizes = struct.unpack('<II', stream.read(8))
        self.image_data = ImageStruct(BytesIO(stream.read(self.sizes[0])), version) if self.sizes[0] > 0 else None
        self.image_data_2 = ImageStruct(BytesIO(stream.read(self.sizes[1])), version) if self.sizes[1] > 0 else None

    def __str__(self):
        streamed = hasattr(self.image_data_2, "size_of_stream") and self.image_data_2.size_of_stream > 0
        return f'{self.type}: {self.name_2}, {self.image_data_2.width}x{self.image_data_2.height}, ' + \
               f'{self.image_data_2.image_format.name}, {"streamed " if streamed else ""}' + \
               f'@{hex(self.image_data_2.stream_start) if streamed else "internal"}'
