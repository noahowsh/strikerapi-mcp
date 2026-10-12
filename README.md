# StrikerAPI MCP server

[![Smithery](https://img.shields.io/badge/Smithery-listed-ff5601?style=flat-square)](https://smithery.ai/servers/noahowsh/StrikerAPI) [![MCP Registry](https://img.shields.io/badge/MCP%20Registry-listed-0b7285?style=flat-square)](https://registry.modelcontextprotocol.io/v0/servers?search=io.github.noahowsh/strikerapi)

**The soccer data API.** Results, lineups, box scores and match events for 17 competitions, from the Premier League, MLS, La Liga, Serie A, the Bundesliga, Ligue 1 and the Champions League to the EFL Championship, the NWSL, Liga MX, the Europa League, the Conference League, the Eredivisie, the Primeira Liga, the Scottish Premiership, Brazil's Serie A and Argentina's Liga Profesional, with the location of every charted shot, our own expected goals and Elo ratings, sportsbook lines and anytime goalscorer prices. REST API and MCP server. 500 free credits every month, no card.

Website: https://strikerapi.com · Docs: https://strikerapi.com/docs · Get a key: https://strikerapi.com/signup

```
You:    "Which Premier League teams allowed the most xG from set pieces last season?"
Claude: [calls get_team_stats]

You:    "Show Arsenal's shot map against Chelsea in their last meeting."
Claude: [calls get_shot_map]

You:    "What was Erling Haaland's anytime goalscorer price at each sportsbook before his last match?"
Claude: [calls get_player_props]
```

## Skills

The [`skills/`](skills/) folder holds 16 Claude skills that turn Claude into a soccer analyst on top of these tools: match lookup, team and player analysis, odds comparison, xG and shot maps, Elo, Poisson and Dixon-Coles score models, three-way devigging, calibration, edge detection, backtesting and anytime goalscorer modeling. Each skill names the exact tools it calls and what they cost.

```bash
git clone https://github.com/noahowsh/strikerapi-mcp.git
```

Or install them as a Claude Code plugin:

```
/plugin marketplace add noahowsh/strikerapi-mcp
/plugin install strikerapi-skills@strikerapi
```

Or with the skills CLI: `npx skills add noahowsh/strikerapi-mcp`.

Then point Claude at the `skills/` folder (for Claude Code, copy or symlink the folders into `~/.claude/skills/`) and connect the server below. Start with `dispatch` if you are unsure which skill to use. Full catalog: [`skills/README.md`](skills/README.md).

## Quick start

This is a hosted (remote) MCP server over Streamable HTTP. There is nothing to install.

**Claude Code**

```bash
claude mcp add --transport http strikerapi "https://mcp.strikerapi.com/mcp?key=YOUR_API_KEY"
```

**Claude Desktop, Cursor and other clients**

```json
{
  "mcpServers": {
    "strikerapi": {
      "url": "https://mcp.strikerapi.com/mcp?key=YOUR_API_KEY"
    }
  }
}
```

The key can also be sent as an `x-api-key` header or `Authorization: Bearer`. Connecting and listing tools works without a key; calling a tool needs one.

**REST**

```bash
curl -X POST https://mcp.strikerapi.com/v1/list_teams -H "x-api-key: YOUR_API_KEY"
```

Every tool is `POST /v1/{tool}` with a JSON body.

## Examples

Runnable Python (standard library only) and Node 18+ (no dependencies) examples live in [`examples/`](examples/):

- [`examples/python/quickstart.py`](examples/python/quickstart.py) and [`examples/node/quickstart.mjs`](examples/node/quickstart.mjs): schedule plus a headline call.
- [`examples/python/soccer_shot_map_xg.py`](examples/python/soccer_shot_map_xg.py): One match, two views.

```bash
export STRIKERAPI_API_KEY=your_key
python3 examples/python/quickstart.py
node examples/node/quickstart.mjs
```

See [`examples/README.md`](examples/README.md) for details. Get a free key (500 credits a month, no card) at https://strikerapi.com/signup.

## Tools (19)

| Tool | What it returns |
|------|-----------------|
| `list_teams` | Club ids, abbreviations and colours for a season |
| `search_players` | Find players by name |
| `list_games` | Fixtures and results by season, stage, date, range or club |
| `get_schedule` | Upcoming fixtures with the median three-way line across sportsbooks |
| `get_standings` | The league table: points, deductions, goal difference, home and away, form |
| `get_ratings` | Our club Elo ratings, ranked |
| `get_head_to_head` | Two clubs' meetings: record, goals and every result |
| `get_game` | One match: score, both box scores, every player's line, key events, each book's line |
| `get_lineups` | Formations, starting XIs, benches and substitutions with minutes |
| `get_player` | Profile, per-season totals and per-90 rates, last 10 matches |
| `get_player_games` | A player's full match log |
| `get_leaders` | Season leaders: goals, assists, shots, xG, cards, saves |
| `get_team_stats` | Per-match averages: goals, xG, shots, possession, passing, discipline, for and against |
| `get_odds` | Every sportsbook's three-way moneyline, goal handicap and total for a match (5) or a day (10), with results |
| `get_events` | Match events: goals, cards, substitutions, shots with location and xG, fouls, corners |
| `get_shot_map` | Shot map for a club, player or defence: every located shot with outcome and xG, plus zone totals |
| `get_line_movement` | Snapshots of each sportsbook's line before kick-off |
| `get_player_props` | Anytime goalscorer prices by sportsbook, opening and closing |
| `get_prop_history` | A player's anytime goalscorer price against whether he scored, match by match |

Leagues: soccer (default, Premier League), mls, laliga, seriea, bundesliga, ligue1, ucl, championship, nwsl, ligamx, uel, uecl, eredivisie, primeira, scotland, brazil, argentina (pass `league` to any tool).

## Data

- Seventeen competitions through the same 19 tools: Premier League, MLS, La Liga, Serie A, Bundesliga, Ligue 1, Champions League, EFL Championship, NWSL, Liga MX, Europa League, Conference League, Eredivisie, Primeira Liga, Scottish Premiership, Brazil's Serie A and Argentina's Liga Profesional
- Results, lineups and goals from 2001-02 and shot locations from 2012-13 for the longest-covered leagues (start years differ by competition; coverage by season is on the docs page)
- League tables with deductions, goal difference, home and away and form; club Elo ratings; head to head
- Per-sportsbook three-way moneylines, goal handicaps and totals from 2017-18, densest (about ten books a match) from 2021-22 to 2023-24, one or two books since, plus opening and closing lines from The Odds API since June 2020 for 16 competitions; pre-match line snapshots from launch: ESPN's once a day, The Odds API's every hour for matches in the next two days
- Anytime goalscorer prices by sportsbook (the Yes price, and No where a book posts it; no other player market) for seven competitions: the Premier League and MLS from April 2024, Ligue 1 from May 2024, La Liga, Serie A and the Bundesliga from August 2024 and the Champions League from March 2025, from DraftKings and FanDuel with Pinnacle and William Hill on some matches in 2026; none for the other ten competitions

Coverage by season, read live from the database: https://strikerapi.com/docs

## Useful pages

- [Odds this week](https://strikerapi.com/odds): upcoming fixtures with the median three-way line
- [Guides](https://strikerapi.com/guides): Python walk-throughs for xG tables, shot maps, Elo, top scorers and odds history
- [Docs](https://strikerapi.com/docs): every tool, parameter and response, with coverage by season
- [Data](https://strikerapi.com/data): shot data, match events, historical odds and goalscorer prices
- [Pricing](https://strikerapi.com/pricing): free tier and plans
- [vs API-Football](https://strikerapi.com/compare/api-football-alternative)
- [vs football-data.org](https://strikerapi.com/compare/football-data-org-alternative)
- [vs Sportmonks](https://strikerapi.com/compare/sportmonks-alternative)
- [vs scraping FBref](https://strikerapi.com/compare/fbref-scraping)

## Pricing

500 free credits every month, no card. Plans: Starter $19/mo (10,000 credits), Pro $49/mo (30,000), Scale $149/mo (125,000). Wallet top-ups from $5, never expire. https://strikerapi.com/pricing

## Attribution

Soccer data from public ESPN data; sportsbook lines and goalscorer prices from ESPN and The Odds API. Expected goals and ratings are ours. Not affiliated with any league, club or federation.

## License

MIT for the contents of this repository. Data terms as above.
