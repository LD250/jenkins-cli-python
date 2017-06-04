import unittest2 as unittest
import os
from argparse import Namespace
from xml.etree import ElementTree
from datetime import datetime, timedelta

from pyfakefs import fake_filesystem_unittest
import mock

import socket

import jenkins

from jenkins_cli.cli import JenkinsCli, CliException, STATUSES_COLOR, ENDCOLLOR

GIT_SCM_XML = """<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<project>\n  <actions/>\n  <description></description>\n  <keepDependencies>false</keepDependencies>\n  <properties/>\n  <scm class="hudson.plugins.git.GitSCM" plugin="git@2.4.2">\n    <configVersion>2</configVersion>\n    <userRemoteConfigs>\n      <hudson.plugins.git.UserRemoteConfig>\n        <url>https://github.com/LD250/jenkins-cli-python/</url>\n      </hudson.plugins.git.UserRemoteConfig>\n    </userRemoteConfigs>\n    <branches>\n      <hudson.plugins.git.BranchSpec>\n        <name>cli-tests</name>\n      </hudson.plugins.git.BranchSpec>\n    </branches>\n    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>\n    <submoduleCfg class="list"/>\n    <extensions/>\n  </scm>\n  <canRoam>true</canRoam>\n  <disabled>false</disabled>\n  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>\n  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>\n  <triggers/>\n  <concurrentBuild>false</concurrentBuild>\n  <builders>\n    <hudson.tasks.Shell>\n      <command></command>\n    </hudson.tasks.Shell>\n    <jenkins.plugins.shiningpanda.builders.VirtualenvBuilder plugin="shiningpanda@0.22">\n      <pythonName>System-CPython-2.7</pythonName>\n      <home></home>\n      <clear>true</clear>\n      <systemSitePackages>false</systemSitePackages>\n      <nature>shell</nature>\n      <command>pip install -U pip\npip install -U setuptools\npip install -U wheel\npip install -r requirements.txt\npip list -o\n\nflake8 jenkins_cli\npython setup.py test</command>\n      <ignoreExitCode>false</ignoreExitCode>\n    </jenkins.plugins.shiningpanda.builders.VirtualenvBuilder>\n  </builders>\n  <publishers/>\n  <buildWrappers/>\n</project>
"""

HG_SCM_XML = """<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<project>\n  <actions/>\n  <description></description>\n  <keepDependencies>false</keepDependencies>\n  <properties/>\n  <scm class="hudson.plugins.mercurial.MercurialSCM" plugin="mercurial@1.54">\n    <modules></modules>\n    <revisionType>BRANCH</revisionType>\n    <revision>v123</revision>\n    <clean>false</clean>\n    <credentialsId></credentialsId>\n    <disableChangeLog>false</disableChangeLog>\n  </scm>\n  <canRoam>true</canRoam>\n  <disabled>false</disabled>\n  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>\n  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>\n  <triggers/>\n  <concurrentBuild>false</concurrentBuild>\n  <builders/>\n  <publishers/>\n  <buildWrappers/>\n</project>
"""

EMPTY_SCM_XML = """<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<project>\n  <actions/>\n  <description></description>\n  <keepDependencies>false</keepDependencies>\n  <properties/>\n  <scm class="hudson.scm.NullSCM"/>\n  <canRoam>true</canRoam>\n  <disabled>false</disabled>\n  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>\n  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>\n  <triggers/>\n  <concurrentBuild>false</concurrentBuild>\n  <builders/>\n  <publishers/>\n  <buildWrappers/>\n</project>
"""

