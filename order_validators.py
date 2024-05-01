from typing_extensions import Self
from pydantic import model_validator
from how_to_use_model_validator import Flags2

if __name__=='__main__':
    from pydantic import field_validator, ValidationInfo
    class Flags2Derived(Flags2):
        @field_validator('is_flip', 'is_zoom', mode='after')
        @classmethod
        def fv(cls, v, vd:ValidationInfo):
            print(f'fv() v:{vd.field_name}')
            return v
        @model_validator(mode='after')
        def validatorf2d(self)->Self:
            print(f'validatorf2d() called.')
            return self
    print()
    f2d = Flags2Derived(is_flip=True, is_zoom=True)
    print(f'f2d:{f2d}')
