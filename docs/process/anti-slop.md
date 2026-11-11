# Anti-slop: optional help for code style (moved out of the rulebook 2026-11-11; reviewers may cite it, it is not a rule)

The gate and the review are the loop; these rules are cheap help, not a substitute. Each is "bad -> good".
- Dispatch on data, not on chains. `if op == "add" {..} else if op == "sub" {..}` -> `match op { Op::Add => .., Op::Sub => .. }`
  over an enum parsed once at load. A string compared in more than one place is an enum that was never declared.
- State as one enum, not several flags. `done: bool, failed: bool, pending: bool` -> `enum State { Pending, Done, Failed }`.
- No silent defaults on failure paths. `map.get(k).unwrap_or_default()`, `.unwrap_or(0)`, `except Exception: return False`,
  `if (!p) return;` -> return an error that names the missing thing, or `assert` the invariant and delete the branch.
- Named predicates. `if a && (b || !c) && d.len() > 3 && ..` repeated -> `fn is_live_region(..) -> bool` with one owner.
- No magic numbers. `if width > 128` -> `const MAX_INLINE_WIDTH: u32 = 128;` next to the rule that needs it, with the spec section.
- One altitude per function. A function that parses bytes AND decides policy is two functions. Over 300 lines in semantics-bearing
  code is a review finding (plan target); split into named phases, each with a unit test, behaviour byte-identical.
- Delete, don't wrap. A helper called once, a wrapper that renames its callee, a `_v2` beside a `_v1`, a flag nobody sets: delete.
- No identifiers from the process in the product. Bead ids, job names, review round numbers, "shift 6", session dates: not in
  source comments, error strings, emitted output or fixture names. Test names and docs/reviews may carry them.
- No litter. Nothing under `__pycache__`, `*.pyc`, `*.log`, `LAST-RUN*`, `PROGRESS*`, lock files, `.darc` backups, scratch
  scripts or scratch markdown is ever committed. Stale markdown is polluted context for the next agent: keep HANDOFF/README
  statements true or delete them.
- A test must be able to see the bug it names. Tolerances no wider than the oracle allows; fixtures large enough to reach the
  branch; an assertion in every test; expected values hand-derived or from an independent oracle, never copied from the output
  of the code under test.