TS = 1456870299


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
    HOME_FILE_CONTENT = ("[DEFAULT]\n"
                         "host =https://jenkins.host.com\n"
                         "username=   username\n"
                         "some weird settings = value = value")

    LOCAL_FILE_CONTENT = ("[DEFAULT]\n"
                          "host=http://jenkins.localhosthost.ua\n"
                          "username=Denys\n"
                          "password=myPassword\n"
                          "other_setting=some_value")

    MULTIENV_FILE_CONTENT = ("[DEFAULT]\n"
                             "host =https://jenkins.host.com\n"
                             "username=   username\n"
                             "some default settings = value = value\n"
                             "\n"
                             "[alternative]\n"
                             "host=http://jenkins.localhosthost.ua\n"
                             "username=Denys\n"
                             "password=myPassword\n"
                             "other_setting=some_value"
                             )

    def setUp(self):
        self.setUpPyfakefs()

    def test_read_settings_from_file(self):
        current_folder = os.getcwd()
        local_folder_filename = os.path.join(current_folder, JenkinsCli.SETTINGS_FILE_NAME)
        home_folder_filename = os.path.join(os.path.expanduser("~"), JenkinsCli.SETTINGS_FILE_NAME)
        self.assertFalse(os.path.exists(local_folder_filename))
        self.assertFalse(os.path.exists(home_folder_filename))

        self.fs.CreateFile(home_folder_filename,
                           contents=self.HOME_FILE_CONTENT)
        self.assertTrue(os.path.exists(home_folder_filename))
        settings_dict = JenkinsCli.read_settings_from_file(environment=None)
        self.assertEqual(settings_dict,
                         {"host": 'https://jenkins.host.com',
                          "username": "username",
                          "some weird settings": "value = value"
                          })

        self.fs.CreateFile(local_folder_filename,
                           contents=self.LOCAL_FILE_CONTENT)
        self.assertTrue(os.path.exists(local_folder_filename))
        settings_dict = JenkinsCli.read_settings_from_file(environment=None)
        self.assertEqual(settings_dict,
                         {"host": 'http://jenkins.localhosthost.ua',
                          "username": "Denys",
                          "password": "myPassword",
                          "other_setting": "some_value"
                          })

    def test_read_settings_from_file_alt_environment(self):
        # make sure we are in the fake fs
        current_folder = os.getcwd()
        local_folder_filename = os.path.join(current_folder, JenkinsCli.SETTINGS_FILE_NAME)
        self.assertFalse(os.path.exists(local_folder_filename))

        # create the fake config file
        self.fs.CreateFile(local_folder_filename,
                           contents=self.MULTIENV_FILE_CONTENT)
        self.assertTrue(os.path.exists(local_folder_filename))

        # read the config from the file
        settings_dict = JenkinsCli.read_settings_from_file(environment='alternative')

        # test and that the alternative environment is used, with the missing
        #   values being provided from the DEFAULT environmtne
        self.assertEqual(settings_dict,
                         {"host": 'http://jenkins.localhosthost.ua',
                          "username": "Denys",
                          "password": "myPassword",
                          "other_setting": "some_value",
                          'some default settings': 'value = value'
                          })


