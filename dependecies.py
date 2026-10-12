import os, hmac

from fastapi import Request, status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

from config import settings

class RapidAPIIdentity(BaseModel):
    username: str
    subscription: str

async def verify_rapidapi_request(
    request: Request,
) -> RapidAPIIdentity:
    """
    FastAPI dependency that validates RapidAPI proxy headers.

    Verifies:
    - Proxy secret
    - Exactly one occurrence of each required header
    - Username format
    - Subscription plan allowlist
    """

    required_headers = (
        "X-RapidAPI-Proxy-Secret",
        "X-RapidAPI-User",
        "X-RapidAPI-Subscription",
    )

    header_values = {}

    # Read raw ASGI headers so duplicate occurrences can be rejected.
    for header_name in required_headers:
        target = header_name.lower().encode("ascii")

        occurrences = [
            value.decode("latin-1")
            for key, value in request.scope.get("headers", [])
            if key.lower() == target
        ]

        if len(occurrences) != 1 or not occurrences[0].strip():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid RapidAPI authentication headers",
            )

        header_values[header_name] = occurrences[0].strip()

    expected_secret = settings.rapidapi_proxy_secret.get_secret_value()

    if not expected_secret:
        raise HTTPException(
            status_code=503,
            detail="RapidAPI authentication is not configured",
        )

    provided_secret = header_values["X-RapidAPI-Proxy-Secret"]

    if not hmac.compare_digest(provided_secret, expected_secret):
        raise HTTPException(
            status_code=401,
            detail="Invalid RapidAPI authentication headers",
        )

    # for expected_secret in configured_secrets:
    #     matches = hmac.compare_digest(
    #         provided_secret,
    #         expected_secret,
    #     )
    #     secret_is_valid = secret_is_valid or matches
    #
    # if not secret_is_valid:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid RapidAPI authentication headers",
    #     )

    # Validate the external username format.
    username = header_values["X-RapidAPI-User"]

    # if not USERNAME_PATTERN.fullmatch(username):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid RapidAPI authentication headers",
    #     )

    # Validate the subscription against configured plans.
    subscription = header_values["X-RapidAPI-Subscription"].upper()

    if subscription not in settings.rapidapi_allowed_plans:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid RapidAPI authentication headers",
        )

    # Return the verified identity to the protected endpoint.
    return RapidAPIIdentity(
        username=username,
        subscription=subscription,
    )