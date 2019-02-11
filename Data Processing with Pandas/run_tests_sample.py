import unittest

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests_sample')
    unittest.TextTestRunner().run(suite)
