# Dev Workflow Chain

`/wbs` breaks a big idea into an EPIC/STORY backlog before either loop below
starts (see `../skills/wbs/SKILL.md`) — a draft in the personal wiki, not the
target repo. Each loop iteration then works one STORY at a time, and that
STORY's `/to-plan` is what actually materializes it into the target
project's `spec/`. `/wbs` never produces Task-level items itself.

Two loops share `/to-plan` and `/do-plan`:

1. **Feature/fix loop**: `/dev-grill-me` → `/to-plan` → `/do-plan`.
   `/do-plan` stops before merge/release and tells the user to run
   `/boy-scout`, which starts the cleanup loop below.
2. **Cleanup loop**: `/boy-scout` → `/to-plan` → `/do-plan`. This plan never
   asks for another `/boy-scout` — once its `/do-plan` finishes, resume the
   feature/fix plan that triggered it (its merge/release step), don't
   restart the chain.

`/to-plan` records, in every plan's "Next step" line, which loop it belongs
to: for a cleanup-loop plan, the feature/fix plan's file path to resume
next, and an explicit note that no further `/boy-scout` is needed; for a
feature/fix-loop plan, that `/boy-scout` runs after `/do-plan` stops before
merge/release. `/do-plan` reads that line back and acts on it when it
finishes.
