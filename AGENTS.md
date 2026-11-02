# FeatherLane AI Auto Drone working instructions

Read `README.md`, `docs/PROJECT-DIRECTION.md`, `docs/ROADMAP.md`, `docs/MASTER-LEARNING-PLAN.md` and `docs/phases/registry.json` before implementation. This folder is a new ArduPilot/macOS project; do not inherit the unrelated FeatherLaneFlight project's PX4 phase dispatch or convert that checkout.

- Learning-first execution (user decision, 2026-10-31): work one focused Lxx phase from the master plan/card at a time. Explain the concept before code, predict the observable result, keep edits to one behavior/integration slice, retain actual evidence and a rollback, and split unfamiliar independent work into another card. Pxx IDs are capability milestones, not single implementation sessions. Registry data and the reusable templates generate the master/card documents through `scripts/render-learning-plan.py`.
- Work only on the user-authorized scope. Initial setup here is documentation; no flight implementation or physical operation is authorized by the plan alone.
- ArduPilot and macOS are the confirmed direction. Keep SkyDive screen/input control separate from ArduPilot/MAVLink simulation; never imply an unqualified bridge exists.
- Mission capabilities are selected per mission/step (user clarification, 2026-10-31). Coordinate/route missions do not require a target detector. Object-dependent missions select qualified target perception/localization; helicopter is an example, not a hardcoded core dependency or a promise of universal recognition.
- Native mission execution is the confirmed direction (user decision, 2026-10-31): maintain our own ArduPilot-derived code with bounded C++ in-flight mission logic/supervision inside the autopilot runtime. Reuse upstream controllers, estimation and failsafes. External Python is for UI/API tooling, simulator sessions, perception and other separately qualified compute; it must not be the authoritative flight mission state machine for the ArduPilot path. Exact native module/mode names and message contracts remain design proposals.
- Maintain custom firmware changes as identifiable commits against a pinned upstream revision/submodule set. Review upstream updates in an integration branch and requalify the selected build before adoption; do not blindly track upstream or automatically deploy updates. Measure end-to-end latency and scheduler load before claiming improvement. Keep blocking inference, browser calls and slow I/O outside time-sensitive flight callbacks.
- Distinguish proposed, implemented, observed and independently verified behavior. Keep simulator truth out of claimed sensor-only autonomy inputs.
- Keep control and supervision local and independent of browser rendering or slow model calls. Record stale/invalid data rather than fabricating state.
- Before application UI integration, show a working interactive preview using the intended React/MUI components and theme; wait for explicit approval of the shown scope. Static images and diagrams are not UI approval. Remove obsolete preview scaffolding after integration.
- Keep one maintained core architecture in `docs/architecture/`: README, rendered `ardupilot-code-stack.html` and editable `ardupilot-code-stack.json`. Update this core instead of accumulating competing overviews. Put teaching walkthroughs under `docs/guides/`, learning diagrams with phase docs, and generated receipts/review history under ignored `.archify/` or `.local/`.
- Use the installed Archify skill for new/material architecture proposals. Keep editable sources and rendered diagrams linked from `docs/architecture/README.md`; record actual approval source/date/scope when approved.
- Do not create or modify automated tests, snapshots or test scaffolding unless explicitly requested. Run appropriate existing checks and manually exercise relevant behavior. Report actual evidence and limitations.
- Keep generated CSV/TXT execution dumps out of maintained evidence by default (user decision, 2026-11-02). Retain concise summaries, figures and needed native recordings; preserve source/build files and dependency locks. Create exports only when explicitly requested.
- Use C++ for the native ArduPilot mission extension; prefer Python/uv for external tooling/perception and TypeScript/pnpm for the console. Qualify/pin compatible simulator and autopilot versions before documenting a setup as working.
- Preserve the existing SkyDive prototype, FeatherLaneFlight checkout and unrelated private files. Do not copy weights or credentials without scoped need.
- Network reads are allowed for research. Publishing, pushing, purchases, remote resource changes and physical operations require their own authorization. Do not initialize/publish a repository merely because documentation exists.

## Match the repository's code style

Read neighboring code and the repository's formatter/compiler settings before editing. Follow the surrounding author's conventions for the touched code; keep unrelated upstream code as it is.

- Use descriptive parameter and local names, such as `request` and `context`, rather than unexplained single letters outside established mathematical or loop conventions.
- Give protocol versions and operating limits clear names. Follow nearby constant conventions; use unit suffixes such as `_M` and `_MPS` for physical limits and retain exact values and boundary semantics during readability refactors.
- Use the repository's indentation, brace style and supported language version. Keep multiline lists one entry per line, and separate logical validation/result groups with blank lines.
- Add short comments where they explain purpose, units, bounds, protocol requirements or state/authority decisions. Keep comments beside the relevant check and consistent with the code; avoid narrating obvious syntax.
- Prefer explicit, readable field mapping and focused guard clauses. Keep conditional build-library selection easy to read without changing which targets include a feature.
- Review the scoped diff and run the relevant existing checks/build. Distinguish readability-only edits from behavior changes and preserve earlier execution evidence when source/build identities change. Do not add automated tests without the user's explicit request.

Update the roadmap, decisions, phase status and diagrams consistently. Approval of a design does not mean it has been implemented or deployed.
