import unittest
from pyspark_streaming_deployment.create_databricks_secrets import (
    CreateDatabricksSecrets as victim
)


class TestCreateDatabricksSecrets(unittest.TestCase):
    def test_scope_exists(self):
        scopes = {"scopes": [{"name": "foo"}, {"name": "bar"}]}

        assert victim._scope_exists(scopes, "foo")
        assert not victim._scope_exists(scopes, "foobar")

    def test_filter_ids(self):
        ids = ["app-foo-key1", "appfoo-key2", "app-bar-key3", "app-key4"]

        filtered = [
            _.databricks_secret_key for _ in victim._filter_keyvault_ids(ids, "app")
        ]
        assert len(filtered) == 3
        assert all(_ in filtered for _ in ("foo-key1", "bar-key3", "key4"))

        filtered = [
            _.databricks_secret_key for _ in victim._filter_keyvault_ids(ids, "app-foo")
        ]
        assert len(filtered) == 1
        assert "key1" in filtered
