# -*- coding: utf-8 -*-
import bandit
import py.io
import pytest
import sys

from pytest_bandit.controller import BanditItem
from pytest_bandit.errors import BanditError


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
        type='args',
        default=1,
        help='Report only issues of a given severity level or higher (1 = LOW, 2 = MEDIUM, 3 = HIGH)'
    )
    parser.addini(
        'bandit_conf_level',
        type='args',
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
        help='Output extra information like excluded and included files'
    )
    parser.addini(
        'bandit_debug',
        type='bool',
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


def pytest_sessionfinish(session, exitstatus):
    if exitstatus == 0:
        return BanditItem(session).runtest()
