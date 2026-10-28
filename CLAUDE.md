# bennett

## What this repo is

The thin meta repo of the Bennett ecosystem: README index of the 13 repositories, manifest.toml (path, language, depends_on, pinned), and a clone/update script. No shared code lives here.

## Where the spec is

North star: Bennett-NorthStar.md section 6.1 (currently in the Bennett.jl repo). Bennett-NorthStar.md, Bennett-ISA-Spec.md and tools/council.py will MOVE here once the ISA spec reaches council consensus.

## Non-negotiables

0. **Maintain the worklog.** Every session, prepend a `## Session log - YYYY-MM-DD - ...` block to the highest-numbered chunk under `worklog/` (`ls worklog/ | sort -r | head -1`). Past ~280 lines, start a new chunk with the next `NNN_` prefix. Record gotchas, surprises and root causes.
1. **Fail fast, fail loud.** Assertions and explicit errors, never silent returns or quiet fallbacks.
2. **One implementer per change.** Code review is batched over accumulated diffs, not per change.
3. **Red-green TDD.** Write the test, watch it fail, make it pass, then refactor.
4. **Exhaustive verification** against the spec's conformance suite for the spec versions declared in `SPEC_VERSIONS.toml` (where present). "Runs without errors" is not a pass.
5. **Coupled to other repos ONLY through published specs.** Never share code across a contract boundary; if you need to, the boundary is wrong.
6. **NO GitHub CI, NO remote automation.** Quality gates are local: `scripts/pre-push` runs the tests (install with `scripts/install-hooks.sh`).
7. **Task tracking:** use beads (`bd`) once initialised. Until then a TODO.md is forbidden; file issues under "open items" in the worklog.
8. **Skepticism.** Verify and reproduce; distrust subagent output, earlier agents' claims and your own assumptions.
