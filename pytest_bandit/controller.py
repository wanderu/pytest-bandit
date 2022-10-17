import logging
import os
import pytest
import sys
from bandit.core.config import BanditConfig
from bandit.core.manager import BanditManager
from bandit.core import constants
from pytest_bandit.errors import BanditError

bandit_config_params = []

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


class BanditItem(pytest.Item):
    CACHE_KEY = 'bandit/mtimes'
    MARKER = 'bandit'

    @classmethod
    def from_parent(cls, parent, name, **kwargs):
        super_ = super()
        if hasattr(super_, "from_parent"):
            new = super_.from_parent(parent=parent, name=name)
        else:
            new = super_(name, parent)
            new.config = parent.config
        return new

    def setup(self):
        old_mtime = self.config.cache.get(
                self.CACHE_KEY, {}
            ).get(
                str(self.fspath), -1
            )
        mtime = self.fspath.mtime()
        if old_mtime == mtime:
            pytest.skip('previously passed bandit checks')

    def runtest(self):
        b_conf = BanditConfig()
        b_mgr = BanditManager(
            b_conf,
            self.config.getini('bandit_aggregate_by'),
            debug=self.config.getini('bandit_debug'),
            profile=self.config.getini('bandit_profile'),
            verbose=self.config.getini('bandit_verbose'),
            ignore_nosec=self.config.getini('bandit_ignore_nosec'))
        b_mgr.discover_files(
            self.config.getini('bandit_targets'),
            self.config.getini('bandit_recurse'),
            ', '.join(self.config.getini('bandit_exclude')))

        if not b_mgr.b_ts.tests:
            LOG.error(
                'No tests would be run, please check your targets and add '
                'recurse'
            )
            return 5

        b_mgr.run_tests()

        # trigger output of results by Bandit Manager
        sev_level = constants.RANKING[
            int(self.config.getini('bandit_sev_level'))
        ]
        conf_level = constants.RANKING[
            int(self.config.getini('bandit_conf_level'))
        ]
        sys.stdout = sys.__stdout__
        # pytest doesn't terminate the last line before invoking `runtest`
        sys.stdout.write(os.linesep)

        outputs = zip(
            list(self.config.getini('bandit_output_formats')),
            list(self.config.getini('bandit_output_files')))

        for (o_fmt, o_file) in outputs:
            o_file = open(o_file, 'w') if o_file != "screen" else sys.stdout
            b_mgr.output_results(self.config.getini('bandit_context_lines'),
                                 sev_level,
                                 conf_level,
                                 o_file,
                                 o_fmt)

        # return an exit code of 1 if there are results, 0 otherwise
        LOG.debug(sev_level)
        LOG.debug(conf_level)
        if b_mgr.results_count(
            sev_filter=sev_level, conf_filter=conf_level
        ) > 0:
            return 1

        return 0

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(BanditError):
            return excinfo.value.args[0]

        return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.fspath, None, 'bandit-check'
