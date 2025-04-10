from utils.parser.log import ParseHistoryLog

log = ParseHistoryLog()

def get_packet_count(raw_file_path):
    total_packets = log.get(raw_file_path)

    # Zero packets
    if total_packets == 0:
        total_packets = 1

    # No previous parsing log
    if total_packets is None:
        total_packets = estimate_packet_count(raw_file_path)


    return total_packets

def estimate_packet_count(raw_file_path):   # TODO: make estimate count
    return 66000