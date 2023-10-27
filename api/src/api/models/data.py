import json
from datetime import date
from typing import Annotated, Any, Literal

from pydantic import Field, field_validator

from api.models.base import SerializableModel


class FormPagerEntry(SerializableModel):
    """Form pager entry."""

    id: str = Field(
        ...,
        title="FormPagerEntry.ID",
        description="ID of the form.",
    )
    title: str = Field(
        ...,
        title="FormPagerEntry.Title",
        description="Title of the form.",
    )


class FormPager(SerializableModel):
    """Form pager."""

    entries: list[FormPagerEntry] = Field(
        ...,
        title="FormPager.Entries",
        description="Entries of the form pager.",
    )
    total: int = Field(
        ...,
        title="FormPager.Total",
        description="Total number of forms.",
    )
    limit: int = Field(
        ...,
        title="FormPager.Limit",
        description="Number of forms per page.",
    )
    start: int = Field(
        ...,
        title="FormPager.Start",
        description="Offset of the first form in the page.",
    )


class CheckboxFormFieldOption(SerializableModel):
    """Checkbox form field option."""

    id: str = Field(
        ...,
        title="CheckboxFormFieldOption.ID",
        description="ID of the field option.",
    )
    title: str | None = Field(
        ...,
        title="CheckboxFormFieldOption.Title",
        description="Title of the field option.",
    )
    value: str = Field(
        ...,
        title="CheckboxFormFieldOption.Value",
        description="Value of the field option.",
    )


class CheckboxFormField(SerializableModel):
    """Checkbox form field."""

    type: Literal["checkbox"] = Field(
        "checkbox",
        title="CheckboxFormField.Type",
        description="Type of the field.",
    )
    id: str = Field(
        ...,
        title="CheckboxFormField.ID",
        description="ID of the field.",
    )
    title: str = Field(
        ...,
        title="CheckboxFormField.Title",
        description="Title of the field.",
    )
    description: str | None = Field(
        ...,
        title="CheckboxFormField.Description",
        description="Description of the field.",
    )
    required: bool = Field(
        ...,
        title="CheckboxFormField.Required",
        description="Whether the field is required.",
    )
    options: list[CheckboxFormFieldOption] = Field(
        ...,
        title="CheckboxFormField.Options",
        description="Options of the field.",
    )
    default: list[str] | None = Field(
        ...,
        title="CheckboxFormField.Default",
        description="Default value of the field.",
    )

    @field_validator("default", mode="before")
    @classmethod
    def _validate_default(cls, v: Any) -> Any:
        """Validate default value."""

        if isinstance(v, str):
            return v.split(",")

        return v


class DateFormField(SerializableModel):
    """Date form field."""

    type: Literal["date"] = Field(
        "date",
        title="DateFormField.Type",
        description="Type of the field.",
    )
    id: str = Field(
        ...,
        title="DateFormField.ID",
        description="ID of the field.",
    )
    title: str = Field(
        ...,
        title="DateFormField.Title",
        description="Title of the field.",
    )
    description: str | None = Field(
        ...,
        title="DateFormField.Description",
        description="Description of the field.",
    )
    required: bool = Field(
        ...,
        title="DateFormField.Required",
        description="Whether the field is required.",
    )
    default: date | None = Field(
        ...,
        title="DateFormField.Default",
        description="Default value of the field.",
    )


class DropdownFormFieldOption(SerializableModel):
    """Dropdown form field option."""

    id: str = Field(
        ...,
        title="DropdownFormFieldOption.ID",
        description="ID of the field option.",
    )
    title: str | None = Field(
        ...,
        title="DropdownFormFieldOption.Title",
        description="Title of the field option.",
    )
    value: str = Field(
        ...,
        title="DropdownFormFieldOption.Value",
        description="Value of the field option.",
    )


class DropdownFormField(SerializableModel):
    """Dropdown form field."""

    type: Literal["dropdown"] = Field(
        "dropdown",
        title="DropdownFormField.Type",
        description="Type of the field.",
    )
    id: str = Field(
        ...,
        title="DropdownFormField.ID",
        description="ID of the field.",
    )
    title: str = Field(
        ...,
        title="DropdownFormField.Title",
        description="Title of the field.",
    )
    description: str | None = Field(
        ...,
        title="DropdownFormField.Description",
        description="Description of the field.",
    )
    required: bool = Field(
        ...,
        title="DropdownFormField.Required",
        description="Whether the field is required.",
    )
    options: list[DropdownFormFieldOption] = Field(
        ...,
        title="DropdownFormField.Options",
        description="Options of the field.",
    )
    default: str | None = Field(
        ...,
        title="DropdownFormField.Default",
        description="Default value of the field.",
    )


