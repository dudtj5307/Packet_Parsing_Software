from scapy.all import Packet, ByteField, ShortField, IntField, PacketField, Ether, raw, sendp,StrFixedLenField, IP, UDP

# msgType: struct msgType { int a; }
class MsgType(Packet):
    name = "msgType"
    fields_desc = [
        IntField("a", 0)
    ]

# trkNo: struct trkNo { msgType type; ushort trkNo1; ushort trkNo2; uint trkNo3; uint trkNo4; }
class TrkNo(Packet):
    name = "trkNo"
    fields_desc = [
        PacketField("type", None, MsgType),
        ShortField("trkNo1", 0),
        ShortField("trkNo2", 0),
        IntField("trkNo3", 0),
        IntField("trkNo4", 0)
    ]

# EIE_header: 변경 – msgType를 ShortField로 사용하여 0~65535 범위 지원
class EIE_header(Packet):
    name = "EIE_header"
    fields_desc = [
        PacketField("srcTN", None, TrkNo),
        PacketField("dstTN", None, TrkNo),
        ShortField("msgType", 0)
    ]

# EIE_0x301: struct EIE_0x301 { EIE_header header; uchar type1; ushort type2; }
class EIE_0x301(Packet):
    name = "EIE_0x301"
    fields_desc = [
        PacketField("header", None, EIE_header),
        ByteField("type1", 0),  # 0~200
        ShortField("type2", 0)
    ]

# EIE_0x302: struct EIE_0x302 { EIE_header header; uint type1; ushort type2; uchar type3; int type4; short type5; char type6; }
class EIE_0x302(Packet):
    name = "EIE_0x302"
    fields_desc = [
        PacketField("header", None, EIE_header),
        IntField("type1", 0),
        ShortField("type2", 0),
        ByteField("type3", 0),
        IntField("type4", 0),
        ShortField("type5", 0),
        ByteField("type6", 0)
    ]

# EIE_0x303: 구조 동일
class EIE_0x303(Packet):
    name = "EIE_0x303"
    fields_desc = [
        PacketField("header", None, EIE_header),
        IntField("type1", 0),
        ShortField("type2", 0),
        ByteField("type3", 0),
        IntField("type4", 0),
        ShortField("type5", 0),
        ByteField("type6", 0)
    ]

class RTPS(Packet):
    name = "RTPS"
    fields_desc = [
        StrFixedLenField("magic", b"RTPS", 4),         # 'RTPS' 문자열
        ByteField("version", 2),                         # RTPS 버전 (예: 2)
        ByteField("subversion", 1),                      # 부버전 (예: 1)
        ShortField("vendorId", 0x0102),                  # 벤더 ID (예제 값)
        StrFixedLenField("guidPrefix", b"\x00"*12, 12)    # GUID Prefix (12바이트)
    ]

if __name__ == '__main__':
    # EIE_0x301 패킷 생성 예제
    pkt301 = EIE_0x301(
        header=EIE_header(
            srcTN=TrkNo(type=MsgType(a=1), trkNo1=10, trkNo2=20, trkNo3=30, trkNo4=40),
            dstTN=TrkNo(type=MsgType(a=2), trkNo1=50, trkNo2=60, trkNo3=70, trkNo4=80),
            msgType=0x301  # 이제 ShortField이므로 0x301 (769) 사용 가능
        ),
        type1=100,
        type2=200
    )

    # EIE_0x302 패킷 생성 예제
    pkt302 = EIE_0x302(
        header=EIE_header(
            srcTN=TrkNo(type=MsgType(a=3), trkNo1=11, trkNo2=21, trkNo3=31, trkNo4=41),
            dstTN=TrkNo(type=MsgType(a=4), trkNo1=51, trkNo2=61, trkNo3=71, trkNo4=81),
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
            srcTN=TrkNo(type=MsgType(a=5), trkNo1=12, trkNo2=22, trkNo3=32, trkNo4=42),
            dstTN=TrkNo(type=MsgType(a=6), trkNo1=52, trkNo2=62, trkNo3=72, trkNo4=82),
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
    from scapy.all import raw
    print("\nRaw bytes (hex) for EIE_0x301:")
    print(raw(pkt301_full).hex())
    print("\nRaw bytes (hex) for EIE_0x302:")
    print(raw(pkt302_full).hex())
    print("\nRaw bytes (hex) for EIE_0x303:")
    print(raw(pkt303_full).hex())

    # 실제 네트워크로 패킷 전송 (테스트 시 주석 해제, iface는 본인 환경에 맞게 설정)
    # from scapy.all import sendp
    sendp(pkt301_full, iface="이더넷")
    sendp(pkt302_full, iface="이더넷")
    sendp(pkt303_full, iface="이더넷")