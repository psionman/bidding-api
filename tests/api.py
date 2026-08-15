import logging
import sys

import requests

logger = logging.getLogger(__name__)

API_DOMAIN = "http://localhost:8000"  # adjust as needed

# No session/CSRF auth in play, so a plain Session (or even
# requests.post directly) is fine — kept as a Session in case you
# want connection reuse across a batch of test calls.
session = requests.Session()


def post_data_to_api(
    uri: str, params: dict | None = None, repeat: bool = False
) -> dict:
    while True:
        result = _get_hand(uri, params)
        if not repeat:
            break
        result = input("Press Enter to continue...")
        if result.lower() == "q":
            break


def _get_hand(uri: str, params: dict | None) -> dict:
    """Python equivalent of postDataToAPI for testing bidding_conventions."""
    if params is None:
        params = {}

    endpoint = f"{API_DOMAIN}/{uri}/"

    try:
        response = session.post(
            endpoint,
            json=params,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if not response.ok:
            err_text = ""
            try:
                err_text = response.text
            except Exception:
                pass
            raise RuntimeError(f"HTTP {response.status_code} - {err_text}")

        data = response.json()
        _display_data(data)

        if "error" in data:
            print(f"Error: {data['error']}")
            return data

        return data

    except (requests.RequestException, RuntimeError, ValueError) as err:
        logger.error("POST failed: %s", err)
        print(f"Error at {uri}\n{err}")
        raise


def _display_data(data: dict) -> None:
    data.pop("description")
    for key, item in sorted(data.items()):
        print(f"{key:<20}: {item}")


if __name__ == "__main__":
    repeat = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "repeat":
            repeat = True
    post_data_to_api(
        "conventions-selected", {"conventions": ["lebensohl"]}, repeat=repeat
    )
