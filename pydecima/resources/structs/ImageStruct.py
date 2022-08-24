import struct
from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.enums.EPixelFormat import EPixelFormat


class ImageStruct:
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        self.unk_short1 = struct.unpack('<H', stream.read(2))[0]
        width = struct.unpack('<H', stream.read(2))[0]
        self.width = width & 0x3FFF
        self.width_crop = width >> 14
        height = struct.unpack('<H', stream.read(2))[0]
        self.height = height & 0x3FFF
        self.height_crop = height >> 14
        self.unk_short2 = struct.unpack('<H', stream.read(2))[0]
        self.unk_byte1 = struct.unpack('<B', stream.read(1))[0]
        self.image_format: EPixelFormat = EPixelFormat(struct.unpack('<B', stream.read(1))[0])
        self.unk_byte2 = struct.unpack('<B', stream.read(1))[0]
        self.unk_byte3 = struct.unpack('<B', stream.read(1))[0]
        self.magic = stream.read(4)
        # assert self.magic == b'\x00\xA9\xFF\x00'
        self.maybe_hash = stream.read(16)
        self.image_chunk_size = struct.unpack('<I', stream.read(4))[0]
        # TODO: Assert here?
        if version == DecimaVersion.HZDPS4:
            self.size_with_stream = struct.unpack('<I', stream.read(4))[0]
            self.size_without_stream = struct.unpack('<I', stream.read(4))[0]
            if self.size_with_stream != self.size_without_stream:
                self.size_of_stream = struct.unpack('<I', stream.read(4))[0]
                assert self.size_with_stream == self.size_without_stream + self.size_of_stream, \
                    "Stream size doesn't add up"
                self.mipmaps_in_stream = struct.unpack('<I', stream.read(4))[0]
                self.image_contents = stream.read(self.size_without_stream)
                cache_len = struct.unpack('<I', stream.read(4))[0]
                self.cache_string = stream.read(cache_len).decode('ASCII')
                self.stream_start = struct.unpack('<Q', stream.read(8))[0]
                self.stream_end = struct.unpack('<Q', stream.read(8))[0]
            else:
                stream.read(self.image_chunk_size - (self.size_without_stream + 8))  # padding
                self.image_contents = stream.read(self.size_without_stream)
        else:  # version should be HZDPC
            self.size_without_stream = struct.unpack('<I', stream.read(4))[0]
            self.size_of_stream = struct.unpack('<I', stream.read(4))[0]
            if self.size_of_stream > 0:
                self.mipmaps_in_stream = struct.unpack('<I', stream.read(4))[0]
                cache_len = struct.unpack('<I', stream.read(4))[0]
                self.cache_string = stream.read(cache_len).decode('ASCII')
                self.stream_start = struct.unpack('<Q', stream.read(8))[0]
                self.size_of_stream2 = struct.unpack('<Q', stream.read(8))[0]
                assert self.size_of_stream == self.size_of_stream2, "Stream sizes don't match"
            else:
                stream.read(self.image_chunk_size - (self.size_without_stream + 8))  # padding
            self.image_contents = stream.read(self.size_without_stream)
