from typing_extensions import Self
from pydantic import BaseModel, model_validator

class Flags(BaseModel):
    is_flip: bool = True
    is_zoom: bool = True

class Flags2(BaseModel):
    is_flip: bool = True
    is_zoom: bool = True

    @model_validator(mode='after')
    def validate(self)->Self:
        if self.is_flip == False and self.is_zoom == False:
            raise ValueError('must has one True field.')
        return self

if __name__=='__main__':
    import unittest
    class TestExpectedFlagsBehavior(unittest.TestCase):
        '''正常値テスト'''
        def test_True_True(self):
            f = Flags2()
            self.assertEqual(f.is_flip, True)
            self.assertEqual(f.is_zoom, True)
        def test_False_True(self):
            is_flip = False
            is_zoom = True
            f = Flags2(is_flip=is_flip, is_zoom=is_zoom)
            self.assertEqual(f.is_flip, is_flip)
            self.assertEqual(f.is_zoom, is_zoom)
        def test_True_False(self):
            is_flip = True
            is_zoom = False
            f = Flags2(is_flip=is_flip, is_zoom=is_zoom)
            self.assertEqual(f.is_flip, is_flip)
            self.assertEqual(f.is_zoom, is_zoom)
            
        '''異常値テスト'''
        def test_False_False(self):
            is_flip = False
            is_zoom = False
            with self.assertRaises(ValueError):
                f = Flags2(is_flip=is_flip, is_zoom=is_zoom)
    unittest.main()
