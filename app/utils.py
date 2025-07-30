from pydantic import BaseModel, Field, create_model
from typing import List, Union

def create_item_model(formats: List[str]) -> type[BaseModel]:
    field_types = {}
    
    for field in formats:
        if any(keyword in field.lower() for keyword in ['数量', 'no', '番号']):
            field_types[field] = (int, Field(description=f"Number value for {field}"))
        elif any(keyword in field.lower() for keyword in ['金額', '単価', '価格']):
            field_types[field] = (Union[int, float], Field(description=f"Price value for {field}"))
        elif any(keyword in field.lower() for keyword in ['日付', '納期', '期日']):
            field_types[field] = (str, Field(description=f"Date value for {field}"))
        else:
            field_types[field] = (str, Field(description=f"Text value for {field}"))

    Item = create_model('Item', **field_types)
    return Item

def create_records_model(formats: List[str]) -> type[BaseModel]:
    Item = create_item_model(formats)
    
    class Records(BaseModel):
        items: List[Item] = Field(description="List of extracted items")
    
    return Records