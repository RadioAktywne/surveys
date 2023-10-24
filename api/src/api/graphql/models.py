from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseModel(PydanticBaseModel):
    """Base class for models that can be serialized to JSON."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )


class LoginRequest(BaseModel):
    """Login request."""

    username: str = Field(
        ...,
        title="Username",
        description="Username of the user.",
    )
    password: str = Field(
        ...,
        title="Password",
        description="Password of the user.",
    )


class Tokens(BaseModel):
    """Authentication tokens."""

    access: str = Field(
        ...,
        title="Access Token",
        description="JWT access token.",
    )
    refresh: str = Field(
        ...,
        title="Refresh Token",
        description="JWT refresh token.",
    )


class LoginResponse(BaseModel):
    """Login response."""

    tokens: Tokens = Field(
        ...,
        title="Authentication Tokens",
        description="Authentication tokens.",
    )


class ListFormsRequest(BaseModel):
    """Form pager query."""

    limit: int | None = Field(
        None,
        title="Form Pager Query Limit",
        description="Number of forms per page.",
    )
    start: int | None = Field(
        None,
        title="Form Pager Query Start",
        description="Offset of the first form in the page.",
    )


class FormPagerEntry(BaseModel):
    """Form pager entry."""

    id: str = Field(
        ...,
        title="Form ID",
        description="ID of the form.",
    )
    title: str = Field(
        ...,
        title="Form Title",
        description="Title of the form.",
    )


class FormPager(BaseModel):
    """Form pager."""

    entries: list[FormPagerEntry] = Field(
        ...,
        title="Form Pager Entries",
        description="Entries of the form pager.",
    )
    total: int = Field(
        ...,
        title="Form Pager Total",
        description="Total number of forms.",
    )
    limit: int = Field(
        ...,
        title="Form Pager Limit",
        description="Number of forms per page.",
    )
    start: int = Field(
        ...,
        title="Form Pager Start",
        description="Offset of the first form in the page.",
    )


class ListFormsResponse(BaseModel):
    """List forms response."""

    pager: FormPager = Field(
        ...,
        title="Form Pager",
        description="Form pager.",
    )


class GetFormRequest(BaseModel):
    """Get form request."""

    id: str = Field(
        ...,
        title="Form ID",
        description="ID of the form.",
    )


class FormFieldOption(BaseModel):
    """Form field option."""

    id: str = Field(
        ...,
        title="Option ID",
        description="ID of the option.",
    )
    title: str | None = Field(
        ...,
        title="Option Title",
        description="Title of the option.",
    )
    value: str = Field(
        ...,
        title="Option Value",
        description="Value of the option.",
    )


class FormField(BaseModel):
    """Form field."""

    id: str = Field(
        ...,
        title="Field ID",
        description="ID of the field.",
    )
    idx: int | None = Field(
        ...,
        title="Field Index",
        description="Index of the field.",
    )
    title: str = Field(
        ...,
        title="Field Title",
        description="Title of the field.",
    )
    type: str = Field(
        ...,
        title="Field Type",
        description="Type of the field.",
    )
    description: str = Field(
        ...,
        title="Field Description",
        description="Description of the field.",
    )
    required: bool = Field(
        ...,
        title="Field Required",
        description="Whether the field is required.",
    )
    default_value: str | None = Field(
        ...,
        title="Field Default Value",
        description="Default value of the field.",
    )
    options: list[FormFieldOption] = Field(
        ...,
        title="Field Options",
        description="Options of the field.",
    )


class Form(BaseModel):
    """Form data."""

    id: str = Field(
        ...,
        title="Form ID",
        description="ID of the form.",
    )
    title: str = Field(
        ...,
        title="Form Title",
        description="Title of the form.",
    )
    fields: list[FormField] = Field(
        ...,
        title="Form Fields",
        description="Fields of the form.",
    )


class GetFormResponse(BaseModel):
    """Get form response."""

    form: Form = Field(
        ...,
        title="Form",
        description="Form.",
    )


class Submission(BaseModel):
    """Submission data."""

    id: str = Field(
        ...,
        title="Submission ID",
        description="ID of the submission.",
    )
    percentage_complete: float = Field(
        ...,
        title="Submission Percentage Complete",
        description="Percentage of the submission that is complete.",
    )


class Device(BaseModel):
    """Device data."""

    type: str = Field(
        ...,
        title="Device Type",
        description="Type of the device.",
    )
    name: str = Field(
        ...,
        title="Device Name",
        description="Name of the device.",
    )


class SubmissionStartData(BaseModel):
    """Submission start data."""

    token: str = Field(
        ...,
        title="Submission Token",
        description="Token of the submission.",
    )
    device: Device = Field(
        ...,
        title="Submission Device",
        description="Device of the submission.",
    )


class StartSubmissionRequest(BaseModel):
    """Start submission request."""

    form: str = Field(
        ...,
        title="Submission Form",
        description="ID of the form.",
    )
    submission: SubmissionStartData = Field(
        ...,
        title="Submission Data",
        description="Data of the submission.",
    )


class StartSubmissionResponse(BaseModel):
    """Start submission response."""

    submission: Submission = Field(
        ...,
        title="Submission",
        description="Submission.",
    )


class SubmissionFieldData(BaseModel):
    """Submission field data."""

    token: str = Field(
        ...,
        title="Submission Token",
        description="Token of the submission.",
    )
    field: str = Field(
        ...,
        title="Submission Field",
        description="ID of the field.",
    )
    data: str = Field(
        ...,
        title="Submission Data",
        description="JSON-encoded data of the field.",
    )


class SubmitFieldRequest(BaseModel):
    """Submit field request."""

    submission: str = Field(
        ...,
        title="Submission",
        description="ID of the submission.",
    )
    field: SubmissionFieldData = Field(
        ...,
        title="Submission Field",
        description="Data of the field.",
    )


class SubmitFieldResponse(BaseModel):
    """Submit field response."""

    submission: Submission = Field(
        ...,
        title="Submission",
        description="Submission.",
    )


class FinishSubmissionRequest(BaseModel):
    """Finish submission request."""

    submission: str = Field(
        ...,
        title="Submission",
        description="ID of the submission.",
    )


class FinishSubmissionResponse(BaseModel):
    """Finish submission response."""

    submission: Submission = Field(
        ...,
        title="Submission",
        description="Submission.",
    )
