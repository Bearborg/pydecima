from enum import IntEnum


class EWaveDataEncodingQuality(IntEnum):
    Uncompressed__PCM_ = 0x0,
    Lossy_Lowest = 0x1,
    Lossy_Low = 0x2,
    Lossy_Medium = 0x3,
    Lossy_High = 0x4,
    Lossy_Highest = 0x5
