import unittest

import libgadu


class GaduTestSuite(unittest.TestCase):
    def test_libgadu_version(self):
        ver = libgadu.gg_libgadu_version()
        self.assertRegexpMatches(ver, '^\d+\.\d+\.\d+$')
    def test_gg_login_params(self):
        params = libgadu.gg_login_params()
        # uin_t assignment fixed in ecf29d08
        params.uin = 12345
        self.assertEquals(params.uin, 12345)
        params.password = 'password'
        self.assertEquals(params.password, 'password')
        params.async = 1
        self.assertEquals(params.async, 1)
        params.status = libgadu.GG_STATUS_INVISIBLE
        self.assertEquals(params.status, libgadu.GG_STATUS_INVISIBLE)

if __name__ == '__main__':
    unittest.main()
