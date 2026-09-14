from pydantic import BaseModel, Field

class AddressCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=7, max_length=20)
    address_line: str = Field(min_length=5, max_length=255)
    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=100)
    postal_code: str = Field(min_length=3, max_length=20)
    country: str = Field(
        default="India",
        min_length=2,
        max_length=100,
    )
    is_default: bool = False

class AddressUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=20,
    )

    address_line: str | None = Field(
        default=None,
        min_length=5,
        max_length=255,
    )

    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None
    is_default: bool | None = None

class AddressResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    address_line: str
    city: str
    state: str
    postal_code: str
    country: str
    is_default: bool

    model_config = {
        "from_attributes": True
    }