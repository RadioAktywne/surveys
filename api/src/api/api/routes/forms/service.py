import json
from asyncio import TaskGroup
from typing import Any
from uuid import uuid4

from pydantic import ValidationError

from api.api.routes.forms.errors import (
    FieldNotFoundError,
    FormNotFoundError,
    GraphQLError,
)
from api.graphql import errors as ge
from api.graphql import models as gm
from api.graphql.client import GraphQLClient
from api.models import data as dm


class Service:
    """Service for the forms endpoints."""

    def __init__(self, graphql: GraphQLClient) -> None:
        self._graphql = graphql

    def _parse_pager(self, pager: gm.FormPager) -> dm.FormPager:
        """Parse pager."""

        return dm.FormPager(
            entries=[
                dm.FormPagerEntry(
                    id=entry.id,
                    title=entry.title,
                )
                for entry in pager.entries
            ],
            total=pager.total,
            limit=pager.limit,
            start=pager.start,
        )

    async def list(
        self,
        limit: int | None = None,
        start: int | None = None,
    ) -> dm.FormPager:
        """List forms."""

        request = gm.ListFormsRequest(limit=limit, start=start)

        try:
            response = await self._graphql.list_forms(request)
        except ge.GraphQLError as e:
            raise GraphQLError() from e

        return self._parse_pager(response.pager)

    def _parse_json_value(self, value: str | None) -> Any:
        """Parse JSON value."""

        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return None

    def _parse_checkbox_field(self, field: gm.FormField) -> dm.CheckboxFormField:
        """Parse checkbox form field."""

        return dm.CheckboxFormField(
            id=field.id,
            title=field.title,
            description=field.description or None,
            required=field.required,
            options=[
                dm.CheckboxFormFieldOption(
                    id=option.id,
                    title=option.title,
                    value=option.value,
                )
                for option in field.options
            ],
            default=self._parse_json_value(field.default_value),
        )

    def _parse_date_field(self, field: gm.FormField) -> dm.DateFormField:
        """Parse date form field."""

        return dm.DateFormField(
            id=field.id,
            title=field.title,
            description=field.description or None,
            required=field.required,
            default=self._parse_json_value(field.default_value),
        )

    def _parse_dropdown_field(self, field: gm.FormField) -> dm.DropdownFormField:
        """Parse dropdown form field."""

        return dm.DropdownFormField(
            id=field.id,
            title=field.title,
            description=field.description or None,
            required=field.required,
            options=[
                dm.DropdownFormFieldOption(
                    id=option.id,
                    title=option.title,
                    value=option.value,
                )
                for option in field.options
            ],
            default=self._parse_json_value(field.default_value),
        )

    def _parse_email_field(self, field: gm.FormField) -> dm.EmailFormField:
        """Parse email form field."""

        return dm.EmailFormField(
            id=field.id,
            title=field.title,
            description=field.description or None,
            required=field.required,
            default=self._parse_json_value(field.default_value),
        )

    def _parse_number_field(self, field: gm.FormField) -> dm.NumberFormField:
        """Parse number form field."""

        return dm.NumberFormField(
            id=field.id,
            title=field.title,
            description=field.description or None,
            required=field.required,
            default=self._parse_json_value(field.default_value),
        )

    def _parse_radio_field(self, field: gm.FormField) -> dm.RadioFormField:
        """Parse radio form field."""

        return dm.RadioFormField(
            id=field.id,
            title=field.title,
            description=field.description or None,
            required=field.required,
            options=[
                dm.RadioFormFieldOption(
                    id=option.id,
                    title=option.title,
                    value=option.value,
                )
                for option in field.options
            ],
            default=self._parse_json_value(field.default_value),
        )

    def _parse_slider_field(self, field: gm.FormField) -> dm.SliderFormField:
        """Parse slider form field."""

        return dm.SliderFormField(
            id=field.id,
            title=field.title,
            description=field.description or None,
            required=field.required,
            min=field.options[0].value,
            max=field.options[1].value,
            step=field.options[2].value,
            default=self._parse_json_value(field.default_value),
        )

    def _parse_textarea_field(self, field: gm.FormField) -> dm.TextareaFormField:
        """Parse textarea form field."""

        return dm.TextareaFormField(
            id=field.id,
            title=field.title,
            description=field.description or None,
            required=field.required,
            default=self._parse_json_value(field.default_value),
        )

    def _parse_text_field(self, field: gm.FormField) -> dm.TextFormField:
        """Parse text form field."""

        return dm.TextFormField(
            id=field.id,
            title=field.title,
            description=field.description or None,
            required=field.required,
            default=self._parse_json_value(field.default_value),
        )

    def _parse_url_field(self, field: gm.FormField) -> dm.UrlFormField:
        """Parse url form field."""

        return dm.UrlFormField(
            id=field.id,
            title=field.title,
            description=field.description or None,
            required=field.required,
            default=self._parse_json_value(field.default_value),
        )

    def _parse_yesno_field(self, field: gm.FormField) -> dm.YesNoFormField:
        """Parse yes/no form field."""

        return dm.YesNoFormField(
            id=field.id,
            title=field.title,
            description=field.description or None,
            required=field.required,
            default=self._parse_json_value(field.default_value),
        )

    def _parse_form_field(self, field: gm.FormField) -> dm.FormField | None:
        """Parse form field."""

        try:
            match field.type:
                case "checkbox":
                    return self._parse_checkbox_field(field)
                case "date":
                    return self._parse_date_field(field)
                case "dropdown":
                    return self._parse_dropdown_field(field)
                case "email":
                    return self._parse_email_field(field)
                case "number":
                    return self._parse_number_field(field)
                case "radio":
                    return self._parse_radio_field(field)
                case "slider":
                    return self._parse_slider_field(field)
                case "textarea":
                    return self._parse_textarea_field(field)
                case "textfield":
                    return self._parse_text_field(field)
                case "link":
                    return self._parse_url_field(field)
                case "yes_no":
                    return self._parse_yesno_field(field)
        except ValidationError:
            pass

        return None

    def _parse_form(self, form: gm.Form) -> dm.Form:
        """Parse form."""

        fields = sorted(form.fields, key=lambda field: field.idx or 0)
        fields = [self._parse_form_field(field) for field in fields]
        fields = [field for field in fields if field is not None]

        return dm.Form(
            id=form.id,
            title=form.title,
            fields=fields,
        )

    async def get(self, id: str) -> dm.Form:
        """Get form."""

        request = gm.GetFormRequest(id=id)

        try:
            response = await self._graphql.get_form(request)
        except ge.NotFoundError as e:
            raise FormNotFoundError(form=id) from e
        except ge.GraphQLError as e:
            raise GraphQLError() from e

        return self._parse_form(response.form)

    def _generate_submission_token(self) -> str:
        """Generate submission token."""

        return uuid4().hex

    async def _start_submission(
        self, id: str, metadata: dm.SubmissionMetadata, token: str
    ) -> gm.Submission:
        """Start submission."""

        request = gm.StartSubmissionRequest(
            form=id,
            submission=gm.SubmissionStartData(
                token=token,
                device=gm.Device(
                    type=metadata.device.type if metadata.device else "unknown",
                    name=metadata.device.name if metadata.device else "unknown",
                ),
            ),
        )

        try:
            response = await self._graphql.start_submission(request)
        except ge.NotFoundError as e:
            raise FormNotFoundError(form=id) from e
        except ge.GraphQLError as e:
            raise GraphQLError() from e

        return response.submission

    async def _submit_form_field(
        self, submission: str, field: str, data: Any, token: str
    ) -> None:
        """Submit form field."""

        request = gm.SubmitFieldRequest(
            submission=submission,
            field=gm.SubmissionFieldData(
                token=token,
                field=field,
                data=json.dumps(data),
            ),
        )

        try:
            await self._graphql.submit_field(request)
        except ge.NotFoundError as e:
            raise FieldNotFoundError(field=field) from e
        except ge.GraphQLError as e:
            raise GraphQLError() from e

    async def _submit_form_fields(
        self, submission: str, fields: dict[str, Any], token: str
    ) -> None:
        """Submit form fields."""

        try:
            async with TaskGroup() as group:
                for field, data in fields.items():
                    coro = self._submit_form_field(submission, field, data, token)
                    group.create_task(coro)
        except ExceptionGroup as e:
            raise e.exceptions[0] from e

    async def _finish_submission(self, submission: str) -> None:
        """Finish submission."""

        request = gm.FinishSubmissionRequest(submission=submission)

        try:
            await self._graphql.finish_submission(request)
        except ge.GraphQLError as e:
            raise GraphQLError() from e

    async def submit(
        self, id: str, submission: dm.Submission
    ) -> dm.SubmissionConfirmation:
        """Submit form."""

        token = self._generate_submission_token()

        graphql_submission = await self._start_submission(
            id, submission.metadata, token
        )
        await self._submit_form_fields(graphql_submission.id, submission.fields, token)
        await self._finish_submission(graphql_submission.id)

        return dm.SubmissionConfirmation(submission=graphql_submission.id)
