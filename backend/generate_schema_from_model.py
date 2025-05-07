from typing import Type, Optional

from pydantic import create_model, Field
from sqlmodel import SQLModel


def generate_schemas_from_model(model: Type[SQLModel], output_file="schemas.py"):
    # Modelin alanlarını al
    fields = {}
    for field_name, field_info in model.model_fields.items():
        # Alanın türünü ve varsayılan değerini al
        field_type = field_info.annotation
        default_value = ... if field_info.is_required() else None

        # Field sınıfını kullanarak alanı tanımla
        fields[field_name] = (field_type, Field(default=default_value))

    # Create şeması
    CreateSchema = create_model(f"{model.__name__}Create", **fields)

    # Update şeması
    UpdateSchema = create_model(
        f"{model.__name__}Update",
        **{k: (Optional[v.annotation], Field(default=None)) for k, v in CreateSchema.model_fields.items()}
    )

    # Read şeması için id'yi ayrı olarak ekle
    if "id" in fields:
        fields.pop("id")  # fields'den id'yi çıkar

    fields["id"] = (int, Field(default=..., description="Primary key"))

    ReadSchema = create_model(
        f"{model.__name__}Read",
        **fields
    )
    ReadSchema.model_config = {"from_attributes": True}

    # Şemaları bir dosyaya yaz
    with open(output_file, "w") as f:
        f.write("# Otomatik olarak oluşturulan şemalar\n")
        f.write("from typing import Optional\n")
        f.write("from datetime import date\n")
        f.write("from pydantic import BaseModel, Field\n\n")

        # Create şemasını yaz
        f.write(f"class {CreateSchema.__name__}(BaseModel):\n")
        for field_name, field_info in CreateSchema.model_fields.items():
            default = "..." if field_info.is_required() else "None"
            f.write(f"    {field_name}: {field_info.annotation.__name__} = Field(default={default})\n")
        f.write("\n")

        # Update şemasını yaz
        f.write(f"class {UpdateSchema.__name__}(BaseModel):\n")
        for field_name, field_info in UpdateSchema.model_fields.items():
            f.write(f"    {field_name}: Optional[{field_info.annotation.__name__}] = Field(default=None)\n")
        f.write("\n")

        # Read şemasını yaz
        f.write(f"class {ReadSchema.__name__}(BaseModel):\n")
        for field_name, field_info in ReadSchema.model_fields.items():
            default = "..." if field_info.is_required() else "None"
            f.write(f"    {field_name}: {field_info.annotation.__name__} = Field(default={default})\n")
        f.write("\n")
        f.write("    model_config = {\n")
        f.write('        "from_attributes": True\n')
        f.write("    }\n")

    print(f"Şemalar başarıyla '{output_file}' dosyasına yazıldı.")
