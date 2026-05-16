# magick — agent notes

Python CLI for casting intents. See [`README.md`](README.md) for user-facing docs and the code structure rundown.

## Sibling project

There's a PWA companion at `~/magick-pwa/` (separate repo, vanilla JS). Same ritual, on the phone. The two are **independent**: no shared dependency, no sync, separate data stores (CLI writes to `~/.magick/logofcasts`; PWA uses IndexedDB on the device). If a user says "magick" without context, ask whether they mean this CLI or the PWA.

## Shared invariant (loose coupling)

The PWA mirrors this CLI's log shape on purpose — so a future export feature can write one place and read the other without translation:

- Timestamp: `YYYY-MM-DDTHH:MM:SSZ` (second-precision UTC). Produced by `datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")` in `magick/cast.py`.
- Log line: `"{timestamp} | {intent}\n"`.
- Confirmation echoed to stdout: `the spell is cast for "{intent}". Godspeed.`

If you change any of these, update `~/magick-pwa/` to match, or accept that an export feature later will need a translator.
