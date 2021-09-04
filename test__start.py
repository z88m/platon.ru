import unittest

from test_000_loginForm import TestLoginForm

tests_000 = unittest.TestLoader().loadTestsFromTestCase(TestLoginForm)

test_mw = unittest.TestSuite([tests_000])

result = unittest.TextTestRunner(verbosity=2).run(test_mw)

if result.wasSuccessful():
    exit(0)
else:
    exit(1)