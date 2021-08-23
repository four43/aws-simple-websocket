import json
from pathlib import Path

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def get_fixture_json(fixture_name: str):
    with open(FIXTURE_DIR / fixture_name) as fixture_fh:
        return json.load(fixture_fh)
