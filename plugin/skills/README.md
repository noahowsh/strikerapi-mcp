# StrikerAPI skills

Sixteen Claude skills that turn Claude into a soccer analyst wired to the StrikerAPI tools. Each skill is a folder with a `SKILL.md`: when to use it, which tools it calls and what they cost, the method (formulas, pitfalls, sample-size warnings), a worked example and an output format. Skills also work on your own CSV or JSON files; no API key is needed for that.

## Use them

```bash
git clone https://github.com/noahowsh/strikerapi-mcp.git
```

Point Claude at the `skills/` folder (for Claude Code, copy or symlink the folders into `~/.claude/skills/` or a project's `.claude/skills/`), then connect the data:

```bash
claude mcp add --transport http strikerapi "https://mcp.strikerapi.com/mcp?key=YOUR_API_KEY"
```

Free tier: 500 credits every month, no card. Keys at https://strikerapi.com/signup, plans at https://strikerapi.com/pricing. Start with `dispatch` if you are unsure which skill fits.

## Catalog

| Skill | Category | What it does |
|-------|----------|--------------|
| [`match-lookup`](match-lookup/SKILL.md) | Data Exploration | Fixtures, results, box scores, lineups and match events |
| [`team-analysis`](team-analysis/SKILL.md) | Data Exploration | Table, form, home and away splits, xG for and against |
| [`player-scouting`](player-scouting/SKILL.md) | Data Exploration | Per-90 profiles, leaders, match logs and finishing against xG |
| [`odds-explorer`](odds-explorer/SKILL.md) | Data Exploration | Three-way prices, best book, margin and line movement |
| [`xg-analysis`](xg-analysis/SKILL.md) | Soccer Analytics | Shot maps, xG tables, expected points and finishing |
| [`elo-ratings`](elo-ratings/SKILL.md) | Soccer Analytics | Club Elo ratings, win probabilities and custom Elo builds |
| [`poisson-score-models`](poisson-score-models/SKILL.md) | Soccer Analytics | Poisson and Dixon-Coles scorelines, totals and handicaps |
| [`odds-analysis`](odds-analysis/SKILL.md) | Methodology | Three-way devigging with proportional, power and Shin methods |
| [`walk-forward-validation`](walk-forward-validation/SKILL.md) | Methodology | Leak-free splits, point-in-time features, RPS against the close |
| [`probability-calibration`](probability-calibration/SKILL.md) | Methodology | Per-class reliability, RPS and scaling for home/draw/away |
| [`edge-detection`](edge-detection/SKILL.md) | Betting | Model against devigged market, EV, fractional Kelly and CLV |
| [`backtesting`](backtesting/SKILL.md) | Betting | Strategy tests at real opening and closing prices |
| [`goalscorer-prop-modeling`](goalscorer-prop-modeling/SKILL.md) | Betting | Anytime goalscorer probabilities against sportsbook prices |
| [`match-preview`](match-preview/SKILL.md) | Workflow | One-fixture preview: form, xG, Elo, head to head and the line |
| [`strikerapi-tool`](strikerapi-tool/SKILL.md) | Infrastructure | All 19 tools, credits, REST and MCP access, the data envelope |
| [`dispatch`](dispatch/SKILL.md) | Infrastructure | Routes a request to the right two or three skills |

## Conventions

- Every tool name, parameter and credit cost in these files comes from the live StrikerAPI tool catalog. Each skill has a "Commands That Do NOT Exist" table for tools people expect but that are not there (injuries, in-play, other player props).
- Soccer prices are three-way. Skills always handle home, draw and away together, and devig all three.
- Responses are wrapped as `{"data": ...}`. See `strikerapi-tool`.
- Anytime goalscorer prices exist for the Premier League, MLS, La Liga, Serie A, the Bundesliga, Ligue 1 and the Champions League only.
- Betting skills describe estimates. They warn about variance, sample size and closing-line value, and they do not promise returns.

## Credits

Typical costs: a match box score 5, a league xG table 5, a one-match preview about 20, a season of closing prices for one league 2 credits per match (760 for 380 matches). Skills state the cost before any loop.

Data: expected goals and ratings are StrikerAPI's own. Not affiliated with any league, club or federation. MIT licensed.
