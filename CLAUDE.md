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

## Promises (the one place there *is* a relay)

`magick promise "<commitment>" --at <when>` is the exception to "no sync." It logs to `~/.magick/promises` (`{created} | {due} | {commitment}`, both UTC) **and** POSTs the promise to a Cloudflare Worker (`~/magick-worker/`) which, at the due time, sends a Web Push so the magick-pwa on the phone notifies. Config lives in env or `~/.magick/config`: `MAGICK_WORKER_URL`, `MAGICK_PROMISE_TOKEN`. The relay is best-effort — a failed POST never loses the local record. The PWA, CLI, and Worker share the promise shape: `{ commitment, dueAt }` with `dueAt` a UTC `YYYY-MM-DDTHH:MM:SSZ` string. Keep all three in step.
