import os
from unittest import mock

from takeoff.application_version import ApplicationVersion
from takeoff.azure.k8s_image_rolling_update import K8sImageRollingUpdate as victim
from tests.azure import takeoff_config

env_variables = {'AZURE_TENANTID': 'David',
                 'AZURE_KEYVAULT_SP_USERNAME_DEV': 'Doctor',
                 'AZURE_KEYVAULT_SP_PASSWORD_DEV': 'Who'}


@mock.patch.dict(os.environ, env_variables)
class TestK8sImageRollingUpdate(object):
    @mock.patch("takeoff.step.KeyVaultClient.vault_and_client", return_value=(None, None))
    def test_validate_schema(self, _):
        conf = {**takeoff_config(), **{'task': 'k8sImageRollingUpdate',
                                      'cluster_name': "Dave",
                                      'resource_group': "Mustaine",
                                      'deployment_name': "the-king",
                                      'image': 'docker-image'}}

        conf['azure'].update({"kubernetes_naming": "aks{env}"})
        res = victim(ApplicationVersion("dev", "v", "branch"), conf)
        assert res.config['namespace'] == 'default'