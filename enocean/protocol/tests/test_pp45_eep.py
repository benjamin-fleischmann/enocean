# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import
import pytest
from enocean.protocol.packet import Packet, RadioPacket
from enocean.protocol.eep import EEP
from enocean.protocol.constants import RORG
from enocean.decorators import timing

import dataclasses

@dataclasses.dataclass
class PP45TestCase:
    data: list
    operation_mode: int
    ventilation_level: int

    def id(self):
        return f"OM:{self.operation_mode}, VL:{self.ventilation_level}"

@pytest.mark.parametrize("test_case", [
(PP45TestCase(data=[0xd1, 0x27, 0x0, 0x08, 0x0, 0x0, 0x5, 0x1a, 0xea, 0xbd, 0x81],operation_mode=1,ventilation_level=0)),
(PP45TestCase(data=[0xd1, 0x27, 0x0, 0x09, 0x3c, 0x0, 0x5, 0x1a, 0xea, 0xbd, 0x81],operation_mode=1,ventilation_level=1)),
(PP45TestCase(data=[0xd1, 0x27, 0x0, 0x0a, 0x3c, 0x0, 0x5, 0x1b, 0x76, 0x84, 0x82],operation_mode=1,ventilation_level=2)),
(PP45TestCase(data=[0xd1, 0x27, 0x0, 0x0b, 0x3c, 0x0, 0x5, 0x1b, 0x76, 0x84, 0x81],operation_mode=1,ventilation_level=3)),
(PP45TestCase(data=[0xd1, 0x27, 0x0, 0x0c, 0x3c, 0x0, 0x5, 0x1a, 0xea, 0xbd, 0x81],operation_mode=1,ventilation_level=4)),
(PP45TestCase(data=[0xd1, 0x27, 0x0, 0x0d, 0x3c, 0x0, 0x5, 0x1a, 0xea, 0xbd, 0x81],operation_mode=1,ventilation_level=5)),
(PP45TestCase(data=[0xd1, 0x27, 0x0, 0x20, 0x0, 0x0, 0x5, 0x1b, 0x76, 0x84, 0x82],operation_mode=0,ventilation_level=0)),
(PP45TestCase(data=[0xd1, 0x27, 0x0, 0x21, 0x10, 0x0, 0x5, 0x1b, 0x76, 0x84, 0x81],operation_mode=0,ventilation_level=1)),
(PP45TestCase(data=[0xd1, 0x27, 0x0, 0x02, 0x18, 0x0, 0x5, 0x1a, 0xea, 0xbd, 0x81],operation_mode=0,ventilation_level=2)),
(PP45TestCase(data=[0xd1, 0x27, 0x0, 0x03, 0x1, 0x0, 0x5, 0x1a, 0xea, 0xbd, 0x81],operation_mode=0,ventilation_level=3)),
(PP45TestCase(data=[0xd1, 0x27, 0x0, 0x04, 0x1e, 0x0, 0x5, 0x1b, 0x76, 0x84, 0x81],operation_mode=0,ventilation_level=4)),
(PP45TestCase(data=[0xd1, 0x27, 0x0, 0x05, 0x3b, 0x0, 0x5, 0x1b, 0x76, 0x84, 0x81],operation_mode=0,ventilation_level=5))],
ids=PP45TestCase.id)
@timing(1000)
def test_d1270_telegrams(test_case):
    ''' Tests RADIO message for EEP -profile 0xd1 0x27 0x0 '''
    """
    05:1B:76:84->05:1A:EA:AD (-71 dBm): 0x01 
    ['0xd1', '0x27', '0x0', '0x21', '0x10', '0x0', '0x5', '0x1b', '0x76', '0x84', '0x81']
    ['0x0', '0x5', '0x1a', '0xea', '0xad', '0x47', '0x0']
    """
    packet = RadioPacket(0x01,
        data=test_case.data,
        optional=[0x00, 0x05, 0x1a, 0xea, 0xad, 0x47, 0x0]
    )
    assert packet.rorg == 0xd1
    assert packet.rorg_func == 0x27
    assert packet.rorg_type == 0x0
    assert packet.parse_eep(0x27, 0x0) == ['OM','VL']
    assert packet.parsed['OM']['raw_value'] == test_case.operation_mode
    assert packet.parsed['VL']['raw_value'] == test_case.ventilation_level
    assert packet.learn is False
    assert packet.contains_eep is True
    # assert packet.status == 0x00
    # assert packet.repeater_count == 0
    # assert packet.sender == [0x05, 0x1B, 0x76, 0x84]
    # assert packet.sender_hex == '05:1B:76:84'
