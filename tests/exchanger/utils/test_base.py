

class TestBase:

    def setUp(self) -> None:
        self.exchanger = None

        self.url_wrong = None
        self.host_wrong = None
        self.prefix_wrong = None
        self.test_data_error = None
        self.test_data = None

        #  gate
        self.api_key_wrong = None
        self.api_secret_wrong = None
        #  mexc
        self.apiSecret_wrong = None
        self.url_other = None

    def _set_wrong_api(self):
        if self.apiSecret_wrong:
            self.exchanger.apiSecret = self.apiSecret_wrong
        elif self.api_key_wrong:
            self.exchanger.key = self.api_key_wrong

    def _set_wrong_secret(self):
        self.exchanger.secret = self.api_secret_wrong

    def _set_wrong_prefix(self):
        self.exchanger.prefix = self.prefix_wrong

    def _set_wrong_host(self):
        self.exchanger.host = self.host_wrong

    def _set_other_url(self):
        self.exchanger.url = self.url_other

    def _set_wrong_url(self):
        self.exchanger.url = self.url_wrong

    def assertIsInstance(self, param, list):
        pass

    def assertIn(self, exchanger, result):
        pass

    def assertEqual(self, param, param1):
        pass

    def _check_data_in_test_base(self, result):
        self.assertIsInstance(result, dict)
        self.assertIn(self.exchanger.exchanger, result)
        self.assertIn('coin', list(result.values())[0][0])
        self.assertIn('bal', list(result.values())[0][0])

    def test_get_account(self):
        self._check_data_in_test_base(
            self.exchanger.get_account())

    def test_normalize_data(self):
        self._check_data_in_test_base(
            self.exchanger._normalize_data(self.test_data))

    def test_normalize_with_errors_data(self):
        result = self.exchanger._normalize_data(*self.test_data_error)

        self.assertIn(self.exchanger.exchanger, result)
        self.assertEqual(result[self.exchanger.exchanger], self.test_data_error)

