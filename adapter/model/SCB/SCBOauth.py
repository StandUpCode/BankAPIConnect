from typing import Tuple

import httpx as httpx
import pytz
from httpx_auth import (
    OAuth2ClientCredentials,
    GrantNotProvided,
    InvalidGrantRequest,

)

bkk_tz = pytz.timezone("Asia/Bangkok")


class KBankOAuth2ClientCredentials(OAuth2ClientCredentials):
    def __init__(
            self,
            token_url: str,
            client_id: str,
            client_secret: str,
            *args,
            **kwargs
    ):
        super().__init__(token_url, client_id, client_secret, **kwargs)
        self.data = "grant_type=client_credentials"

    @staticmethod
    def request_new_grant_with_post_kbank_special(
            data,
            url: str,
            grant_name: str,
            client: httpx.Client) -> Tuple[str, int]:
        with client:
            header = {"Content-Type": "application/x-www-form-urlencoded"}
            response = client.post(url, data=data, headers=header)

            if response.is_error:
                # As described in https://tools.ietf.org/html/rfc6749#section-5.2
                raise InvalidGrantRequest(response)

            content = response.json()

        token = content.get(grant_name)
        if not token:
            raise GrantNotProvided(grant_name, content)
        return token, content.get("expires_in")

    def request_new_token(self) -> tuple:
        # As described in https://tools.ietf.org/html/rfc6749#section-4.3.3
        token, expires_in = self.request_new_grant_with_post_kbank_special(
            self.token_url,
            self.data,
            self.token_field_name,
            self.client
        )
        # Handle both Access and Bearer tokens
        return (
            (self.state, token, expires_in)
            if expires_in
            else (self.state, token)
        )
