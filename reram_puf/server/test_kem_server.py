import unittest
from kem_server import KEMServer

class TestKEMServerMethods(unittest.TestCase):
    
    def setUp(self):
        self.ks = KEMServer(salt_len=16, group_len=2)
        self.username = "user"
        self.password = "password"
        self.client = {}
        self.client["key"] = \
            "a8070e1351bba7400e2ad710b947d72369303a245460e8616193f55edd1ef641"
        self.client["salt"] = \
            b"\xa0\xd5\x08\xb9\x8au\xf7:\x81\x1dC\xc8J\xb7\xfd`"
        self.client["image"] = { 
            700 : [2.8, 3.5, 4.2, 4.9], 
            600 : [2.4, 3.0, 3.6, 4.2], 
            500 : [2.0, 2.5, 3.0, 3.5], 
            400 : [1.6, 2.0, 2.4, 2.8] }
        self.ks.enroll(user=self.username, passwd=self.password,
            salt=self.client["salt"], lut= self.client["image"])

    def test_hash(self):
        result = self.ks.hash(self.password, self.client["salt"])
        self.assertEqual(result, self.client["key"])

    def test_enroll(self):
        self.ks = KEMServer(salt_len=16, group_len=2)
        result = self.ks.enroll(user=self.username, passwd=self.password, 
            salt=self.client["salt"], lut=self.client["image"])
        self.assertTrue(result)
        self.assertEqual(self.ks.clients[self.username]["key"], 
            self.client["key"])
        self.assertEqual(self.ks.clients[self.username]["salt"], 
            self.client["salt"])

    def test_authenticate(self):
        [passwd, auth] = self.ks.authenticate(self.username, 
            passwd=self.password)
        self.assertEqual(passwd, self.password)
        self.assertTrue(auth)

    def test_handshake(self):
        result = self.ks.handshake(self.username, passwd=self.password,
            rand=self.client["salt"])
        # Addresses and orders generated manually using self.client key and salt
        addresses = ["00", "01", "10", "11"] 
        orders = [2, 2, 2, 0, 0, 0, 1, 3, 0, 0, 3, 2, 0, 1, 0, 3, 1, 1, 0, 1,
         2, 3, 2, 3, 2, 2, 1, 3, 1, 0, 0, 0, 0, 0, 3, 2, 0, 2, 2, 2, 3, 1, 1, 
         3, 0, 1,0, 0, 2, 3, 2, 1, 1, 0, 1, 3, 3, 1, 1, 3, 0, 2, 0, 3]
        self.assertTrue(result)
        self.assertListEqual(self.ks.addresses, addresses)
        self.assertListEqual(self.ks.orders, orders)

    def test_create_message(self):
        pass


if __name__ == "__main__":
    unittest.main()