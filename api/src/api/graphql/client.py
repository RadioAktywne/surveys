from typing import Awaitable, Callable, Self, TypeVar

from fifolock import FifoLock
from gql import Client, gql
from gql.transport.exceptions import TransportError, TransportQueryError
from gql.transport.httpx import HTTPXAsyncTransport
from graphql import DocumentNode

from api.graphql.errors import (
    ConnectError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    UnkownError,
)
from api.graphql.models import (
    FinishSubmissionRequest,
    FinishSubmissionResponse,
    GetFormRequest,
    GetFormResponse,
    ListFormsRequest,
    ListFormsResponse,
    LoginRequest,
    LoginResponse,
    StartSubmissionRequest,
    StartSubmissionResponse,
    SubmitFieldRequest,
    SubmitFieldResponse,
    Tokens,
)
from api.locks import Read, Write

T = TypeVar("T")


class GraphQLRawClient:
    """GraphQL raw client."""

    def __init__(self, url: str) -> None:
        self._client = Client(
            transport=HTTPXAsyncTransport(url=url),
        )

    async def connect(self) -> None:
        """Connect to the GraphQL API."""

        try:
            await self._client.connect_async(reconnecting=True)
        except TransportError as e:
            raise ConnectError() from e

    async def close(self) -> None:
        """Close the connection to the GraphQL API."""

        try:
            await self._client.close_async()
        except TransportError as e:
            raise ConnectError() from e

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()

    def _build_authentication_headers(self, tokens: Tokens) -> dict:
        """Build authentication headers."""

        return {"Authorization": f"Bearer {tokens.access}"}

    async def _execute(
        self,
        query: DocumentNode,
        variables: dict | None = None,
        headers: dict | None = None,
    ) -> dict:
        """Execute a GraphQL query."""

        try:
            return await self._client.session.execute(
                query,
                variable_values=variables,
                extra_args={"headers": headers},
            )
        except TransportQueryError as e:
            error = e.errors[0] if e.errors else None

            if error is None:
                raise UnkownError() from e

            message = error.get("message")
            code = error.get("extensions", {}).get("code")

            if not code:
                raise UnkownError(message) from e

            if code == "FORBIDDEN":
                raise ForbiddenError(message) from e

            if code == "INTERNAL_SERVER_ERROR":
                if message == "invalid id passed":
                    raise NotFoundError(message) from e

                raise InternalServerError(message) from e

            raise UnkownError(message) from e
        except TransportError as e:
            raise ConnectError() from e

    def _get_login_query(self) -> DocumentNode:
        """Get the login query."""

        return gql(
            """
            mutation authLogin($username: String!, $password: String!) {
              tokens: authLogin(username: $username, password: $password) {
                access: accessToken
                refresh: refreshToken
              }
            }
            """
        )

    def _build_login_variables(self, request: LoginRequest) -> dict:
        """Build the login variables."""

        return request.model_dump(mode="json")

    def _parse_login_response(self, response: dict) -> LoginResponse:
        """Parse the login response."""

        return LoginResponse.model_validate(response)

    async def login(self, request: LoginRequest) -> LoginResponse:
        """Login to the GraphQL API."""

        query = self._get_login_query()
        variables = self._build_login_variables(request)
        response = await self._execute(query, variables)
        return self._parse_login_response(response)

    def _get_list_forms_query(self) -> DocumentNode:
        """Get the list forms query."""

        return gql(
            """
            query listForms($start: Int, $limit: Int) {
              pager: listForms(start: $start, limit: $limit) {
                entries {
                  id
                  title
                }
                total
                limit
                start
              }
            }
            """
        )

    def _build_list_forms_variables(self, request: ListFormsRequest | None) -> dict:
        """Build the list forms variables."""

        if request is None:
            return {}

        variables = request.model_dump(mode="json")

        if request.start is None:
            variables.pop("start")

        if request.limit is None:
            variables.pop("limit")

        return variables

    def _parse_list_forms_response(self, response: dict) -> ListFormsResponse:
        """Parse the list forms response."""

        return ListFormsResponse.model_validate(response)

    async def list_forms(
        self, tokens: Tokens, request: ListFormsRequest | None = None
    ) -> ListFormsResponse:
        """List forms."""

        query = self._get_list_forms_query()
        variables = self._build_list_forms_variables(request)
        headers = self._build_authentication_headers(tokens)
        response = await self._execute(query, variables, headers)
        return self._parse_list_forms_response(response)

    def _get_form_query(self) -> DocumentNode:
        """Get the form query."""

        return gql(
            """
            query getFormById($id: ID!) {
              form: getFormById(id: $id) {
                id
                title
                fields {
                  id
                  idx
                  title
                  type
                  description
                  required
                  defaultValue
                  options {
                    id
                    title
                    value
                  }
                }
              }
            }
            """
        )

    def _build_form_variables(self, request: GetFormRequest) -> dict:
        """Build the form variables."""

        return request.model_dump(mode="json")

    def _parse_form_response(self, response: dict) -> GetFormResponse:
        """Parse the form response."""

        return GetFormResponse.model_validate(response)

    async def get_form(
        self, request: GetFormRequest, tokens: Tokens
    ) -> GetFormResponse:
        """Get a form."""

        query = self._get_form_query()
        variables = self._build_form_variables(request)
        headers = self._build_authentication_headers(tokens)
        response = await self._execute(query, variables, headers)
        return self._parse_form_response(response)

    def _get_start_submission_query(self) -> DocumentNode:
        """Get the start submission query."""

        return gql(
            """
            mutation submissionStart($form: ID!, $submission: SubmissionStartInput!) {
              submission: submissionStart(form: $form, submission: $submission) {
                id
                percentageComplete
              }
            }
            """
        )

    def _build_start_submission_variables(
        self, request: StartSubmissionRequest
    ) -> dict:
        """Build the start submission variables."""

        return request.model_dump(mode="json")

    def _parse_start_submission_response(
        self, response: dict
    ) -> StartSubmissionResponse:
        """Parse the start submission response."""

        return StartSubmissionResponse.model_validate(response)

    async def start_submission(
        self, request: StartSubmissionRequest, tokens: Tokens
    ) -> StartSubmissionResponse:
        """Start a submission."""

        query = self._get_start_submission_query()
        variables = self._build_start_submission_variables(request)
        headers = self._build_authentication_headers(tokens)
        response = await self._execute(query, variables, headers)
        return self._parse_start_submission_response(response)

    def _get_submit_field_query(self) -> DocumentNode:
        """Get the submit field query."""

        return gql(
            """
            mutation submissionSetField($submission: ID!, $field: SubmissionSetFieldInput!) {
              submission: submissionSetField(submission: $submission, field: $field) {
                id
                percentageComplete
              }
            }
            """
        )

    def _build_submit_field_variables(self, request: SubmitFieldRequest) -> dict:
        """Build the submit field variables."""

        return request.model_dump(mode="json")

    def _parse_submit_field_response(self, response: dict) -> SubmitFieldResponse:
        """Parse the submit field response."""

        return SubmitFieldResponse.model_validate(response)

    async def submit_field(
        self, request: SubmitFieldRequest, tokens: Tokens
    ) -> SubmitFieldResponse:
        """Submit a field."""

        query = self._get_submit_field_query()
        variables = self._build_submit_field_variables(request)
        headers = self._build_authentication_headers(tokens)
        response = await self._execute(query, variables, headers)
        return self._parse_submit_field_response(response)

    def _get_finish_submission_query(self) -> DocumentNode:
        """Get the finish submission query."""

        return gql(
            """
            mutation submissionFinish($submission: ID!) {
              submission: submissionFinish(submission: $submission) {
                id
                percentageComplete
              }
            }
            """
        )

    def _build_finish_submission_variables(
        self, request: FinishSubmissionRequest
    ) -> dict:
        """Build the finish submission variables."""

        return request.model_dump(mode="json")

    def _parse_finish_submission_response(
        self, response: dict
    ) -> FinishSubmissionResponse:
        """Parse the finish submission response."""

        return FinishSubmissionResponse.model_validate(response)

    async def finish_submission(
        self, request: FinishSubmissionRequest, tokens: Tokens
    ) -> FinishSubmissionResponse:
        """Finish a submission."""

        query = self._get_finish_submission_query()
        variables = self._build_finish_submission_variables(request)
        headers = self._build_authentication_headers(tokens)
        response = await self._execute(query, variables, headers)
        return self._parse_finish_submission_response(response)


