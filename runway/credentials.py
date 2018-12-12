from enum import Enum, auto

from typing import Dict

from runway.KeyVaultSecrets import KeyVaultSecrets, Secret


class CommonCredentials(Enum):
    subscription_id = auto()
    azure_username = auto()
    azure_password = auto()
    azure_databricks_host = auto()
    azure_databricks_token = auto()
    azure_shared_blob_username = auto()
    azure_shared_blob_password = auto()
    registry_username = auto()
    registry_password = auto()
    artifact_store_username = auto()
    artifact_store_password = auto()
    artifact_store_index_url = auto()
    artifact_store_upload_url = auto()


def find_secret(secret_key, secrets: Dict[str, Secret]):
    if secret_key not in secrets:
        raise ValueError(f"Could not find required key {secret_key}")
    return secrets[secret_key].val


def common_credentials(dtap):
    secrets = KeyVaultSecrets.get_keyvault_secrets(dtap, 'common')
    indexed = {_.key: _ for _ in secrets}
    # Keyvault does not support _ and python does not support -, hence the 'replace'
    return {_: find_secret(_.name.replace('_', '-'), indexed) for _ in CommonCredentials}
