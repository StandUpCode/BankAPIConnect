import uuid
from typing import Tuple

import httpx as httpx
import pytz
from httpx_auth import (
    OAuth2ClientCredentials,
    GrantNotProvided,
    InvalidGrantRequest,

)

bkk_tz = pytz.timezone("Asia/Bangkok")


class SCBOAuth2ClientCredentials(OAuth2ClientCredentials):

    def __init__(
            self,
            token_url: str,
            client_id: str,
            client_secret: str,
            **kwargs,
    ):

        super().__init__(
            token_url,
            client_id,
            client_secret,
            token_field_name="accessToken",
            **kwargs,
        )
        self.data = {
            "applicationKey": client_id,
            "applicationSecret": client_secret,
        }

    def request_new_grant_with_post_scb_special(
            self, url: str, data, grant_name: str, client: httpx.Client
    ) -> Tuple[str, int]:

        with client:
            header = {
                "Content-Type": "application/json",
                "resourceOwnerId": self.client_id,
                "requestUId": uuid.uuid4().hex,
                "accept-language": "EN",
            }
            response = client.post(url, json=data, headers=header)

            if response.is_error:
                # As described in https://tools.ietf.org/html/rfc6749#section-5.2
                raise InvalidGrantRequest(response)

            content = response.json().get("data")

        token = content.get(grant_name)
        if not token:
            raise GrantNotProvided(grant_name, content)
        return token, content.get("expiresIn")

    def request_new_token(self) -> tuple:

        # As described in https://tools.ietf.org/html/rfc6749#section-4.3.3
        token, expires_in = self.request_new_grant_with_post_scb_special(
            self.token_url, self.data, self.token_field_name, self.client
        )
        # Handle both Access and Bearer tokens
        return (
            (self.state, token, expires_in) if expires_in else (self.state, token)
        )
