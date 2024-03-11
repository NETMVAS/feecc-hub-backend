import pydantic

from src.feecc_workbench.utils import time_execution
from src.database.database import BaseMongoDbWrapper
from src.database.models import ProductionSchema


class ProdSchemaWrapper:
    collection = "productionSchemas"

    @time_execution
    def get_all_schemas(self) -> list[ProductionSchema]:
        """get all production schemas"""
        schema_data = BaseMongoDbWrapper.read(collection=self.collection, projection={"_id": 0})
        return [pydantic.TypeAdapter.validate_python(ProductionSchema, schema) for schema in schema_data]

    @time_execution
    def get_schema_by_id(self, schema_id: str) -> ProductionSchema:
        """get the specified production schema"""
        filters = {"schema_id": schema_id}
        projection = {"_id": 0}
        target_schema = BaseMongoDbWrapper.read(collection=self.collection, filters=filters, projection=projection)

        if target_schema is None:
            raise ValueError(f"Schema {schema_id} not found")

        return pydantic.TypeAdapter.validate_python(ProductionSchema, target_schema)


prod_schema_wrapper = ProdSchemaWrapper()
