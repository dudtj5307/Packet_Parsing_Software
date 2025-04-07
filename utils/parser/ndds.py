from scapy.layers.inet import UDP
from scapy.packet import Raw

from scapy.packet import Packet
from scapy.fields import ByteField, XIntField, XShortField, StrFixedLenField
from scapy.all import bind_layers

class NDDS(Packet):
    name = "NDDS"
    fields_desc = [
        XIntField("magic", 0x52545053),  # 'RTPS' in ASCII
        ByteField("version_major", 2),   # RTPS 버전 (예: 2.3 -> major=2, minor=3)
        ByteField("version_minor", 3),
        ByteField("vendor_id_major", 1),
        ByteField("vendor_id_minor", 2),
        StrFixedLenField("guid_prefix", b"\x00" * 8, 8)  # 8바이트 GUID Prefix
    ]

    def guess_payload_class(self, payload):
        if self.magic == 0x52545053:  # 올바른 RTPS magic number인지 확인
            return Packet.guess_payload_class(self, payload)
        else:
            return Raw  # 올바르지 않으면 Raw 데이터로 처리

    def post_dissect(self, s):
        # Validate Magic Number
        if self.magic != 0x52545053:
            # Change instance to Raw if Wrong magic number
            self.__class__ = Raw
        return s


bind_layers(UDP, NDDS)

