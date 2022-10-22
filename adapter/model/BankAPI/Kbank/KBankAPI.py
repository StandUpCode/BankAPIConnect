import uuid
from datetime import datetime
from typing import Optional, Dict

import httpx
import pytz
from furl import furl
from httpx._types import CertTypes
from loguru import logger

from Config.KBankConfig import KBankConfig
from .KbankModel import KbankSlipVerifyResponse
from .KbankOauth import KBankOAuth2ClientCredentials

bkk_tz = pytz.timezone("Asia/Bangkok")


class KBankAPI_Service:
    creds: Optional[Dict] = None

    def __init__(
            self,
            config: KBankConfig,
            cert: CertTypes,
            base_url="https://openapi.kasikornbank.com",
    ):
        self.consumer_id = config.KBANK_CONSUMER_ID
        self.consumer_secret = config.KBANK_CONSUMER_SECRET
        self.cert = cert
        self.base_url = furl(base_url)
        auth_url = self.base_url / "oauth/token"
        client = httpx.Client(cert=self.cert)

        # change this to async with https://docs.authlib.org/en/latest/client/httpx.html
        auth = KBankOAuth2ClientCredentials(
            auth_url.url,
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            client=client,
        )

        self.client = httpx.AsyncClient(
            base_url=base_url, cert=self.cert, auth=auth
        )

        self.client_sync = httpx.Client(
            base_url=base_url, cert=self.cert, auth=auth
        )

    async def get_token(self):
        """
        This is normally handle by `KBankOAuth2ClientCredentials` automatically. This is for dev to call.
        """

        body = {"grant_type": "client_credentials"}

        auth_url = self.base_url / "oauth/token"
        r = httpx.post(
            auth_url.url,
            data=body,
            auth=(self.consumer_id, self.consumer_secret),
            cert=self.cert,
        )

        if r.status_code == 200:
            self.creds = r.json()
            return r.json()
        else:
            return r

    async def verify_slip(self,
                          transaction_ref_id: str,
                          sending_bank_id: str, *, raw=False):
        body = {
            "rqUID": uuid.uuid4().hex,
            "rqDt": datetime.now(tz=bkk_tz).isoformat(),
            "data": {"sendingBank": sending_bank_id, "transRef": transaction_ref_id},
        }

        r = await self.client.post("/v1/verslip/kbank/verify", json=body)

        if r.status_code == 200:
            json = r.json()
            if raw:
                return json
            try:
                response = KbankSlipVerifyResponse(**json)
                if response.status_message.strip() != "SUCCESS":
                    logger.warning(
                        "Not Success: {} {}",
                        response.status_code,
                        response.status_message,
                    )
                return response
            except Exception as e:
                logger.debug("data is {}", json)
                raise Exception("Could not parse the json") from e
        else:
            return r

    def verify_slip_sync(self, sending_bank_id, trans_ref, *, raw=False):
        body = {
            "rqUID": uuid.uuid4().hex,
            "rqDt": datetime.now(tz=bkk_tz).isoformat(),
            "data": {"sendingBank": sending_bank_id, "transRef": trans_ref},
        }

        r = self.client_sync.post("/v1/verslip/kbank/verify", json=body)

        if r.status_code == 200:
            json = r.json()
            if raw:
                return json
            try:
                response = KbankSlipVerifyResponse(**json)
                if response.status_message.strip() != "SUCCESS":
                    logger.warning(
                        "Not Success: {} {}",
                        response.status_code,
                        response.status_message,
                    )
                return response
            except Exception as e:
                logger.debug("data is {}", json)
                raise Exception("Could not parse the json") from e
        else:
            return r
