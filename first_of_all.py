from datetime import datetime
from typing import Annotated, Dict
from pydantic import BaseModel, ConfigDict, Field, PositiveInt, field_validator
from annotated_types import Gt, Ge, Le

class User(BaseModel):
    id: int  
    name: str = 'John Doe'  
    signup_ts: datetime | None  
    tastes: dict[str, PositiveInt]

class User2(BaseModel):
    model_config = ConfigDict(regex_engine='rust-regex')
    id: Annotated[int, Gt(0), Le(100)]
    name: str = Field(pattern=r'^[a-zA-Z]+[a-zA-Z0-9]*$', min_length=1, max_length=10)
    signup_ts: datetime | None
    tastes: Dict[
        Annotated[str, Field(pattern=r'^[a-zA-Z]+[a-zA-Z0-9]*$', min_length=2, max_length=8)],
        Annotated[int, Ge(0), Le(100)]] | None

    @field_validator("signup_ts", mode='after')
    @classmethod
    def ensure_date_range(cls, v):
        if not (datetime(year=2024,month=4,day=29) <= v <= datetime(year=2034,month=3,day=31)):
            raise ValueError('signup_ts must be in range.')
        return v
    @field_validator("signup_ts", mode='before')
    @classmethod
    def ensure_date_type(cls, v):
        if not isinstance(v, str):
            raise TypeError('signup_ts must be str.')
        if v.count('-') != 2:
            raise ValueError('signup_ts must contains \'-\'')
        return v

import unittest
class TestUser2Validation(unittest.TestCase):
    def make_args(self, id=1, name='ore', signup_ts='2024-04-29', tastes={'score1': 50, 'score2':70}):
        return {
            'id':id,
            'name': name,
            'signup_ts': signup_ts,
            'tastes': tastes
            }
    ''' id.正常値テスト'''
    def test_id_1(self):
        j = self.make_args(id=1)
        u = User2(**j)
        self.assertEqual(j['id'], u.id)
    def test_id_100(self):
        j = self.make_args(id=100)
        u = User2(**j)
        self.assertEqual(j['id'], u.id)
    ''' id.境界値テスト'''
    def test_id_0(self):
        j = self.make_args(id=0)
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_id_101(self):
        j = self.make_args(id=101)
        with self.assertRaises(ValueError):
            u = User2(**j)
    ''' id.異常値テスト'''
    def test_id_float(self):
        j = self.make_args(id=0.5)
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_id_str(self):
        j = self.make_args(id='No.1')
        with self.assertRaises(ValueError):
            u = User2(**j)
    ''' name.正常値テスト'''
    def test_name_Tom(self):
        j = self.make_args(name='Tom')
        u = User2(**j)
        self.assertEqual(j['name'], u.name)
    def test_name_Smith_2(self):
        j = self.make_args(name='Smith2')
        u = User2(**j)
        self.assertEqual(j['name'], u.name)
    def test_name_shortest(self):
        j = self.make_args(name='X')
        u = User2(**j)
        self.assertEqual(j['name'], u.name)
    def test_name_longest(self):
        j = self.make_args(name='abcdefghij')
        u = User2(**j)
        self.assertEqual(j['name'], u.name)
    ''' name.境界値テスト'''
    def test_name_too_short(self):
        j = self.make_args(name='')
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_name_too_long(self):
        j = self.make_args(name='abcdefghijk')
        with self.assertRaises(ValueError):
            u = User2(**j)
    ''' name.異常値テスト'''
    def test_name_0Tom(self):
        j = self.make_args(name='0Tom')
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_name_some_mark(self):
        j = self.make_args(name='(>_<)')
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_name_space(self):
        j = self.make_args(name=' ')
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_name_num(self):
        j = self.make_args(name=0)
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_name_empty(self):
        j = self.make_args(name='')
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_name_Smith_Ⅱ(self):
        j = self.make_args(name='SmithⅡ')
        with self.assertRaises(ValueError):
            u = User2(**j)
    ''' signup_ts.正常値テスト'''
    def test_signup_ts_s20240429(self):
        j = self.make_args(signup_ts='2024-04-29')
        u = User2(**j)
        self.assertEqual(j['signup_ts'], u.signup_ts.strftime('%Y-%m-%d'))
    def test_signup_ts_s20280930(self):
        j = self.make_args(signup_ts='2028-09-30')
        u = User2(**j)
        self.assertEqual(j['signup_ts'], u.signup_ts.strftime('%Y-%m-%d'))
    def test_signup_ts_s20340331(self):
        j = self.make_args(signup_ts='2034-03-31')
        u = User2(**j)
        self.assertEqual(j['signup_ts'], u.signup_ts.strftime('%Y-%m-%d'))
    ''' signup_ts.境界値テスト'''
    def test_signup_ts_s20240428_range_too_old_ng(self):
        j = self.make_args(signup_ts='2024-04-28')
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_signup_ts_s20340401_range_too_new_ng(self):
        j = self.make_args(signup_ts='2034-04-01')
        with self.assertRaises(ValueError):
            u = User2(**j)
    ''' signup_ts.異常値テスト'''
    def test_signup_ts_invalid_format_ng(self):
        j = self.make_args(signup_ts='20340301')
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_signup_ts_int_ng(self):
        j = self.make_args(signup_ts=20340301)
        with self.assertRaises(TypeError):
            u = User2(**j)
    ''' tastes.正常値テスト'''
    def test_tastes_n1(self):
        j = self.make_args(tastes={'score1': 50})
        u = User2(**j)
        self.assertEqual(j['tastes'], u.tastes)
    def test_tastes_n2(self):
        j = self.make_args(tastes={'score1': 50, 'score2': 60})
        u = User2(**j)
        self.assertEqual(j['tastes'], u.tastes)
    def test_tastes_len2(self):
        j = self.make_args(tastes={'s1': 50})
        u = User2(**j)
        self.assertEqual(j['tastes'], u.tastes)
    def test_tastes_len8(self):
        j = self.make_args(tastes={'score100': 50})
        u = User2(**j)
        self.assertEqual(j['tastes'], u.tastes)
    def test_tastes_0(self):
        j = self.make_args(tastes={'score1': 0})
        u = User2(**j)
        self.assertEqual(j['tastes'], u.tastes)
    def test_tastes_100(self):
        j = self.make_args(tastes={'score1': 100})
        u = User2(**j)
        self.assertEqual(j['tastes'], u.tastes)
    def test_tastes_None(self):
        j = self.make_args(tastes=None)
        u = User2(**j)
        self.assertEqual(j['tastes'], u.tastes)
    ''' tastes.境界値テスト'''
    def test_tastes_len1_too_short(self):
        j = self.make_args(tastes={'s': 50})
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_tastes_len9_too_long(self):
        j = self.make_args(tastes={'score1000': 50})
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_tastes_val_too_small_ng(self):
        j = self.make_args(tastes={'score1': -1})
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_tastes_val_too_big_ng(self):
        j = self.make_args(tastes={'score1': 101})
        with self.assertRaises(ValueError):
            u = User2(**j)
    ''' tastes.異常値テスト'''
    def test_tastes_keyname_ng(self):
        j = self.make_args(tastes={'0score1': 50})
        with self.assertRaises(ValueError):
            u = User2(**j)
    def test_tastes_keyname_ng2(self):
        j = self.make_args(tastes={'scre-': 50})
        with self.assertRaises(ValueError):
            u = User2(**j)
if __name__=='__main__':
    unittest.main()
