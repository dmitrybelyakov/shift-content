import unittest
import os
import shutil
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from shiftcontent.db.db import Db
from shiftevent.db import Db as EventDb
from shiftcontent import services



class BaseTestCase(unittest.TestCase):
    """
    Base test case
    Provides common helpers to ease testing, including maintaining and rolling
    back test SQLite database between tests
    """

    db = None

    def setUp(self):
        """
        Set up a test
        :return: None
        """
        super().setUp()
        self.tmp

        # init services
        services.db.init(self.db_url)
        services.definition.init(self.schema_path, self.revisions_path)

        # create db now
        self.create_db()

    def tearDown(self):
        """
        Cleanup
        :return: None
        """
        super().tearDown()
        self.refresh_db()
        tests = os.path.join(os.getcwd(), 'var', 'data', 'tests')
        if os.path.exists(tests):
            shutil.rmtree(tests)

    @property
    def db_path(self):
        """ Path to test database file"""
        path = os.path.join(os.getcwd(), 'var', 'data', 'test.db')
        return path

    @property
    def db_url(self):
        """ Get test db url """
        url = 'sqlite:///{}'.format(self.db_path)
        return url

    @property
    def tmp(self):
        """
        Temp
        Returns path to temp and creates it if necessary
        :return: str
        """
        cwd = os.getcwd()
        tmp = os.path.join(cwd, 'var', 'data', 'tests', 'tmp')
        if not os.path.exists(tmp):
            os.makedirs(tmp, exist_ok=True)
        return tmp

    @property
    def schema_path(self):
        """ Get path to content schema file """
        path = os.path.join(os.getcwd(), 'tests', '_assets', 'content.yml')
        return path

    @property
    def revisions_path(self):
        """ Get path to schema revisions """
        cwd = os.getcwd()
        return os.path.join(cwd, 'var', 'data', 'tests', 'known_schemas')

    def create_db(self):
        """
        Create db
        Reads table metadata and creates all tables. And a backup for quick
        rollbacks. Will skip execution if database already exists.
        :return:
        """

        # skip if exists
        if os.path.isfile(self.db_path):
            return

        # otherwise create
        services.db.meta.create_all()
        shutil.copyfile(self.db_path, self.db_path + '.bak')

    def refresh_db(self, force=False):
        """
        Rollback database and optionally force recreation
        :param force: bool, force recreate
        :return:
        """
        if force:
            if os.path.isfile(self.db_path):
                os.remove(self.db_path)
            if os.path.isfile(self.db_path + '.bak'):
                os.remove(self.db_path + '.bak')
        else:
            shutil.copyfile(self.db_path + '.bak', self.db_path)



