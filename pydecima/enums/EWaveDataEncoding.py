from enum import IntEnum


class EWaveDataEncoding(IntEnum):
    PCM = 0x0,
    PCM_FLOAT = 0x1,
    XWMA = 0x2,
    ATRAC9 = 0x3,
    MP3 = 0x4,
    ADPCM = 0x5,
    AAC = 0x6
