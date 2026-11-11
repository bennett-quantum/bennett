# bennett

## What this repo is

The thin meta repo of the Bennett ecosystem: README index of the 13 repositories, manifest.toml (path, language, depends_on, pinned), and a clone/update script. No shared code lives here.

## Where the spec is

North star: `docs/Bennett-NorthStar.md`. ISA: `../bennett-isa-spec/spec/` (0.9 published beside 0.8; consumers migrating; each repo's
`SPEC_VERSIONS.toml` and gate.toml pins say which it uses). Dialect: `../bennett-dialect-spec/spec/` (versions per its
`SPEC_VERSIONS.toml`). Current state and the demo ladder: `HANDOFF.md`.

## Rules

The one rulebook is [docs/process/COMMON.md](docs/process/COMMON.md); it binds here. This repo's gate is `scripts/pre-push`
(`python3 -m unittest discover tools/tests`); install hooks with `scripts/install-hooks.sh`.
Tasks: `bd` (`bd prime` lists its commands).
