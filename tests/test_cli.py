import unittest2 as unittest
import mock

import jenkins

from jenkins_cli.cli import JenkinsCli, CliException


class TestCliCommands(unittest.TestCase):

    def setUp(self):
        pass

    @mock.patch.object(JenkinsCli, 'read_settings_from_file', return_value={})
    @mock.patch.object(jenkins.Jenkins, '__init__')
    def test_auth_no_file_settings(self, patched_init, read_settings_from_file):
        exep = None
        try:
            JenkinsCli.auth()
        except Exception as e:
            exep = e
        self.assertEqual(type(exep), CliException)
        self.assertEqual(patched_init.called, False)

if __name__ == '__main__':
    unittest.main()

