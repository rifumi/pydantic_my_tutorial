from pydantic import BaseModel, ConfigDict, field_validator
import tensorflow as tf
import numpy as np

'''PydanticSchemaGenerationError
class Test(BaseModel):
    tensor:tf.Tensor|np.ndarray
    
    @field_validator('tensor', mode='after')
    @classmethod
    def tensor_validator(cls, v):
        if v.ndim not in (3, 4, 5):
            raise ValueError('tensor.ndim must be 3 or 4 or 5')
        return v
    
    @property
    def value(self):
        return self.tensor
'''

class Test2(BaseModel):
    tensor:np.ndarray|tf.Tensor
    
    @field_validator('tensor', mode='after')
    @classmethod
    def tensor_validator(cls, v):
        if v.ndim not in (3, 4, 5):
            raise ValueError('tensor.ndim must be 3 or 4 or 5')
        return v
    
    @property
    def value(self):
        return self.tensor

    class Config:
        arbitrary_types_allowed = True

class Test3(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    tensor:np.ndarray|tf.Tensor
    
    @field_validator('tensor', mode='after')
    @classmethod
    def tensor_validator(cls, v):
        if v.ndim not in (3, 4, 5):
            raise ValueError('tensor.ndim must be 3 or 4 or 5')
        return v
    
    @property
    def value(self):
        return self.tensor

if __name__=='__main__':
    tensor = tf.random.normal(shape=(1,9,9,3))
    tensor = Test2(tensor=tensor).value
    print(tensor)
    print()
    import unittest
    class ExpectedTestBehavior(unittest.TestCase):
        def get_2dim_tensor(self):
            return tf.random.normal(shape=(9,9))
        def get_3dim_tensor(self):
            return tf.random.normal(shape=(9,9,3))
        def get_4dim_tensor(self):
            return tf.random.normal(shape=(2,9,9,3))
        def get_5dim_tensor(self):
            return tf.random.normal(shape=(8,2,9,9,3))
        def get_6dim_tensor(self):
            return tf.random.normal(shape=(2,8,2,9,9,3))
        '''正常値テスト'''
        def test_ndim_3_Test2(self):
            tensor = Test2(tensor=self.get_3dim_tensor()).value
        def test_ndim_4_Test2(self):
            tensor = Test2(tensor=self.get_4dim_tensor()).value
        def test_ndim_5_Test2(self):
            tensor = Test2(tensor=self.get_5dim_tensor()).value
        '''異常値テスト'''
        def test_ndim_2_Test2(self):
            with self.assertRaises(ValueError):
                tensor = Test2(tensor=self.get_2dim_tensor()).value
        def test_ndim_6_Test2(self):
            with self.assertRaises(ValueError):
                tensor = Test2(tensor=self.get_6dim_tensor()).value
        '''正常値テスト'''
        def test_ndim_3_Test3(self):
            tensor = Test3(tensor=self.get_3dim_tensor()).value
        def test_ndim_4_Test3(self):
            tensor = Test3(tensor=self.get_4dim_tensor()).value
        def test_ndim_5_Test3(self):
            tensor = Test3(tensor=self.get_5dim_tensor()).value
        '''異常値テスト'''
        def test_ndim_2_Test3(self):
            with self.assertRaises(ValueError):
                tensor = Test3(tensor=self.get_2dim_tensor()).value
        def test_ndim_6_Test3(self):
            with self.assertRaises(ValueError):
                tensor = Test3(tensor=self.get_6dim_tensor()).value
    unittest.main() 
