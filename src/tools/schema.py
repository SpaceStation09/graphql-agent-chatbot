from typing import Dict

class SchemaInfo:
  def __init__(self, name: str, endpoint: str, schema_data: Dict):
    self.name = name
    self.endpoint = endpoint
    self.schema = schema_data
