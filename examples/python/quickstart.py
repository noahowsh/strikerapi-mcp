#!/usr/bin/env python3
"""StrikerAPI quickstart: upcoming Premier League fixtures with three-way prices, then the league table. Needs STRIKERAPI_API_KEY. Costs about 4 credits."""
import json
import os
import sys
import urllib.error
import urllib.request

BRAND = "StrikerAPI"
KEY_ENV = "STRIKERAPI_API_KEY"
BASE_URL = "https://mcp.strikerapi.com/v1"
SIGNUP_URL = "https://strikerapi.com/signup"
LAST_REMAINING = None


class ApiError(Exception):
    pass


def require_key():
    key = os.environ.get(KEY_ENV, "").strip()
    if not key:
        sys.exit(
            f"Set {KEY_ENV} first:\n"
            f"  export {KEY_ENV}=your_key\n"
            f"Get a free key (500 credits every month, no card): {SIGNUP_URL}"
        )
    return key


def call(key, tool, args=None):
    """POST /v1/<tool> with a JSON body and return the parsed response."""
    global LAST_REMAINING
    req = urllib.request.Request(
        f"{BASE_URL}/{tool}",
        data=json.dumps(args or {}).encode(),
        headers={
            "Content-Type": "application/json",
            "x-api-key": key,
            "User-Agent": "strikerapi.com-examples/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            LAST_REMAINING = resp.headers.get("X-Credits-Remaining", LAST_REMAINING)
            return json.load(resp)
    except urllib.error.HTTPError as err:
        raise ApiError(describe(err, tool)) from None
    except urllib.error.URLError as err:
        raise ApiError(f"Network error calling {tool}: {err.reason}") from None


def describe(err, tool):
    try:
        body = json.loads(err.read().decode() or "{}")
    except ValueError:
        body = {}
    message = body.get("message") or body.get("error") or err.reason
    if err.code == 401:
        return f"401 unauthorized. Check {KEY_ENV}. {message}"
    if err.code == 402:
        upgrade = body.get("upgrade_url") or SIGNUP_URL
        return f"402 out of credits. {message} Upgrade or wait for the monthly reset: {upgrade}"
    return f"HTTP {err.code} from {tool}: {message}"


def fmt(value, digits=None):
    if value is None:
        return "-"
    if digits is not None and isinstance(value, (int, float)):
        return f"{value:.{digits}f}"
    return str(value)


def pct(value, digits=1):
    return "-" if value is None else f"{value * 100:.{digits}f}%"


def table(headers, rows):
    rows = [["-" if c is None else str(c) for c in r] for r in rows]
    widths = [max([len(h)] + [len(r[i]) for r in rows]) for i, h in enumerate(headers)]
    line = lambda cells: "  ".join(c.ljust(w) for c, w in zip(cells, widths)).rstrip()
    print(line(headers))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print(line(r))


def finish():
    if LAST_REMAINING is not None:
        print(f"\nCredits remaining: {LAST_REMAINING}")

def main():
    key = require_key()

    sched = call(key, "get_schedule", {"days": 7})
    games = sched.get("games") or []
    print("Upcoming fixtures (get_schedule, 2 credits)")
    if games:
        rows = []
        for g in games[:8]:
            line = g.get("line") or {}
            rows.append([
                g.get("date"),
                f"{g['home']['name']} v {g['away']['name']}",
                fmt(line.get("home_ml")),
                fmt(line.get("draw_ml")),
                fmt(line.get("away_ml")),
            ])
        table(["Date", "Fixture", "Home", "Draw", "Away"], rows)
    else:
        print("No fixtures in the next 7 days.")

    standings = call(key, "get_standings", {"season": 2025})
    print("\nLeague table, 2025-26, top 5 (get_standings, 2 credits)")
    table(
        ["#", "Club", "P", "W", "D", "L", "GD", "Pts", "Form"],
        [[t.get("rank"), t.get("display_name"), t.get("played"), t.get("wins"), t.get("draws"),
          t.get("losses"), t.get("goal_diff"), t.get("points"), t.get("form")]
         for t in (standings.get("standings") or [])[:5]],
    )
    finish()


if __name__ == "__main__":
    try:
        main()
    except ApiError as err:
        sys.exit(f"Error: {err}")
