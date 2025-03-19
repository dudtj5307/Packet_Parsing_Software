from scapy.all import Packet, ByteField, ShortField, IntField, PacketField, Ether, raw, sendp,StrFixedLenField, IP, UDP

from scapy.all import Packet, ShortField, IntField, ByteField, PacketField


# TrkNo 패킷 정의 (모든 필드 unsigned 처리)
class TrkNo(Packet):
    name = "trkNo"
    fields_desc = [
        ShortField("trkNo1", 0),  # ushort
        ShortField("trkNo2", 0),  # ushort
        IntField("trkNo3", 0),  # uint
        IntField("trkNo4", 0)  # uint
    ]

    def post_dissection(self):
        self.trkNo1 = self.trkNo1 & 0xFFFF
        self.trkNo2 = self.trkNo2 & 0xFFFF
        self.trkNo3 = self.trkNo3 & 0xFFFFFFFF
        self.trkNo4 = self.trkNo4 & 0xFFFFFFFF


# EIE_header 패킷 정의 (모든 필드 unsigned 처리)
class EIE_header(Packet):
    name = "EIE_header"
    fields_desc = [
        PacketField("srcTN", None, TrkNo),  # TrkNo 패킷
        PacketField("dstTN", None, TrkNo),  # TrkNo 패킷
        ShortField("msgType", 0)  # ushort
    ]

    def post_dissection(self):
        if self.srcTN is not None and hasattr(self.srcTN, "post_dissection"):
            self.srcTN.post_dissection()
        if self.dstTN is not None and hasattr(self.dstTN, "post_dissection"):
            self.dstTN.post_dissection()
        self.msgType = self.msgType & 0xFFFF


# EIE_0x301: struct EIE_0x301 { EIE_header header; uchar type1; ushort type2; }
class EIE_0x301(Packet):
    name = "EIE_0x301"
    fields_desc = [
        PacketField("header", None, EIE_header),
        ByteField("type1", 0),  # uchar (unsigned 8-bit)
        ShortField("type2", 0)  # ushort
    ]

    def post_dissection(self):
        if self.header is not None and hasattr(self.header, "post_dissection"):
            self.header.post_dissection()
        self.type1 = self.type1 & 0xFF
        self.type2 = self.type2 & 0xFFFF


# EIE_0x302: struct EIE_0x302 { EIE_header header; uint type1; ushort type2; uchar type3; int type4; short type5; char type6; }
class EIE_0x302(Packet):
    name = "EIE_0x302"
    fields_desc = [
        PacketField("header", None, EIE_header),
        IntField("type1", 0),  # uint
        ShortField("type2", 0),  # ushort
        ByteField("type3", 0),  # uchar
        IntField("type4", 0),  # int (unsigned 처리 시 uint)
        ShortField("type5", 0),  # short (unsigned 처리 시 ushort)
        ByteField("type6", 0)  # char (unsigned 8-bit)
    ]

    def post_dissection(self):
        if self.header is not None and hasattr(self.header, "post_dissection"):
            self.header.post_dissection()
        self.type1 = self.type1 & 0xFFFFFFFF
        self.type2 = self.type2 & 0xFFFF
        self.type3 = self.type3 & 0xFF
        self.type4 = self.type4 & 0xFFFFFFFF
        self.type5 = self.type5 & 0xFFFF
        self.type6 = self.type6 & 0xFF


# EIE_0x303: struct EIE_0x303 { EIE_header header; uint type1; ushort type2; uchar type3; int type4; short type5; char type6; }
class EIE_0x303(Packet):
    name = "EIE_0x303"
    fields_desc = [
        PacketField("header", None, EIE_header),
        IntField("type1", 0),  # uint
        ShortField("type2", 0),  # ushort
        ByteField("type3", 0),  # uchar
        IntField("type4", 0),  # int (unsigned 처리 시 uint)
        ShortField("type5", 0),  # short (unsigned 처리 시 ushort)
        ByteField("type6", 0)  # char (unsigned 8-bit)
    ]

    def post_dissection(self):
        if self.header is not None and hasattr(self.header, "post_dissection"):
            self.header.post_dissection()
        self.type1 = self.type1 & 0xFFFFFFFF
        self.type2 = self.type2 & 0xFFFF
        self.type3 = self.type3 & 0xFF
        self.type4 = self.type4 & 0xFFFFFFFF
        self.type5 = self.type5 & 0xFFFF
        self.type6 = self.type6 & 0xFF

