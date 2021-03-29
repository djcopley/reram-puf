import unittest
from kem_server_copy import KEMServer

class TestKEMServerMethods(unittest.TestCase):
    
    def setUp(self):
        self.ks = KEMServer(salt_len=16, group_len=2)

    def test_hash(self):
        salt = b'\xa0\xd5\x08\xb9\x8au\xf7:\x81\x1dC\xc8J\xb7\xfd`'
        test_hash = \
            'edaf35d9626155406a6b7ad04e4661451ed90f3dc5262632ebfaaaf65a119485'
        real_hash = self.ks.hash("test", salt)
        self.assertEqual(test_hash, real_hash)
    
    def test_authenticate(self):
        client = { 
            "key" : 
            '9389203d0b9aaa2ae452626dd522b1a00bc15d481597c22bd4d3ae6b1fe4f071',
            "salt" : b'\xa0\xd5\x08\xb9\x8au\xf7:\x81\x1dC\xc8J\xb7\xfd`'
            }
        [passwd, auth] = self.ks.authenticate(client, passwd="test_passwd")
        self.assertEqual(passwd, "test_passwd")
        self.assertTrue(auth)

    def test_enroll(self):
        test_salt = self.ks.generate_salt(self.ks.salt_len)
        test_hash = self.ks.hash("password", test_salt)
        results = self.ks.enroll(user="user", passwd="password", salt=test_salt)
        user, passwd, salt = results
        self.assertEqual(user, "user")
        self.assertEqual(passwd, test_hash)
        self.assertEqual(salt, test_salt)

    def test_handshake(self):
        client = { 
            "key" : 
            '9389203d0b9aaa2ae452626dd522b1a00bc15d481597c22bd4d3ae6b1fe4f071',
            "salt" : b'\xa0\xd5\x08\xb9\x8au\xf7:\x81\x1dC\xc8J\xb7\xfd`'
            }
        result = self.ks.handshake(client, passwd="test_passwd")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()