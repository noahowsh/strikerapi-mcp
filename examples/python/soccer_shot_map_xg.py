#!/usr/bin/env python3
"""Soccer shot map and xG for one match, plus anytime goalscorer odds. Usage: python3 soccer_shot_map_xg.py [game_id]. Costs 20 credits (get_shot_map 10 + get_player_props 10)."""
import json
import os
import sys
import urllib.error
import urllib.request
import argparse
from statistics import median

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
            body = json.load(resp)
            # Every response is wrapped as {"data": ...}.
            return body.get("data", body) if isinstance(body, dict) else body
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

def implied(american):
    if american is None:
        return None
    return 100 / (american + 100) if american > 0 else -american / (-american + 100)


def main():
    ap = argparse.ArgumentParser(description="xG shot map and anytime goalscorer prices for one match.")
    ap.add_argument("game_id", nargs="?", default="740916",
                    help="match id from list_games or get_schedule (default: 740916, Man City v Arsenal)")
    ap.add_argument("--top", type=int, default=8, help="players to show in the odds table")
    args = ap.parse_args()
    key = require_key()

    smap = call(key, "get_shot_map", {"game_id": args.game_id, "include_shots": True})
    shots = smap.get("shots") or []
    totals = smap.get("totals") or {}
    print(f"Match {args.game_id}: {totals.get('shots')} shots, {totals.get('goals')} goals, "
          f"{fmt(totals.get('xg'), 2)} xG ({fmt(totals.get('xg_per_shot'), 3)} per shot)")

    by_team = {}
    for s in shots:
        t = by_team.setdefault(s.get("team"), {"shots": 0, "goals": 0, "xg": 0.0})
        t["shots"] += 1
        t["goals"] += 1 if s.get("outcome") == "goal" else 0
        t["xg"] += s.get("xg") or 0
    print("\nBy team")
    table(["Team", "Shots", "Goals", "xG"],
          [[team, v["shots"], v["goals"], fmt(v["xg"], 2)] for team, v in by_team.items()])

    print("\nBy zone")
    table(["Zone", "Shots", "Goals", "On target", "xG", "Share"],
          [[z.get("zone"), z.get("shots"), z.get("goals"), z.get("on_target"), fmt(z.get("xg"), 2),
            pct(z.get("share"), 0)] for z in smap.get("zones") or []])

    print("\nBiggest chances")
    table(["Min", "Team", "Player", "Outcome", "Zone", "xG"],
          [[s.get("minute"), s.get("team"), s.get("player"), s.get("outcome"), s.get("zone"), fmt(s.get("xg"), 2)]
           for s in sorted(shots, key=lambda s: s.get("xg") or 0, reverse=True)[:5]])

    props = call(key, "get_player_props", {"game_id": args.game_id}).get("props") or []
    players = {}
    for p in props:
        if p.get("over_odds") is None:
            continue
        players.setdefault(p["player_name"], []).append((p["over_odds"], p.get("bookmaker")))
    ranked = sorted(players.items(), key=lambda kv: median(o for o, _ in kv[1]))
    print("\nAnytime goalscorer, closing prices (American odds)")
    if not ranked:
        print("No goalscorer prices for this match.")
    else:
        table(["Player", "Median", "Implied", "Best", "Best book", "Books"],
              [[name, round(median(o for o, _ in quotes)), pct(implied(median(o for o, _ in quotes))),
                max(quotes)[0], max(quotes)[1], len(quotes)] for name, quotes in ranked[: args.top]])
    finish()


if __name__ == "__main__":
    try:
        main()
    except ApiError as err:
        sys.exit(f"Error: {err}")
