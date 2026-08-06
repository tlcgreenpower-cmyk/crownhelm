# Tidefall — build time log

Lee wants to know the game's total build time. Every session gets a row when it ends;
the TOTAL line is the whole game, all time. Historical rows (before this file existed)
were estimated from git commit clustering: commits < 75 min apart = one session, plus
30 min lead-in each. Git history starts 2026-07-31; any work before the repo existed
is not counted.

| Date       | Session                | Time  | Shipped |
|------------|------------------------|-------|---------|
| 2026-07-31 | 12:44–17:18 (est.)     | 5.1h  | early builds |
| 2026-08-01 | 04:01–06:35 (est.)     | 3.1h  | |
| 2026-08-01 | 16:39–18:58 (est.)     | 2.8h  | |
| 2026-08-02 | 04:32–07:11 (est.)     | 3.2h  | b62–b64 era: mines, map builder |
| 2026-08-02 | 13:11–14:15 (est.)     | 1.6h  | |
| 2026-08-02 | 16:00–18:02 (est.)     | 2.5h  | b65–b71: AoE pacing, counters, rams |
| 2026-08-03 | 03:25–05:20 (est.)     | 2.4h  | b72–b79: stone walls, diagonal walls |
| 2026-08-03 | 12:42–13:13 (est.)     | 1.0h  | |
| 2026-08-05 | ~08:29 (est.)          | 0.5h  | b80: real cavalry |
| 2026-08-05 | ~13:50 (est.)          | 0.5h  | CLAUDE.md |
| 2026-08-05 | 18:06–20:46 (est.)     | 3.2h  | b81–b91: China, Thebes, saves, AI towns |
| 2026-08-06 | 00:00–00:25            | 0.4h  | b92: mesh-merge surgery + TIMELOG |
| 2026-08-06 | ~07:55–ongoing         | 0.5h+ | b93: 8 realms, map sizes, builder overhaul, idle-peasant fix, Menu button |

**TOTAL: 26.7 hours** (as of 2026-08-06 08:20, morning session still running)
