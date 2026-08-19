# Community Research Notes — Reddit access landscape (Aug 2026)

Source: r/hermesagent thread "What tool do you use to browse Reddit with Hermes"
(1vl4n44), read via Arctic Shift. Verified locally where possible.
Not a roadmap — candidates for review, each needs a policy call first.

## 1. Reddit blocks `.json` at the IP/ASN level (verified)

u/angaba1992's matrix (self-hosted LXC, matches our probe from this machine):

| Method                                | Result   |
|---------------------------------------|----------|
| `www.reddit.com/r/<sub>/.json` + custom UA | 403 |
| `old.reddit.com/...json` + full Chrome UA  | 403 |
| Headless browser (same datacenter IP) | blocked  |
| `old.reddit.com` HTML                 | 200 OK   |

Key claim: **it is not the User-Agent** — datacenter ASN ranges are blocked,
which also kills the "just use a browser tool" fallback on the same IP.
Residential IPs reportedly still reach `.json` fine.

Implication for us: our zero-config story already degrades on servers;
`old.reddit.com` HTML is the only direct path that survives datacenter IPs.
(Scraping HTML is also the most clearly non-compliant option — see
`docs` on the Responsible Builder Policy before building anything here.)

Parsing gotchas if ever attempted: `thing_t3_`/`thing_t1_` blocks carry
score/author/permalink; thread URLs need the full slug + trailing slash or
you parse a ~438-byte redirect stub; the search page uses entirely different
markup; parse title+permalink in one pass or they mis-pair.

## 2. Subreddit RSS as a listing source

u/Imaginary_Scarcity58: `old.reddit.com/r/<sub>/top/.rss?t=month` works for
top/week/month/new harvesting, **limit ~75 before 429s**. They collect links
via RSS, then extract comments per post another way.

Relevance: we already trust RSS for `get_saved_posts`. A subreddit-listing RSS
mode could give `analyze_niche_trends` a zero-config fallback path it
currently lacks (trends hard-fail without OAuth). Caveats: 75-item cap, RSS
redirect observed unanswered from this host, and same policy question as #1.

## 3. Arctic Shift is near-live (validates our fallback)

u/Square_Helicopter992: archive lag is "30 seconds to a minute" in practice.
Our `ARCHIVE_LAG_MESSAGE` ("scores may lag live Reddit") stays accurate but is
arguably over-conservative for freshness; keep as-is, but this is evidence the
fallback data quality is better than the message implies.

## 4. OAuth rejection for agentic apps is systemic

u/EvolvingDior (4 pts): "Reddit refuses API keys for agentic work." Others:
`.json` "randomly stopped working", rdt-cli 403 even with login cookies, one
PRAW success story. Our app rejection appears to be pattern, not our app
description. A re-application is likely futile without changing the app's
framing (see Responsible Builder Policy notes in PR history).

## 5. Session-based approaches (out of architecture, for awareness)

The dominant personal-use pattern in the thread: drive your own logged-in
browser (Chrome CDP, BRYG MCP, Playwright) from a desktop — nothing to
authenticate, survives markup changes; fails from VPS IPs (see #1).
Session-cookie + throwaway account was mentioned with ban risk. Not a fit for
our stdio server model; noted so we stop treating OAuth as the only "right"
path users compare us against.

## Not worth pursuing

- Alt frontends (redlib/safereddit instances) — third-party dependency,
  availability churn, same policy issues.
- Paid MCP wrappers (composio, socialrouter, Apify scraper) — commercial
  aggregation, opposite of our zero-config story.
