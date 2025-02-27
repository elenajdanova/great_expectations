from ruamel import yaml

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py imports">
import great_expectations as gx

# </snippet>

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py get_context">
context = gx.get_context()
# </snippet>

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py datasource_yaml">
datasource_yaml = f"""
name: taxi_datasource
class_name: SimpleSqlalchemyDatasource
connection_string: <CONNECTION_STRING>

introspection:  # Each key in the "introspection" section is the name of an InferredAssetSqlDataConnector (key name "introspection" in "SimpleSqlalchemyDatasource" configuration is reserved).
    whole_table: {{}}  # Any alphanumeric key name is acceptable.
"""
# </snippet>

# Please note this override is only to provide good UX for docs and tests.
# In normal usage you'd set your path directly in the yaml above.
data_dir_path = "data"
CONNECTION_STRING = f"sqlite:///{data_dir_path}/yellow_tripdata.db"

datasource_yaml = datasource_yaml.replace("<CONNECTION_STRING>", CONNECTION_STRING)

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py test_yaml_config">
context.test_yaml_config(datasource_yaml)
# </snippet>

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py buggy_datasource_yaml">
datasource_yaml = f"""  # buggy datasource_yaml configuration
name: mis_configured_datasource
class_name: SimpleSqlalchemyDatasource
connection_string: <CONNECTION_STRING>

introspecting:  # illegal top-level key name
    whole_table: {{}}
"""
# </snippet>

datasource_yaml = datasource_yaml.replace("<CONNECTION_STRING>", CONNECTION_STRING)

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py test_yaml_config_2">
context.test_yaml_config(datasource_yaml)
# </snippet>

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py datasource_yaml_introspection">
datasource_yaml = f"""
name: taxi_datasource
class_name: SimpleSqlalchemyDatasource
connection_string: <CONNECTION_STRING>

introspection:  # Each key in the "introspection" section is the name of an InferredAssetSqlDataConnector (key name "introspection" in "SimpleSqlalchemyDatasource" configuration is reserved).
    whole_table:
        include_schema_name: true
        introspection_directives:
            include_views: true
        skip_inapplicable_tables: true  # skip and continue upon encountering introspection errors
        excluded_tables:  # a list of tables to ignore when inferring data asset_names
            - main.yellow_tripdata_sample_2019_03  # format: schema_name.table_name
"""
# </snippet>

datasource_yaml = datasource_yaml.replace("<CONNECTION_STRING>", CONNECTION_STRING)

context.test_yaml_config(datasource_yaml)

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py add_datasource">
context.add_datasource(**yaml.load(datasource_yaml))
# </snippet>

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py get_available_data_asset_names">
available_data_asset_names = context.datasources[
    "taxi_datasource"
].get_available_data_asset_names(data_connector_names="whole_table")["whole_table"]
# </snippet>

assert len(available_data_asset_names) == 2

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py datasource_yaml_tables">
datasource_yaml = f"""
name: taxi_datasource
class_name: SimpleSqlalchemyDatasource
connection_string: <CONNECTION_STRING>

tables:  # Each key in the "tables" section is a table_name (key name "tables" in "SimpleSqlalchemyDatasource" configuration is reserved).
    yellow_tripdata_sample_2019_01:  # Must match table name exactly.
        partitioners:  # Each key in the "partitioners" sub-section the name of a ConfiguredAssetSqlDataConnector (key name "partitioners" in "SimpleSqlalchemyDatasource" configuration is reserved).
            whole_table: {{}}
"""
# </snippet>

datasource_yaml = datasource_yaml.replace("<CONNECTION_STRING>", CONNECTION_STRING)

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py test_yaml_config_3">
context.test_yaml_config(datasource_yaml)
# </snippet>

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py datasource_yaml_tables_partitioners">
datasource_yaml = f"""
name: taxi_datasource
class_name: SimpleSqlalchemyDatasource
connection_string: <CONNECTION_STRING>

tables:  # Each key in the "tables" section is a table_name (key name "tables" in "SimpleSqlalchemyDatasource" configuration is reserved).
    yellow_tripdata_sample_2019_01:  # Must match table name exactly.
        partitioners:  # Each key in the "partitioners" sub-section the name of a ConfiguredAssetSqlDataConnector (key name "partitioners" in "SimpleSqlalchemyDatasource" configuration is reserved).
            whole_table:
                include_schema_name: true
                schema_name: main
                data_asset_name_prefix: taxi__
                data_asset_name_suffix: __asset
"""
# </snippet>

datasource_yaml = datasource_yaml.replace("<CONNECTION_STRING>", CONNECTION_STRING)

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py test_yaml_config_4">
context.test_yaml_config(datasource_yaml)
# </snippet>

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/how_to_introspect_and_partition_your_data/sql_database/yaml_example_gradual.py add_datasource_2">
context.add_datasource(**yaml.load(datasource_yaml))
# </snippet>

available_data_asset_names = context.datasources[
    "taxi_datasource"
].get_available_data_asset_names(data_connector_names="whole_table")["whole_table"]
assert len(available_data_asset_names) == 1
