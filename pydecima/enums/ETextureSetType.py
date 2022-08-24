from enum import IntEnum


class ETextureSetType(IntEnum):
    Invalid = 0x0,
    Color = 0x1,
    Alpha = 0x2,
    Normal = 0x3,
    Reflectance = 0x4,
    AO = 0x5,
    Roughness = 0x6,
    Height = 0x7,
    Mask = 0x8,
    Mask_Alpha = 0x9,
    Incandescence = 0xA,
    Translucency_Diffusion = 0xB,
    Translucency_Amount = 0xC,
    Misc_01 = 0xD,
    Count = 0xE
