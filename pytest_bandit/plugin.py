# -*- coding: utf-8 -*-
import bandit
import logging
import py.io
import pytest
import sys

from pytest_bandit.controller import BanditItem
from pytest_bandit.errors import BanditError

logging.getLogger("bandit.core").setLevel(logging.WARNING)
LOG = logging.getLogger(__name__)


def pytest_addoption(parser):
    group = parser.getgroup('bandit')
    group.addoption(
        '--bandit',
        action='store_true',
        default=False,
        dest='run_bandit',
        help='Run bandit'
    )
    parser.addini(
        'bandit_targets',
        type='args',
        help='Path to analyzed code'
    )
    parser.addini(
        'bandit_recurse',
        type='bool',
        default=True,
        help='Path to analyzed code'
    )
    parser.addini(
        'bandit_aggregate_by',
        type='args',
        default='vuln',
        help='Aggregate output by vulnerability (default) or by filename'
    )
    parser.addini(
        'bandit_context_lines',
        type='args',
        default=3,
        help='Maximum number of code lines to output for each issue'
    )
    parser.addini(
        'bandit_config',
        type='args',
        help='Optional config file to use for selecting plugins and overriding defaults'
    )
    parser.addini(
        'bandit_profile',
        type='args',
        default=None,
        help='Profile to use (defaults to executing all tests)'
    )
    parser.addini(
        'bandit_run_tests',
        type='args',
        help='Comma-separated list of test IDs to run'
    )
    parser.addini(
        'bandit_skip_tests',
        type='args',
        help='Comma-separated list of test IDs to skip'
    )
    parser.addini(
        'bandit_sev_level',
        default=1,
        help='Report only issues of a given severity level or higher (1 = LOW, 2 = MEDIUM, 3 = HIGH)'
    )
    parser.addini(
        'bandit_conf_level',
        default=1,
        help='Report only issues of a given confidence level or higher (1 = LOW, 2 = MEDIUM, 3 = HIGH)'
    )
    parser.addini(
        'bandit_output_format',
        type='args',
        default='screen',
        help='(CURRENTLY NOT IMPLEMENTED) Specify output format'
    )
    parser.addini(
        'bandit_msg_template',
        type='args',
        help='(CURRENTLY NOT IMPLEMENTED) Specify output message template (only usable with --format custom), \
              see CUSTOM FORMAT section for list of available values'
    )
    parser.addini(
        'bandit_verbose',
        type='bool',
        default=False,
        help='Output extra information like excluded and included files'
    )
    parser.addini(
        'bandit_debug',
        type='bool',
        default=False,
        help='Turn on debug mode'
    )
    parser.addini(
        'bandit_ignore_nosec',
        type='bool',
        help='Do not skip lines with # nosec comments'
    )
    parser.addini(
        'bandit_exclude',
        type='args',
        help='Comma-separated list of paths to exclude from scan'
    )
    parser.addini(
        'bandit_baseline',
        type='args',
        help='Path of baseline report to compare against (only JSON-formatted files are accepted)'
    )
    parser.addini(
        'bandit_ini',
        type='args',
        help='Path to a .bandit file that supplies command line arguments'
    )


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pytest

StringIO  # pyflakes, this is for re-export


if hasattr(pytest, 'hookimpl'):
    hookwrapper = pytest.hookimpl(hookwrapper=True)
else:
    hookwrapper = pytest.mark.hookwrapper

class SessionWrapper(object):
    def __init__(self, session):
        self.session = session
        self.config = self.session.config
        self.nodeid = self.session.nodeid
        if hasattr(self.session, 'testsfailed'):
            self._attr = 'testsfailed'
        else:
            self._attr = '_testsfailed'

    @property
    def testsfailed(self):
        return getattr(self.session, self._attr)

    @testsfailed.setter
    def testsfailed(self, value):
        setattr(self.session, self._attr, value)

    @property
    def shouldfail(self):
        return getattr(self.session, 'shouldfail')

    @shouldfail.setter
    def shouldfail(self, value):
        # Only set when currently False
        if not self.shouldfail:
            setattr(self.session, 'shouldfail', value)


@hookwrapper
def pytest_runtestloop(session):
    yield
    compat_session = SessionWrapper(session)
    bandit_failures = BanditItem(compat_session).runtest()
    LOG.debug(compat_session.shouldfail)
    compat_session.testsfailed += bandit_failures
    compat_session.shouldfail = bool(bandit_failures)
    LOG.debug(compat_session.shouldfail)
