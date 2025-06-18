from databricks.sdk import WorkspaceClient
from databricks import sql
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_sqlalchemy_engine(catalog: str, schema: str) -> Engine:
    """
    Creates a SQLAlchemy engine for Databricks SQL Warehouse.

    Retrieves connection parameters (DATABRICKS_SERVER_HOSTNAME,
    DATABRICKS_HTTP_PATH, DATABRICKS_TOKEN) from environment variables.

    Returns:
        sqlalchemy.engine.Engine: An initialized SQLAlchemy engine.

    Raises:
        ValueError: If any of the required environment variables for host,
                    http_path, or token are not set.
    """
    server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    access_token = os.getenv("DATABRICKS_TOKEN")

    if not server_hostname:
        raise ValueError("DATABRICKS_SERVER_HOSTNAME environment variable not set.")
    if not http_path:
        raise ValueError("DATABRICKS_HTTP_PATH environment variable not set.")
    if not access_token:
        raise ValueError("DATABRICKS_TOKEN environment variable not set.")

    connection_uri = (
        f"databricks://token:{access_token}@{server_hostname}?"
        + f"http_path={http_path}&catalog={catalog}&schema={schema}"
    )

    return create_engine(connection_uri)
