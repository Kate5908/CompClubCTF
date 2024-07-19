import string
from collections import Counter

def preprocess_text(text):
    return ''.join(filter(str.isalpha, text.lower()))

def split_text_into_columns(text, key_length):
    columns = ['' for _ in range(key_length)]
    for i, char in enumerate(text):
        columns[i % key_length] += char
    return columns

def get_frequencies(text):
    return Counter(text)

def chi_squared_statistic(text, expected_frequencies):
    text_frequencies = get_frequencies(text)
    text_length = len(text)
    chi_squared = 0
    for char in string.ascii_lowercase:
        observed = text_frequencies.get(char, 0)
        expected = expected_frequencies[char] * text_length
        chi_squared += (observed - expected) ** 2 / expected
    return chi_squared

def find_caesar_shift(column):
    expected_frequencies = {
        'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702,
        'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153,
        'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507,
        'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
        'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 'y': 0.01974,
        'z': 0.00074
    }
    best_shift = 0
    lowest_chi_squared = float('inf')
    for shift in range(26):
        shifted_text = caesar_decrypt(column, shift)
        chi_squared = chi_squared_statistic(shifted_text, expected_frequencies)
        if chi_squared < lowest_chi_squared:
            lowest_chi_squared = chi_squared
            best_shift = shift
    return best_shift

def caesar_decrypt(text, shift):
    decrypted = ''
    for char in text:
        if char in string.ascii_lowercase:
            decrypted += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            decrypted += char
    return decrypted

def vigenere_decrypt(ciphertext, key):
    plaintext = ''
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char in string.ascii_lowercase:
            shift = ord(key[i % key_length]) - 97
            plaintext += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            plaintext += char
    return plaintext

def break_vigenere_cipher(ciphertext, key_length):
    ciphertext = preprocess_text(ciphertext)
    columns = split_text_into_columns(ciphertext, key_length)
    key = ''
    for column in columns:
        shift = find_caesar_shift(column)
        key += chr(shift + 97)
    plaintext = vigenere_decrypt(ciphertext, key)
    return plaintext, key

ciphertext = """JFU DYB EJVL BXV ITV YI MPM RFGCM WN FVYIA
PIXV RWXG JGVL BXZZA NFXVP BJVGG DMMRVPH VITN
R JXZPBPZLV UMNQIC SXIBJ F FDP UIA Z
APET BJZQ P EQOJKLXGO W OP JDOM UA NGUX
LMCKF IAIB JRRW LCKMU RWX PWPVW DY BPA SPTTBP
JRRW AIL PF NDPMZ AVR JIWV VYW QXICVP
RWHC ITK LDM KWPHSTKL JGRSIRA MPJGVG GMV
ZQ RKQUUFL XG BPA CGEL IVF ZL IAG KJVCZL QVVIM_IH_KBH/{IMBXW_IPU_HJEQMV/}
RLS WMIVYQ ETTM HCYV BA VQK YSOIVEVB IAMZG
KWQTTB NZCHM BPQL RWXZM KE RWR JTQFBN LPMGK
M LAIB OFPT YIDQLP RTV Q FF RD MPMG
KFPG EQVY RWTB PCEB IAIB ELR IAG GQLRW BV BYRGC
MW AWEBTK PQU KFPM EIU KFXGM MPVKN
YWZIZTT FM KQLQXG IP FVYG CCTKVR
LAG ITK RWHC GGK QD YIQT JFPET Q DVJXXDM
VYYI NVAWSQITVBKRJ SXIBJ ZQ PFWZQLQ
PGL BJRR IAM TGRL PUPWTICS FWVUKCG DMMRJ
RWXM PGIC XG LITB RD UM PKJ NPKIUQLP
UHZ NGRP DY BPCK G HMQTN NGAE ABCP UXMP BJVC
PGL VGMCG YZWO KFXL XINRAT HN LKD LXZPB
FVNPKB IIRGC AMZG YCGX EQNC G GXUIKE
UXMP EQIKH MPIV RPT MPG EYYBUMZORGSL W PGIC
LBTT K JCI NX UA VTTKTIUKGCZ ZMUK
YCW APCBC IAM GQBC DY QVCLQEBKQQLQ HMIZU
WPDF BPKJ UDKTLYVYGBML HCCHA MGGJ JDHS GQLP ATAB
CIKH MISG PMJK TIUK CBUZIEV YCW TQRJ M NHC
BJV BDHZA QW ZGXIBJ JCPE EQVY Y GBOPVVMJL SQUJ
Y STBMNVQH UIZIRGC MW MPXPDLAQPX BTTBP
EFKT UQBVVP RHVLWTR RHUM WEQPOWCTP EJBLM
VYMJ WMARVPPMM XKCMI GWE CK MCVM ZWE MC
MPM FRQWBVO TFAZL BPA JCPLQKM NCPKG JCII
WXZMU KM BR TWXV"""  # Replace with your Vigenère cipher text
key_length = 7

plaintext, key = break_vigenere_cipher(ciphertext, key_length)
print(f"Decrypted Text: {plaintext}")
print(f"Key: {key}")
