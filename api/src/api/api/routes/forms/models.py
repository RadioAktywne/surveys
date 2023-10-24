from pydantic import Field

from api.models.base import SerializableModel
from api.models.data import Form, FormPager, Submission, SubmissionConfirmation


class ListResponse(SerializableModel):
    """Response model for the GET /forms endpoint."""

    pager: FormPager = Field(
        ...,
        title="ListResponse.Pager",
        description="The pager for the forms.",
    )


class GetResponse(SerializableModel):
    """Response model for the GET /forms/:id endpoint."""

    form: Form = Field(
        ...,
        title="GetResponse.Form",
        description="The form.",
    )


class SubmitRequest(SerializableModel):
    """Request model for the POST /forms/:id/submit endpoint."""

    submission: Submission = Field(
        ...,
        title="SubmitRequest.Submission",
        description="The submission for the form.",
    )


class SubmitResponse(SerializableModel):
    """Response model for the POST /forms/:id/submit endpoint."""

    confirmation: SubmissionConfirmation = Field(
        ...,
        title="SubmitResponse.Confirmation",
        description="The confirmation for the submission.",
    )
