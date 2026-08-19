# Dev Workflow Chain

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
