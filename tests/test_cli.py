import unittest2 as unittest
import os
from StringIO import StringIO
from argparse import Namespace

from pyfakefs import fake_filesystem_unittest
import mock

import socket

import jenkins

from jenkins_cli.cli import JenkinsCli, CliException, COLORS


class TestCliAuth(unittest.TestCase):

    @mock.patch.object(JenkinsCli, 'read_settings_from_file', return_value={})
    @mock.patch.object(jenkins.Jenkins, '__init__', return_value=None)
    def test_auth_no_file_settings(self, patched_init, read_settings_from_file):
        exep = None
        try:
            JenkinsCli.auth()
        except Exception as e:
            exep = e
        self.assertEqual(type(exep), CliException)
        self.assertEqual(patched_init.called, False)

        host = 'http://localhost:5055'
        JenkinsCli.auth(host=host)
        patched_init.assert_called_once_with(host, None, None, socket._GLOBAL_DEFAULT_TIMEOUT)
        patched_init.reset_mock()

        username = 'username'
        password = 'password'
        JenkinsCli.auth(host=host, username=username, password=password)
        patched_init.assert_called_once_with(host, username, password, socket._GLOBAL_DEFAULT_TIMEOUT)

    @mock.patch.object(JenkinsCli, 'read_settings_from_file')
    @mock.patch.object(jenkins.Jenkins, '__init__', return_value=None)
    def test_auth_has_file_settings(self, patched_init, read_settings_from_file):
        read_settings_from_file.return_value = {'username': 'username'}
        exep = None
        try:
            JenkinsCli.auth()
        except Exception as e:
            exep = e
        self.assertEqual(type(exep), CliException)
        self.assertEqual(patched_init.called, False)

        host_from_file = 'http://low.priority.com'
        username = 'username'
        password = 'password'
        read_settings_from_file.return_value = {'host': host_from_file, 'username': username, 'password': password}
        JenkinsCli.auth()
        patched_init.assert_called_once_with(host_from_file, username, password, socket._GLOBAL_DEFAULT_TIMEOUT)
        patched_init.reset_mock()

        host = 'http://localhost:5055'
        JenkinsCli.auth(host=host)
        patched_init.assert_called_once_with(host, username, password, socket._GLOBAL_DEFAULT_TIMEOUT)
        patched_init.reset_mock()


class TestCliFileUsing(fake_filesystem_unittest.TestCase):
    HOME_FILE_CONTENT = ("host =https://jenkins.host.com\n"
                         "username=   username\n"
                         "some weird settings = value = value")

    LOCAL_FILE_CONTENT = ("host=http://jenkins.localhosthost.ua\n"
                          "username=Denys\n"
                          "password=myPassword\n"
                          "other_setting=some_value")

    def setUp(self):
        self.setUpPyfakefs()

    def test_read_settings_from_file(self):
        host = "http://jenkins.host.com/"
        current_folder = os.getcwd()
        local_folder_filename = os.path.join(current_folder, JenkinsCli.SETTINGS_FILE_NAME)
        home_folder_filename = os.path.join(os.path.expanduser("~"), JenkinsCli.SETTINGS_FILE_NAME)
        self.assertFalse(os.path.exists(local_folder_filename))
        self.assertFalse(os.path.exists(home_folder_filename))

        self.fs.CreateFile(home_folder_filename,
                           contents=self.HOME_FILE_CONTENT)
        self.assertTrue(os.path.exists(home_folder_filename))
        settings_dict = JenkinsCli.read_settings_from_file()
        self.assertEqual(settings_dict,
                         {"host": 'https://jenkins.host.com',
                          "username": "username",
                          "some weird settings": "value = value"
                          })

        self.fs.CreateFile(local_folder_filename,
                           contents=self.LOCAL_FILE_CONTENT)
        self.assertTrue(os.path.exists(local_folder_filename))
        settings_dict = JenkinsCli.read_settings_from_file()
        self.assertEqual(settings_dict,
                         {"host": 'http://jenkins.localhosthost.ua',
                          "username": "Denys",
                          "password": "myPassword",
                          "other_setting": "some_value"
                          })


class TestCliCommands(unittest.TestCase):

    def setUp(self):
        self.args = Namespace(host='http://jenkins.host.com', username=None, password=None)

    @mock.patch.object(jenkins.Jenkins, 'get_jobs')
    @mock.patch('jenkins_cli.cli.print')
    def test_jobs(self, patched_print, patched_get_jobs):
        jobs = [{'name': 'Job1',
                 'color': 'blue'},
                {'name': 'Job2',
                 'color': 'red'}]
        patched_get_jobs.return_value = jobs
        JenkinsCli(self.args).jobs(self.args)
        arg1 = "%s***%s Job1" % (COLORS.get(jobs[0]['color'], jobs[0]['color']), COLORS['endcollor'])
        arg2 = "%s***%s Job2" % (COLORS.get(jobs[1]['color'], jobs[1]['color']), COLORS['endcollor'])
        patched_print.assert_has_calls([mock.call(arg1)], [mock.call(arg2)])


if __name__ == '__main__':
    unittest.main()

