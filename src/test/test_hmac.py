import unittest
import util
from binascii import hexlify, unhexlify
from ctypes import create_string_buffer

# HMAC vectors from https://tools.ietf.org/html/rfc4231
hmac_cases = [
    ['0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b', '4869205468657265',
     '87aa7cdea5ef619d4ff0b4241a1d6cb0 2379f4e2ce4ec2787ad0b30545e17cde'
     'daa833b7d6b8a702038b274eaea3f4e4 be9d914eeb61f1702e696c203a126854'],

    ['4a656665', '7768617420646f2079612077616e7420666f72206e6f7468696e673f',
     '164b7a7bfcf819e2e395fbe73b56e0a3 87bd64222e831fd610270cd7ea250554'
     '9758bf75c05a994a6d034f65f8f0e6fd caeab1a34d4a6b4b636e070a38bce737'],

    ['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
     'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd'
     'dddddddddddddddddddddddddddddddddddd',
     'fa73b0089d56a284efb0f0756c890be9 b1b5dbdd8ee81a3655f83e33b2279d39'
     'bf3e848279a722c806b485a47e67c807 b946a337bee8942674278859e13292fb'],

    ['0102030405060708090a0b0c0d0e0f10111213141516171819',
     'cdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd'
     'cdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd',
     'b0ba465637458c6990e5a8c5f61d4af7 e576d97ff94b872de76f8050361ee3db'
     'a91ca5c11aa25eb4d679275cc5788063 a5f19741120c4f2de2adebeb10a298dd'],

    ['0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c',
     '546573742057697468205472756e636174696f6e',
     '415fad6271580a531d4179bc891d87a6'],

    ['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
     'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
     'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
     'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
     'aaaaaa',
     '54657374205573696e67204c6172676572205468616e20426c6f636b2d53697a'
     '65204b6579202d2048617368204b6579204669727374',
     '80b24263c7c1a3ebb71493c1dd7be8b4 9b46d1f41b4aeec1121b013783f8f352'
     '6b56d037e05f2598bd0fd2215d6a1e52 95e64f73f63f0aec8b915a985d786598'],

    ['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
     'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
     'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
     'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
     'aaaaaa',
     '5468697320697320612074657374207573696e672061206c6172676572207468'
     '616e20626c6f636b2d73697a65206b657920616e642061206c61726765722074'
     '68616e20626c6f636b2d73697a6520646174612e20546865206b6579206e6565'
     '647320746f20626520686173686564206265666f7265206265696e6720757365'
     '642062792074686520484d414320616c676f726974686d2e',
     'e37b6a775dc87dbaa4dfa9f96e5e3ffd debd71f8867289865df5a32d20cdc944'
     'b6022cac3c4982b10d5eeb55c3e4de15 134676fb6de0446065c97440fa8c6a58']
]

class HMACTests(unittest.TestCase):

    HMAC_SHA512_LEN = 64

    def setUp(self):
        if not hasattr(self, 'hmac_sha512'):
            util.bind_all(self, util.sha2_funcs)

    def doHMAC(self, hmac_fn, key_in, msg_in):
        buf_len = self.HMAC_SHA512_LEN
        buf = create_string_buffer(buf_len)
        key, key_len = util.make_cbuffer(key_in)
        msg, msg_len = util.make_cbuffer(msg_in)
        hmac_fn(buf, key, key_len, msg, msg_len)
        return hexlify(buf)


    def test_vectors(self):

        for test in hmac_cases:
            k, msg, expected = test[0], test[1], test[2]
            result = self.doHMAC(self.hmac_sha512, k, msg)
            expected = expected.replace(' ', '')
            self.assertEqual(result[0:len(expected)], expected)


if __name__ == '__main__':
    unittest.main()