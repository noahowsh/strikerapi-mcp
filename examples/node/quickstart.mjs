#!/usr/bin/env node
// StrikerAPI quickstart: upcoming Premier League fixtures with three-way prices, then the league table. Node 18+, no dependencies. Needs STRIKERAPI_API_KEY. Costs about 4 credits.
const BRAND = "StrikerAPI";
const KEY_ENV = "STRIKERAPI_API_KEY";
const BASE_URL = "https://mcp.strikerapi.com/v1";
const SIGNUP_URL = "https://strikerapi.com/signup";

const key = (process.env[KEY_ENV] || "").trim();
if (!key) {
  console.error(
    `Set ${KEY_ENV} first:\n  export ${KEY_ENV}=your_key\n` +
      `Get a free key (500 credits every month, no card): ${SIGNUP_URL}`,
  );
  process.exit(1);
}

let remaining = null;

async function call(tool, args = {}) {
  let res;
  try {
    res = await fetch(`${BASE_URL}/${tool}`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-api-key": key },
      body: JSON.stringify(args),
    });
  } catch (err) {
    throw new Error(`Network error calling ${tool}: ${err.cause?.code ?? err.message}`);
  }
  remaining = res.headers.get("x-credits-remaining") ?? remaining;
  const text = await res.text();
  let body = {};
  try {
    body = JSON.parse(text);
  } catch {}
  if (res.ok) return body;
  const message = body.message || body.error || res.statusText;
  if (res.status === 401) throw new Error(`401 unauthorized. Check ${KEY_ENV}. ${message}`);
  if (res.status === 402) {
    throw new Error(
      `402 out of credits. ${message} Upgrade or wait for the monthly reset: ${body.upgrade_url || SIGNUP_URL}`,
    );
  }
  throw new Error(`HTTP ${res.status} from ${tool}: ${message}`);
}

const fmt = (v, digits) => (v == null ? "-" : digits != null && typeof v === "number" ? v.toFixed(digits) : String(v));
const pct = (v, digits = 1) => (v == null ? "-" : `${(v * 100).toFixed(digits)}%`);

function table(headers, rows) {
  const cells = rows.map((r) => r.map((c) => (c == null ? "-" : String(c))));
  const widths = headers.map((h, i) => Math.max(h.length, ...cells.map((r) => r[i].length)));
  const line = (r) => r.map((c, i) => c.padEnd(widths[i])).join("  ").trimEnd();
  console.log(line(headers));
  console.log(widths.map((w) => "-".repeat(w)).join("  "));
  cells.forEach((r) => console.log(line(r)));
}

function finish() {
  if (remaining !== null) console.log(`\nCredits remaining: ${remaining}`);
}

async function main() {
  const sched = await call("get_schedule", { days: 7 });
  const games = sched.games ?? [];
  console.log("Upcoming fixtures (get_schedule, 2 credits)");
  if (games.length) {
    table(
      ["Date", "Fixture", "Home", "Draw", "Away"],
      games.slice(0, 8).map((g) => [
        g.date,
        `${g.home.name} v ${g.away.name}`,
        fmt(g.line?.home_ml),
        fmt(g.line?.draw_ml),
        fmt(g.line?.away_ml),
      ]),
    );
  } else {
    console.log("No fixtures in the next 7 days.");
  }

  const standings = await call("get_standings", { season: 2025 });
  console.log("\nLeague table, 2025-26, top 5 (get_standings, 2 credits)");
  table(
    ["#", "Club", "P", "W", "D", "L", "GD", "Pts", "Form"],
    (standings.standings ?? [])
      .slice(0, 5)
      .map((t) => [t.rank, t.display_name, t.played, t.wins, t.draws, t.losses, t.goal_diff, t.points, t.form]),
  );
  finish();
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
