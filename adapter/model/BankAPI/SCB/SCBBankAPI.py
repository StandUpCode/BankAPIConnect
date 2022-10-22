import uuid
from decimal import Decimal
from enum import Enum
from typing import Literal, Optional

import httpx
from furl import furl
from httpx._types import CertTypes
from loguru import logger
from pydantic import validate_arguments
from pydantic.types import constr

from config.SCBConfig import SCBConfig
from .SCBModel import (SCBCredentialsSCBResponse, CreateQR30SCBResponse, StatusCode,
                       VerifySCBResponse,
                       TransactionInquirySCBResponse, SCBDeeplinkResponse,
                       SCBDeeplinkTransactionResponse)
from .SCBOauth import SCBOAuth2ClientCredentials


class SCBBaseURL(str, Enum):
    sandbox = "https://api-sandbox.partners.scb/partners/sandbox/"
    uat = "https://api-uat.partners.scb/partners/"
    production = "https://api.partners.scb/partners/"


class SCBAPI_Service:
    creds: Optional[SCBCredentialsSCBResponse] = None

    def __init__(
            self,
            config: SCBConfig,
            cert: Optional[CertTypes] = None,
            base_url=SCBBaseURL.sandbox.value,
    ):

        self.api_key = config.SCB_API_KEY
        self.api_secret = config.SCB_API_SECRET
        self.cert = cert
        self.base_url = furl(base_url)

        auth_url = self.base_url / "v1/oauth/token"
        client = httpx.Client(cert=self.cert)

        auth = SCBOAuth2ClientCredentials(
            auth_url.url,
            client_id=self.api_key,
            client_secret=self.api_secret,
            client=client,
        )

        common_header = {
            "Content-Type": "application/json",
            "resourceOwnerId": self.api_key,
            "accept-language": "EN",
        }
        self.client = httpx.AsyncClient(
            base_url=base_url, cert=self.cert, headers=common_header, auth=auth
        )

        self.client_sync = httpx.Client(
            base_url=base_url, cert=self.cert, headers=common_header, auth=auth
        )

    async def get_token(self):
        """get access_token from scb"""
        # TODO: turn this into a  custom auth engine
        body = {
            "applicationKey": self.api_key,
            "applicationSecret": self.api_secret,
        }
        headers = {
            "Content-Type": "application/json",
            "resourceOwnerId": self.api_key,
            "requestUId": uuid.uuid4().hex,
            "accept-language": "EN",
        }

        auth_url = self.base_url / "v1/oauth/token"
        r = httpx.post(
            auth_url.url,
            json=body,
            headers=headers,
            cert=self.cert,
        )

        if r.status_code == 200:
            self.creds = SCBCredentialsSCBResponse.parse_raw(r.content)
            logger.debug(self.creds)
            return self.creds
        else:
            raise ConnectionError(r.json())

    @validate_arguments
    async def create_qr30(
            self,
            pp_id: constr(min_length=15, max_length=15),
            amount: Decimal,
            ref1: constr(max_length=20, regex="[A-Z0-9]*"),
            ref2: constr(max_length=20, regex="[A-Z0-9]*"),
            ref3: constr(max_length=20, regex="[A-Z]{3}[A-Z0-9]*"),
            qr_type: Literal["PP"] = "PP",
            pp_type: Literal["BILLERID"] = "BILLERID",
    ):
        request_unique_id = uuid.uuid4().hex
        headers = {
            "requestUId": request_unique_id,
        }
        payload = {
            "qrType": qr_type,
            "ppType": pp_type,
            "amount": str(amount),
            "ppId": pp_id,
            "ref1": ref1,
            "ref2": ref2,
            "ref3": ref3,
        }
        r = await self.client.post(
            "/v1/payment/qrcode/create", json=payload, headers=headers
        )

        if r.status_code == 200:
            parsed_response = CreateQR30SCBResponse.parse_raw(r.content)

            if parsed_response.status.code == StatusCode.success:
                return parsed_response
            else:
                raise ConnectionError(parsed_response.status.description)
        else:
            raise ConnectionError(r.json())

    @validate_arguments
    async def verify_slip(
            self,
            transaction_ref_id: str,
            sending_bank_id: str,
    ):

        headers = {
            "requestUId": uuid.uuid4().hex,
        }

        the_furl = (
                furl("/v1/payment/billpayment/transactions") / transaction_ref_id
        )
        the_furl.args["sendingBank"] = sending_bank_id
        logger.debug(the_furl.url)
        r = await self.client.get(the_furl.url, headers=headers)
        logger.debug(r.json())

        if r.status_code == 200:
            parsed_response = VerifySCBResponse.parse_raw(r.content)
            if parsed_response.status.code == StatusCode.success:
                return parsed_response
            else:
                raise ConnectionError(parsed_response.status.description)
        else:
            raise ConnectionError(r.json())

    @validate_arguments
    async def query_transaction(
            self,
            biller_id: str,
            reference1: str,
            transaction_date: constr(regex=r"\d{4}-\d{2}-\d{2}"),
            reference2: Optional[str] = None,
            amount: Optional[Decimal] = None,
            event_code: Literal["00300100", "00300104"] = "00300100",
    ):

        the_furl = furl("/v1/payment/billpayment/inquiry")
        args = {
            "eventCode": event_code,
            "billerId": biller_id,
            "reference1": reference1,
            "reference2": reference2,
            "amount": amount,
            "transactionDate": transaction_date,
        }
        args = {k: v for k, v in args.items() if v is not None}

        the_furl.add(args=args)

        headers = {"requestUId": uuid.uuid4().hex}

        r = await self.client.get(the_furl.url, headers=headers)

        if r.status_code == 200:
            # TODO: parse into specific object
            parsed_response = TransactionInquirySCBResponse.parse_raw(r.content)
            if parsed_response.status.code == StatusCode.success:
                return parsed_response
            else:
                raise ConnectionError(parsed_response.status.description)
        else:
            raise ConnectionError(r.json())

    @validate_arguments
    async def create_deeplink(self, payload: dict):

        the_furl = furl("/v3/deeplink/transactions")

        headers = {"requestUId": uuid.uuid4().hex, "channel": "scbeasy"}

        r = await self.client.post(the_furl.url, headers=headers, json=payload)

        if r.status_code == 200 or r.status_code == 201:
            parsed_response = SCBDeeplinkResponse.parse_raw(r.content)
            if parsed_response.status.code == StatusCode.success:
                return parsed_response
            else:
                raise ConnectionError(parsed_response.status.description)
        else:
            raise ConnectionError(r.json())

    @validate_arguments
    async def get_deeplink(self, transaction_ref_id: str):
        the_furl = furl("/v2/transactions") / transaction_ref_id

        headers = {
            "requestUId": uuid.uuid4().hex,
        }

        r = await self.client.get(the_furl.url, headers=headers)

        if r.status_code == 200:
            parsed_response = SCBDeeplinkTransactionResponse.parse_raw(
                r.content
            )
            if parsed_response.status.code == StatusCode.success:
                return parsed_response
            else:
                raise ConnectionError(parsed_response.status.description)
        else:
            raise ConnectionError(r.json())
