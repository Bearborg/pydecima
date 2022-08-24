import struct
from typing import BinaryIO, List, Optional
from pydecima.enums.DecimaVersion import DecimaVersion
from pydecima.resources.Resource import Resource
from pydecima.resources.structs.Ref import Ref
from pydecima._utils import parse_hashed_string


class LocalizedSimpleSoundResource(Resource):
    class SoundInfo:
        def __init__(self, stream: BinaryIO):
            self.size_1 = struct.unpack('<I', stream.read(4))[0]
            self.sample_count = struct.unpack('<I', stream.read(4))[0]
            self.unk_3 = struct.unpack('<I', stream.read(4))[0]
            assert (self.unk_3 == 0)
            self.start = struct.unpack('<I', stream.read(4))[0]
            self.unk_5 = struct.unpack('<I', stream.read(4))[0]
            assert (self.unk_5 == 0)
            self.size_2 = struct.unpack('<I', stream.read(4))[0]
            self.unk_7 = struct.unpack('<I', stream.read(4))[0]
            assert (self.unk_7 == 0)
            assert (self.size_1 == self.size_2), "size 1 and 2 don't match"

    def __init__(self, stream: BinaryIO, version: DecimaVersion):
        Resource.__init__(self, stream, version)
        self.name = parse_hashed_string(stream)
        self.unk_floats_1: List[float] = [struct.unpack('<f', stream.read(4))[0] for _ in range(17)]
        self.unk_bytes_2 = stream.read(17)
        self.unk_floats_3: List[float] = [struct.unpack('<f', stream.read(4))[0] for _ in range(9)]
        self.unk_bytes_4 = stream.read(3)
        self.state_relative_mix = Ref(stream, self.version)
        self.sound_preset = Ref(stream, self.version)
        filename_len = struct.unpack('<I', stream.read(4))[0]
        self.sound_filename = stream.read(filename_len).decode('UTF8')
        self.language_flags = struct.unpack('<H', stream.read(2))[0]
        assert (self.language_flags <= 0xFFF), "unrecognized language flag"
        self.unk_byte_5 = stream.read(1)
        self.audio_type = struct.unpack('<b', stream.read(1))[0]
        # 9: at9
        # b: mp3
        # d: at9, TODO: Figure out what's different from 9
        # f: aac, ps4-only
        assert (self.audio_type in [0x09, 0x0b, 0x0d, 0x0f]), f"unrecognized sound type {self.audio_type}"
        self.unk_bytes_6 = stream.read(4)
        self.sample_rate = struct.unpack('<I', stream.read(4))[0]
        self.bits_per_sample = struct.unpack('<H', stream.read(2))[0]
        self.bit_rate = struct.unpack('<I', stream.read(4))[0]
        self.unk_short_8 = struct.unpack('<H', stream.read(2))[0]
        self.unk_short_9 = struct.unpack('<H', stream.read(2))[0]
        self.sound_info: List[Optional[LocalizedSimpleSoundResource.SoundInfo]] = list()
        for i in range(12):
            if self.language_flags & (1 << i) != 0:
                self.sound_info.append(LocalizedSimpleSoundResource.SoundInfo(stream))
            else:
                self.sound_info.append(None)

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)