class EmailFormField(SerializableModel):
    """Email form field."""

    type: Literal["email"] = Field(
        "email",
        title="EmailFormField.Type",
        description="Type of the field.",
    )
    id: str = Field(
        ...,
        title="EmailFormField.ID",
        description="ID of the field.",
    )
    title: str = Field(
        ...,
        title="EmailFormField.Title",
        description="Title of the field.",
    )
    description: str | None = Field(
        ...,
        title="EmailFormField.Description",
        description="Description of the field.",
    )
    required: bool = Field(
        ...,
        title="EmailFormField.Required",
        description="Whether the field is required.",
    )
    default: str | None = Field(
        ...,
        title="EmailFormField.Default",
        description="Default value of the field.",
    )


class NumberFormField(SerializableModel):
    """Number form field."""

    type: Literal["number"] = Field(
        "number",
        title="NumberFormField.Type",
        description="Type of the field.",
    )
    id: str = Field(
        ...,
        title="NumberFormField.ID",
        description="ID of the field.",
    )
    title: str = Field(
        ...,
        title="NumberFormField.Title",
        description="Title of the field.",
    )
    description: str | None = Field(
        ...,
        title="NumberFormField.Description",
        description="Description of the field.",
    )
    required: bool = Field(
        ...,
        title="NumberFormField.Required",
        description="Whether the field is required.",
    )
    default: float | None = Field(
        ...,
        title="NumberFormField.Default",
        description="Default value of the field.",
    )


class RadioFormFieldOption(SerializableModel):
    """Radio form field option."""

    id: str = Field(
        ...,
        title="RadioFormFieldOption.ID",
        description="ID of the field option.",
    )
    title: str | None = Field(
        ...,
        title="RadioFormFieldOption.Title",
        description="Title of the field option.",
    )
    value: str = Field(
        ...,
        title="RadioFormFieldOption.Value",
        description="Value of the field option.",
    )


class RadioFormField(SerializableModel):
    """Radio form field."""

    type: Literal["radio"] = Field(
        "radio",
        title="RadioFormField.Type",
        description="Type of the field.",
    )
    id: str = Field(
        ...,
        title="RadioFormField.ID",
        description="ID of the field.",
    )
    title: str = Field(
        ...,
        title="RadioFormField.Title",
        description="Title of the field.",
    )
    description: str | None = Field(
        ...,
        title="RadioFormField.Description",
        description="Description of the field.",
    )
    required: bool = Field(
        ...,
        title="RadioFormField.Required",
        description="Whether the field is required.",
    )
    options: list[RadioFormFieldOption] = Field(
        ...,
        title="RadioFormField.Options",
        description="Options of the field.",
    )
    default: str | None = Field(
        ...,
        title="RadioFormField.Default",
        description="Default value of the field.",
    )


class SliderFormField(SerializableModel):
    """Slider form field."""

    type: Literal["slider"] = Field(
        "slider",
        title="SliderFormField.Type",
        description="Type of the field.",
    )
    id: str = Field(
        ...,
        title="SliderFormField.ID",
        description="ID of the field.",
    )
    title: str = Field(
        ...,
        title="SliderFormField.Title",
        description="Title of the field.",
    )
    description: str | None = Field(
        ...,
        title="SliderFormField.Description",
        description="Description of the field.",
    )
    required: bool = Field(
        ...,
        title="SliderFormField.Required",
        description="Whether the field is required.",
    )
    min: float = Field(
        ...,
        title="SliderFormField.Min",
        description="Minimum value of the field.",
    )
    max: float = Field(
        ...,
        title="SliderFormField.Max",
        description="Maximum value of the field.",
    )
    step: float = Field(
        ...,
        title="SliderFormField.Step",
        description="Step of the field.",
    )
    default: float | None = Field(
        ...,
        title="SliderFormField.Default",
        description="Default value of the field.",
    )


class TextareaFormField(SerializableModel):
    """Textarea form field."""

    type: Literal["textarea"] = Field(
        "textarea",
        title="TextareaFormField.Type",
        description="Type of the field.",
    )
    id: str = Field(
        ...,
        title="TextareaFormField.ID",
        description="ID of the field.",
    )
    title: str = Field(
        ...,
        title="TextareaFormField.Title",
        description="Title of the field.",
    )
    description: str | None = Field(
        ...,
        title="TextareaFormField.Description",
        description="Description of the field.",
    )
    required: bool = Field(
        ...,
        title="TextareaFormField.Required",
        description="Whether the field is required.",
    )
    default: str | None = Field(
        ...,
        title="TextareaFormField.Default",
        description="Default value of the field.",
    )


