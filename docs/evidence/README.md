# Evidence retention

On 2026-11-02 the user requested removal of generated CSV and TXT system dumps. Those exports were removed from the maintained phase records and project-local output directories. Their direct documentation links were removed as well.

Concise JSON measurements, execution summaries, figures, source/configuration identities and needed native simulator recordings remain. Historical manifests can still name an original CSV/TXT path and hash: that records its provenance, not a claim that the export is still present. Earlier execution evidence is unchanged; this cleanup does not rerun or requalify any flight.

Dependency locks, build/source files and dependency/vendor data are inputs and remain in place. The maintained L13/L14 analyzers now produce summaries and figures without CSV/TXT exports. Older ad hoc local scripts describe earlier workflows and may require export regeneration if explicitly reused.

The existing L13/L14 analyzers were rerun offline after cleanup. Their summaries and figures were byte-identical, and no CSV/TXT exports were recreated. Markdown links to the removed files and the scoped whitespace check passed. No flight or firmware build was rerun.
