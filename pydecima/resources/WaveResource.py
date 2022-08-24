import struct
from pydecima.enums.EWaveDataEncoding import EWaveDataEncoding
from pydecima.enums.EWaveDataEncodingQuality import EWaveDataEncodingQuality
from typing import BinaryIO
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource
from pydecima._utils import parse_hashed_string


class WaveResource(Resource):
    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        start_pos = stream.tell()
        Resource.__init__(self, stream, version)
        stream.seek(start_pos + 12)
        self.encoding_quality = EWaveDataEncodingQuality(struct.unpack('<I', stream.read(4))[0])
        self.unk_bytes1 = struct.unpack('<bb', stream.read(2))
        self.uuid = stream.read(16)
        self.name = parse_hashed_string(stream)
        self.size_without_stream = struct.unpack('<I', stream.read(4))[0]
        if self.size_without_stream > 0:
            self.sound = stream.read(self.size_without_stream)
        self.size_with_stream = struct.unpack('<I', stream.read(4))[0]
        self.sample_rate = struct.unpack('<I', stream.read(4))[0]
        self.channels = struct.unpack('<b', stream.read(1))[0]
        self.encoding = EWaveDataEncoding(struct.unpack('<I', stream.read(4))[0])
        self.unk_short4 = struct.unpack('<H', stream.read(2))[0]
        self.bit_rate = struct.unpack('<I', stream.read(4))[0]
        self.unk_short5 = struct.unpack('<H', stream.read(2))[0]
        self.unk_short6 = struct.unpack('<H', stream.read(2))[0]
        self.unk_bytes7 = struct.unpack('<bbbbbb', stream.read(6))
        if self.size_with_stream != self.size_without_stream:
            cache_len = struct.unpack('<I', stream.read(4))[0]
            self.cache_string = stream.read(cache_len).decode('ASCII')
            self.unk_ints8 = struct.unpack('<IIII', stream.read(16))

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