class RTPS(Packet):
    name = "RTPS"
    fields_desc = [
        StrFixedLenField("magic", b"RTPS", 4),         # 'RTPS' 문자열
        ByteField("version", 2),                         # RTPS 버전 (예: 2)
        ByteField("subversion", 1),                      # 부버전 (예: 1)
        ShortField("vendorId", 0x0102),                  # 벤더 ID (예제 값)
        StrFixedLenField("guidPrefix", b"\x00"*8, 8)    # GUID Prefix (12바이트)
    ]

class RTPS_Subheader(Packet):
    name = "RTPS_Subheader"
    fields_desc = [
        ByteField("ID", 2),
        ByteField("Endian", 2),
        ShortField("subMsgLength", 0),
    ]


if __name__ == '__main__':
    # EIE_0x301 패킷 생성 예제
    pkt301 = EIE_0x301(
        header=EIE_header(
            srcTN=TrkNo(trkNo1=10, trkNo2=20, trkNo3=30, trkNo4=40),
            dstTN=TrkNo(trkNo1=50, trkNo2=60, trkNo3=70, trkNo4=80),
            msgType=0x301  # 이제 ShortField이므로 0x301 (769) 사용 가능
        ),
        type1=100,
        type2=200
    )

    # EIE_0x302 패킷 생성 예제
    pkt302 = EIE_0x302(
        header=EIE_header(
            srcTN=TrkNo(trkNo1=11, trkNo2=21, trkNo3=31, trkNo4=41),
            dstTN=TrkNo(trkNo1=51, trkNo2=61, trkNo3=71, trkNo4=81),
            msgType=0x302
        ),
        type1=111,
        type2=112,
        type3=113,
        type4=114,
        type5=115,
        type6=70
    )

    # EIE_0x303 패킷 생성 예제 (구조는 EIE_0x302와 동일)
    pkt303 = EIE_0x303(
        header=EIE_header(
            srcTN=TrkNo(trkNo1=12, trkNo2=22, trkNo3=32, trkNo4=42),
            dstTN=TrkNo(trkNo1=52, trkNo2=62, trkNo3=72, trkNo4=82),
            msgType=0x303
        ),
        type1=121,
        type2=122,
        type3=123,
        type4=124,
        type5=125,
        type6=126
    )

    # 패킷 구조 확인
    print("EIE_0x301 packet:")
    pkt301.show()
    print("\nEIE_0x302 packet:")
    pkt302.show()
    print("\nEIE_0x303 packet:")
    pkt303.show()

    # Ethernet, IP, UDP, RTPS 계층 추가 (RTPS 포함)
    eth = Ether(dst="ff:ff:ff:ff:ff:ff")
    ip = IP(dst="192.168.1.100")  # 목적지 IP 주소 (테스트 환경에 맞게 변경)
    udp = UDP(sport=12345, dport=54321)  # 임의의 포트 번호 설정
    rtps = RTPS()  # RTPS 헤더 (기본값 사용)

    # 각 EIE 패킷을 Ethernet/IP/UDP/RTPS 계층으로 감싸기
    pkt301_full = eth / ip / udp / rtps / pkt301
    pkt302_full = eth / ip / udp / rtps / pkt302
    pkt303_full = eth / ip / udp / rtps / pkt303

    # raw()를 이용해 실제 패킷 바이트 확인 (디버깅용)
    # from scapy.all import raw
    # print("\nRaw bytes (hex) for EIE_0x301:")
    # print(raw(pkt301_full).hex())
    # print("\nRaw bytes (hex) for EIE_0x302:")
    # print(raw(pkt302_full).hex())
    # print("\nRaw bytes (hex) for EIE_0x303:")
    # print(raw(pkt303_full).hex())

    # 실제 네트워크로 패킷 전송 (테스트 시 주석 해제, iface는 본인 환경에 맞게 설정)
    # from scapy.all import sendp
    sendp(pkt301_full, iface="이더넷")
    sendp(pkt302_full, iface="이더넷")
    sendp(pkt303_full, iface="이더넷")