class TextFormField(SerializableModel):
    """Text form field."""

    type: Literal["text"] = Field(
        "text",
        title="TextFormField.Type",
        description="Type of the field.",
    )
    id: str = Field(
        ...,
        title="TextFormField.ID",
        description="ID of the field.",
    )
    title: str = Field(
        ...,
        title="TextFormField.Title",
        description="Title of the field.",
    )
    description: str | None = Field(
        ...,
        title="TextFormField.Description",
        description="Description of the field.",
    )
    required: bool = Field(
        ...,
        title="TextFormField.Required",
        description="Whether the field is required.",
    )
    default: str | None = Field(
        ...,
        title="TextFormField.Default",
        description="Default value of the field.",
    )


class UrlFormField(SerializableModel):
    """URL form field."""

    type: Literal["url"] = Field(
        "url",
        title="UrlFormField.Type",
        description="Type of the field.",
    )
    id: str = Field(
        ...,
        title="UrlFormField.ID",
        description="ID of the field.",
    )
    title: str = Field(
        ...,
        title="UrlFormField.Title",
        description="Title of the field.",
    )
    description: str | None = Field(
        ...,
        title="UrlFormField.Description",
        description="Description of the field.",
    )
    required: bool = Field(
        ...,
        title="UrlFormField.Required",
        description="Whether the field is required.",
    )
    default: str | None = Field(
        ...,
        title="UrlFormField.Default",
        description="Default value of the field.",
    )


class YesNoFormField(SerializableModel):
    """Yes/no form field."""

    type: Literal["yes-no"] = Field(
        "yes-no",
        title="YesNoFormField.Type",
        description="Type of the field.",
    )
    id: str = Field(
        ...,
        title="YesNoFormField.ID",
        description="ID of the field.",
    )
    title: str = Field(
        ...,
        title="YesNoFormField.Title",
        description="Title of the field.",
    )
    description: str | None = Field(
        ...,
        title="YesNoFormField.Description",
        description="Description of the field.",
    )
    required: bool = Field(
        ...,
        title="YesNoFormField.Required",
        description="Whether the field is required.",
    )
    default: bool | None = Field(
        ...,
        title="YesNoFormField.Default",
        description="Default value of the field.",
    )


FormField = Annotated[
    CheckboxFormField
    | DateFormField
    | DropdownFormField
    | EmailFormField
    | NumberFormField
    | RadioFormField
    | SliderFormField
    | TextareaFormField
    | TextFormField
    | UrlFormField
    | YesNoFormField,
    Field(discriminator="type"),
]


class Form(SerializableModel):
    """Form data."""

    id: str = Field(
        ...,
        title="Form.ID",
        description="ID of the form.",
    )
    title: str = Field(
        ...,
        title="Form.Title",
        description="Title of the form.",
    )
    fields: list[FormField] = Field(
        ...,
        title="Form.Fields",
        description="Fields of the form.",
    )


class Device(SerializableModel):
    """Device data."""

    type: str = Field(
        ...,
        title="Device.Type",
        description="Type of the device.",
    )
    name: str = Field(
        ...,
        title="Device.Name",
        description="Name of the device.",
    )


class SubmissionMetadata(SerializableModel):
    """Submission metadata."""

    device: Device | None = Field(
        None,
        title="Submission.Device",
        description="Device of the submission.",
    )


class Submission(SerializableModel):
    """Submission data."""

    metadata: SubmissionMetadata = Field(
        ...,
        title="Submission.Metadata",
        description="Metadata of the submission.",
    )
    fields: dict[str, Any] = Field(
        ...,
        title="Submission.Fields",
        description="Fields of the submission.",
    )

    @field_validator("fields", mode="before")
    @classmethod
    def _validate_fields(cls, v: Any) -> Any:
        """Validate fields."""

        try:
            return json.loads(json.dumps(v))
        except (TypeError, json.JSONDecodeError) as e:
            raise ValueError("fields must be a valid JSON") from e  # noqa: TRY003


class SubmissionConfirmation(SerializableModel):
    """Submission confirmation data."""

    submission: str = Field(
        ...,
        title="SubmissionConfirmation.ID",
        description="ID of the submission.",
    )
