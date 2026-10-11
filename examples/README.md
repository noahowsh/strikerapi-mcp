# StrikerAPI examples

Runnable examples for the [StrikerAPI](https://strikerapi.com). Python uses only the standard library (`urllib` and `json`). Node uses the built-in `fetch` (Node 18 or newer). No packages to install.

Soccer data API with xG, shot maps and odds. Every tool is a REST call: `POST https://mcp.strikerapi.com/v1/<tool_name>` with a JSON body and an `x-api-key` header. The same tools are available over MCP at `https://mcp.strikerapi.com/mcp`.

## Get a key

1. Sign up at https://strikerapi.com/signup. The free plan gives 500 credits every month, no card.
2. Copy a key from https://strikerapi.com/dashboard/keys.
3. Export it. The scripts read it from the environment and never print it.

```bash
export STRIKERAPI_API_KEY=your_key
```

## What is here

| File | What it does | Tools | Credits |
| --- | --- | --- | --- |
| `python/quickstart.py` | Upcoming schedule plus one headline call, printed as small tables | `get_schedule`, `get_standings` | about 4 |
| `python/soccer_shot_map_xg.py` | One match, two views. Shot map totals, xG by team and zone, and the five biggest chances, then anytime goalscorer closing prices across sportsbooks with the median, implied probability and best price. Defaults to match 740916 (Manchester City v Arsenal, Premier League 2025-26). | `get_shot_map`, `get_player_props` | about 20 |
| `node/quickstart.mjs` | Same as the Python quickstart, for Node | `get_schedule`, `get_standings` | about 4 |

## Run

```bash
python3 python/quickstart.py
python3 python/soccer_shot_map_xg.py
node node/quickstart.mjs
```

The use-case script takes optional arguments. For example:

```bash
python3 soccer_shot_map_xg.py 740916
```

Run any script with `--help` (Python) to see its options.

## Credits and errors

- Every call costs credits, priced per tool. The cost is shown next to each call in the script output, and the response header `X-Credits-Remaining` is printed at the end.
- To see what a call would cost without running it, send `"estimate_only": true` on the tools that accept it (see the tool schema).
- When you are out of credits the API returns HTTP 402 with `{"error": "insufficient_credits", "message": "...", "upgrade_url": "..."}`. The scripts print that message and the upgrade link.
- HTTP 401 means the key is missing or wrong. The scripts print a hint to check `STRIKERAPI_API_KEY`.
- The Premier League is the default. Pass `"league"` in the request body for MLS, La Liga, Serie A, Bundesliga, Ligue 1, the Champions League and 10 more.
- The tool list with input schemas is public: `curl https://mcp.strikerapi.com/v1/tools`.

## More

- Docs and example responses for every tool: https://strikerapi.com/docs
- Full reference in one file: https://strikerapi.com/llms-full.txt
- Free key: https://strikerapi.com/signup