class TestCliCommands(unittest.TestCase):

    def setUp(self):
        self.args = Namespace(host='http://jenkins.host.com', username=None, password=None, environment=None)
        self.print_patcher = mock.patch('jenkins_cli.cli.print')
        self.patched_print = self.print_patcher.start()

    def tearDown(self):
        self.print_patcher.stop()

    @mock.patch.object(jenkins.Jenkins, 'get_jobs')
    def test_jobs(self, patched_get_jobs):
        jobs = [{'name': 'Job1',
                 'color': 'blue'},
                {'name': 'Job2',
                 'color': 'disabled'}]
        patched_get_jobs.return_value = jobs
        self.args.a = False
        JenkinsCli(self.args).jobs(self.args)
        arg1 = "%sS..%s Job1" % (STATUSES_COLOR[jobs[0]['color']]['color'], ENDCOLLOR)
        arg2 = "%sD..%s Job2" % (STATUSES_COLOR[jobs[1]['color']]['color'], ENDCOLLOR)
        self.patched_print.assert_has_calls([mock.call(arg1)], [mock.call(arg2)])
        self.patched_print.reset_mock()
        self.args.a = True
        JenkinsCli(self.args).jobs(self.args)
        self.patched_print.assert_called_once_with(arg1)

    @mock.patch.object(jenkins.Jenkins, 'get_queue_info')
    def test_queue(self, patched_get_queue_info):
        queue_list = [
            {u'task': {u'url': u'http://your_url/job/my_job/', u'color': u'aborted_anime', u'name': u'my_job'},
             u'stuck': False,
             u'actions': [{u'causes': [{u'shortDescription': u'Started by timer'}]}],
             u'why': u'Build #2,532 is already in progress (ETA:10 min)'},
            {u'task': {u'url': u'http://your_url/job/my_job/', u'color': u'aborted_anime', u'name': u'my_job2'},
             u'stuck': False,
             u'actions': [{u'causes': [{u'shortDescription': u'Started by timer'}]}],
             u'why': u'Build #234 is already in progress (ETA:10 min)'}
        ]
        patched_get_queue_info.return_value = []
        JenkinsCli(self.args).queue(self.args)
        self.patched_print.assert_called_once_with(JenkinsCli.QUEUE_EMPTY_TEXT)
        patched_get_queue_info.reset_mock()
        patched_get_queue_info.return_value = queue_list
        JenkinsCli(self.args).queue(self.args)
        args = ["%s %s" % (job['task']['name'], job['why']) for job in queue_list]
        self.patched_print.assert_has_calls([mock.call(args[0])], [mock.call(args[1])])

    @mock.patch.object(jenkins.Jenkins, 'get_job_name')
    def test_check_job(self, patched_get_job_name):
        patched_get_job_name.return_value = None
        exep = None
        try:
            JenkinsCli(self.args)._check_job('Job1')
        except Exception as e:
            exep = e
        self.assertEqual(type(exep), CliException)

        patched_get_job_name.return_value = 'Job1'
        job_name = JenkinsCli(self.args)._check_job('Job1')
        self.assertEqual(job_name, 'Job1')

    def test_get_scm_name_and_node(self):
        root = ElementTree.fromstring(GIT_SCM_XML.encode('utf-8'))
        name, branch_node = JenkinsCli(self.args)._get_scm_name_and_node(root)
        self.assertEqual(name, 'Git')
        self.assertEqual(branch_node.text, 'cli-tests')

        root = ElementTree.fromstring(HG_SCM_XML.encode('utf-8'))
        name, branch_node = JenkinsCli(self.args)._get_scm_name_and_node(root)
        self.assertEqual(name, 'Mercurial')
        self.assertEqual(branch_node.text, 'v123')

        root = ElementTree.fromstring(EMPTY_SCM_XML.encode('utf-8'))
        name, branch_node = JenkinsCli(self.args)._get_scm_name_and_node(root)
        self.assertEqual(name, 'UnknownVCS')
        self.assertEqual(branch_node, None)

    @mock.patch.object(jenkins.Jenkins, 'get_job_config')
    @mock.patch.object(jenkins.Jenkins, 'get_job_info')
    @mock.patch.object(jenkins.Jenkins, 'get_job_name', return_value='Job1')
    def test_info(self, patched_get_job_name, patched_get_job_info, patched_get_job_config):
        self.args.job_name = "Job1"
        patched_get_job_info.return_value = {}
        patched_get_job_config.return_value = EMPTY_SCM_XML
        JenkinsCli(self.args).info(self.args)
        arg = JenkinsCli.INFO_TEMPLATE % ('Not Built', 'Not Built', 'Not Built', 'Not Built', 'No', 'UnknownVCS', 'Unknown branch')
        self.patched_print.assert_called_once_with(arg)
        self.patched_print.reset_mock()

        job_info = {'lastBuild': {'fullDisplayName': 'FDN (cur)',
                                  'result': 'Done',
                                  'timestamp': TS * 1000,
                                  'building': True},
                    'lastSuccessfulBuild': {'fullDisplayName': 'FDN (last)'}}
        patched_get_job_info.return_value = job_info
        patched_get_job_config.return_value = GIT_SCM_XML
        JenkinsCli(self.args).info(self.args)
        arg = JenkinsCli.INFO_TEMPLATE % ('FDN (cur)', 'Done', 'FDN (last)', datetime.fromtimestamp(TS), 'Yes', 'Git', 'cli-tests')
        self.patched_print.assert_called_once_with(arg)
        self.patched_print.reset_mock()

        job_info['building'] = False
        patched_get_job_info.return_value = job_info
        patched_get_job_config.return_value = HG_SCM_XML
        JenkinsCli(self.args).info(self.args)
        arg = JenkinsCli.INFO_TEMPLATE % ('FDN (cur)', 'Done', 'FDN (last)', datetime.fromtimestamp(TS), 'Yes', 'Mercurial', 'v123')
        self.patched_print.assert_called_once_with(arg)

    @mock.patch.object(jenkins.Jenkins, 'reconfig_job')
    @mock.patch.object(jenkins.Jenkins, 'get_job_config')
    @mock.patch.object(jenkins.Jenkins, 'get_job_name', return_value='Job1')
    def test_setbranch(self, patched_get_job_name, patched_get_job_config, patched_reconfig_job):
        patched_get_job_config.return_value = EMPTY_SCM_XML
        self.args.job_name = 'Job1'
        self.args.branch_name = 'b1'
        JenkinsCli(self.args).setbranch(self.args)
        self.assertFalse(patched_reconfig_job.called)
        self.patched_print.assert_called_once_with("Cannot set branch name")
        self.patched_print.reset_mock()

        patched_get_job_config.return_value = GIT_SCM_XML
        JenkinsCli(self.args).setbranch(self.args)
        self.assertEqual(patched_reconfig_job.call_args[0][0], 'Job1')
        self.assertIn('b1', str(patched_reconfig_job.call_args[0][1]))
        self.assertNotIn('cli-tests', patched_reconfig_job.call_args[1])
        self.patched_print.assert_called_once_with("Done")
        patched_reconfig_job.reset_mock()
        self.patched_print.reset_mock()

        patched_get_job_config.return_value = HG_SCM_XML
        JenkinsCli(self.args).setbranch(self.args)
        self.assertEqual(patched_reconfig_job.call_args[0][0], 'Job1')
        self.assertIn('b1', str(patched_reconfig_job.call_args[0][1]))
        self.assertNotIn('v123', patched_reconfig_job.call_args[1])
        self.patched_print.assert_called_once_with("Done")
        patched_reconfig_job.reset_mock()
        self.patched_print.reset_mock()

    @mock.patch.object(jenkins.Jenkins, 'build_job', return_value=None)
    @mock.patch.object(jenkins.Jenkins, 'get_job_name', return_value='Job1')
    def test_start(self, patched_job_name, patched_build_job):
        self.args.job_name = ['Job1']
        JenkinsCli(self.args).start(self.args)
        patched_build_job.assert_called_once_with('Job1')
        self.patched_print.assert_called_once_with("%s: %s" % ('Job1', 'started'))

    @mock.patch.object(jenkins.Jenkins, 'stop_build', return_value=None)
    @mock.patch.object(jenkins.Jenkins, 'get_job_info')
    @mock.patch.object(jenkins.Jenkins, 'get_job_name', return_value='Job1')
    def test_stop(self, patched_job_name, patched_job_info, patched_stop_build):
        self.args.job_name = 'Job1'
        patched_job_info.return_value = {'lastBuild': {}}
        JenkinsCli(self.args).stop(self.args)
        self.assertFalse(patched_stop_build.called)
        self.patched_print.assert_called_once_with("%s job is not running" % 'Job1')
        self.patched_print.reset_mock()

        patched_job_info.return_value = {'lastBuild': {'building': True, 'number': 22}}
        JenkinsCli(self.args).stop(self.args)
        patched_stop_build.assert_called_once_with('Job1', 22)
        self.patched_print.assert_called_once_with("Job1: stopped")

    @mock.patch('jenkins_cli.cli.time', return_value=0)
    @mock.patch.object(jenkins.Jenkins, 'get_jobs')
    @mock.patch.object(jenkins.Jenkins, 'get_build_info')
    @mock.patch.object(jenkins.Jenkins, 'get_job_info')
    @mock.patch.object(jenkins.Jenkins, 'get_job_name', side_effect=lambda j: j)
    def test_building(self, patched_job_name, patched_job_info, patched_build_info, get_jobs_patched, patched_time):
        get_jobs_patched.return_value = [{'name': 'Job1', 'color': 'blue'}]
        JenkinsCli(self.args).building(self.args)
        self.assertFalse(patched_job_info.called)
        self.assertFalse(patched_build_info.called)
        self.patched_print.assert_called_once_with("Nothing is being built now")
        self.patched_print.reset_mock()

        get_jobs_patched.return_value = [{'name': 'Job1', 'color': 'blue_anime'},
                                         {'name': 'Job5', 'color': 'red_anime'}]
        patched_job_info.return_value = {'lastBuild': {}}
        JenkinsCli(self.args).building(self.args)
        self.assertFalse(patched_build_info.called)
        self.patched_print.assert_has_calls([mock.call("Job1 estimated time left unknown")],
                                            [mock.call("Job5 estimated time left unknown")])
        self.patched_print.reset_mock()

        patched_job_info.return_value = {'lastBuild': {'number': 2}}

        def info_side_effect(name, number):
            return {'timestamp': TS * 1000, 'estimatedDuration': 0, 'fullDisplayName': 'FDN ' + name}

        patched_build_info.side_effect = info_side_effect
        JenkinsCli(self.args).building(self.args)
        self.patched_print.assert_has_calls([mock.call("FDN Job1 estimated time left %s" % timedelta(seconds=TS))],
                                            [mock.call("FDN Job5 estimated time left %s" % timedelta(seconds=TS))])


if __name__ == '__main__':
    unittest.main()
