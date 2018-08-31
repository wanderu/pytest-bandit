import logging
import pytest
import sys
from bandit.core.config import BanditConfig
from bandit.core.manager import BanditManager
from bandit.core import constants
from pytest_bandit.errors import BanditError

bandit_config_params = []

LOG = logging.getLogger(__name__)


class BanditItem(pytest.Item):
    CACHE_KEY = 'bandit/mtimes'

    def __init__(self, session):
        super().__init__('bandit', session)
        self.add_marker('bandit')
        self.config = session.config

    def setup(self):
        old_mtime = self.config.cache.get(self.CACHE_KEY, {}).get(str(self.fspath), -1)
        mtime = self.fspath.mtime()
        if old_mtime == mtime:
            pytest.skip('previously passed bandit checks')

    def runtest(self):
        b_conf = BanditConfig()
        b_mgr = BanditManager(b_conf,
                              self.config.getini('bandit_aggregate_by'),
                              self.config.getini('bandit_debug'),
                              profile=self.config.getini('bandit_profile'),
                              verbose=self.config.getini('bandit_verbose'),
                              ignore_nosec=self.config.getini('bandit_ignore_nosec'))
        b_mgr.discover_files(self.config.getini('bandit_targets'),
                             self.config.getini('bandit_recurse'),
                             self.config.getini('bandit_exclude'))
        b_mgr.run_tests()

        LOG.debug(b_mgr.b_ma)
        LOG.debug(b_mgr.metrics)

        # trigger output of results by Bandit Manager
        sev_level = constants.RANKING[self.config.getini('bandit_sev_level') - 1]
        conf_level = constants.RANKING[self.config.getini('bandit_conf_level') - 1]
        sys.stdout = sys.__stdout__
        b_mgr.output_results(self.config.getini('bandit_context_lines'),
                             sev_level,
                             conf_level,
                             sys.stdout,
                             'screen')

        # return an exit code of 1 if there are results, 0 otherwise
        if b_mgr.results_count(sev_filter=sev_level, conf_filter=conf_level) > 0:
            return 1
        else:
            return 0

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(BanditError):
            return excinfo.value.args[0]
        else:
            return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.fspath, None, 'bandit-check'
