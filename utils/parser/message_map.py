from collections import defaultdict

# TIE Label Map
TIE_LABEL_NAME = {
    0 : 'SYS',      '0' : 'SYS',
    1 : 'SURV',     '1' : 'SURV',
    2 : 'EW',       '2' : 'EW',
    3 : 'CMD',      '3' : 'CMD',
    4 : 'INFO',     '4' : 'INFO',
    5 : 'EXT',      '5' : 'EXT',
    6 : 'FILT',     '6' : 'FILT',
    7 : 'INTELLI',  '7' : 'INTELLI',
    8 : 'PTXT',     '8' : 'PTXT',
    9 : 'MISC',     '9' : 'MISC',
    11: 'TEST',     '11': 'TEST',       # TODO: how to handel SUBLABEL (B01 B02)
}