class GraphQLClient:
    """GraphQL client with autologin."""

    def __init__(self, url: str, login: LoginRequest) -> None:
        self._client = GraphQLRawClient(url=url)
        self._login_request = login
        self._tokens = None
        self._lock = FifoLock()

    async def connect(self) -> None:
        """Connect to the GraphQL API."""

        async with self._lock(Write):
            await self._client.connect()
            await self._login()

    async def close(self) -> None:
        """Close the connection to the GraphQL API."""

        async with self._lock(Write):
            self._tokens = None
            await self._client.close()

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()

    async def _login(self) -> None:
        """Login to the GraphQL API."""

        response = await self._client.login(self._login_request)
        self._tokens = response.tokens

    async def _try_execute(self, func: Callable[..., Awaitable[T]], **kwargs) -> T:
        """Try to execute a GraphQL API call and login if necessary."""

        try:
            return await func(**kwargs)
        except ForbiddenError:
            async with self._lock(Write):
                await self._login()

            return await func(**kwargs)

    async def list_forms(
        self, request: ListFormsRequest | None = None
    ) -> ListFormsResponse:
        """List forms."""

        async def _list_forms() -> ListFormsResponse:
            async with self._lock(Read):
                return await self._client.list_forms(
                    request=request, tokens=self._tokens
                )

        return await self._try_execute(_list_forms)

    async def get_form(self, request: GetFormRequest) -> GetFormResponse:
        """Get a form."""

        async def _get_form() -> GetFormResponse:
            async with self._lock(Read):
                return await self._client.get_form(request=request, tokens=self._tokens)

        return await self._try_execute(_get_form)

    async def start_submission(
        self, request: StartSubmissionRequest
    ) -> StartSubmissionResponse:
        """Start a submission."""

        async def _start_submission() -> StartSubmissionResponse:
            async with self._lock(Read):
                return await self._client.start_submission(
                    request=request, tokens=self._tokens
                )

        return await self._try_execute(_start_submission)

    async def submit_field(self, request: SubmitFieldRequest) -> SubmitFieldResponse:
        """Submit a field."""

        async def _submit_field() -> SubmitFieldResponse:
            async with self._lock(Read):
                return await self._client.submit_field(
                    request=request, tokens=self._tokens
                )

        return await self._try_execute(_submit_field)

    async def finish_submission(
        self, request: FinishSubmissionRequest
    ) -> FinishSubmissionResponse:
        """Finish a submission."""

        async def _finish_submission() -> FinishSubmissionResponse:
            async with self._lock(Read):
                return await self._client.finish_submission(
                    request=request, tokens=self._tokens
                )

        return await self._try_execute(_finish_submission)
