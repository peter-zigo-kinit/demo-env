"""Test defaults — keep telemetry out of CI runs."""

from __future__ import annotations

import os

# Must run before bancont.app imports and configures Logfire.
os.environ.setdefault("LOGFIRE_SEND_TO_LOGFIRE", "false")
