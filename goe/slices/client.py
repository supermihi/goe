from __future__ import annotations

import itertools
from abc import ABCMeta
from typing import ClassVar, Type

from goe.json_client import GoEJsonClient
from goe.slices.slice import StatusSlice


class SliceClientMeta(ABCMeta):
    def __new__(cls, name, bases, dct):
        if name != 'SliceClient':
            dct = SliceClientMeta.__add_slice_getters(dct)
        result = super().__new__(cls, name, bases, dct)
        return result

    @staticmethod
    def __add_slice_getters(dct):
        result = {**dct}
        if '_SLICES' not in dct:
            raise TypeError(f'{SliceClient.__name__} subclasses must set _SLICES')
        for slc in dct['_SLICES']:
            result[f'get_{slc.NAME}'] = lambda self: slc.query(self.client)
        return result


class SliceClient(metaclass=SliceClientMeta):
    _SLICES: ClassVar[tuple[StatusSlice]]

    def __init__(self, client: GoEJsonClient):
        self.client = client

    @classmethod
    def local(cls, host: str):
        """Convenience factory method using a local JSON client."""
        return cls(GoEJsonClient.local(host))

    @classmethod
    def cloud(cls, serial_number: str, cloud_api_key: str):
        """Convenience factory method using a cloud JSON client."""
        return cls(GoEJsonClient.cloud(serial_number, cloud_api_key))

    def get_slices(self, *slices: Type[StatusSlice]):
        keys = itertools.chain(*(slice.KEYS for slice in slices))
        result = self.client.query(keys=keys)
        return [slice.parse(result) for slice in slices]
