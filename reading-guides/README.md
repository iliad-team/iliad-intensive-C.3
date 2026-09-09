# Reading guides

This folder contains the reusable LaTeX style for guided paper sessions, a
starter document, and the Part 4 reading guide.

- `iliad-reading-guide.sty` defines the shared A4 layout, course metadata,
  title treatment, session summary, reading entries, and reading-route labels.
- `template.tex` is a compiling specimen to copy when starting a new guide.
- `CompMechReadingGuidePt4.tex` ports the supplied belief-geometry guide into
  the visual and terminological system used by the slides and exercise sheets.

To build the guide and the specimen template with a LaTeX installation and
`latexmk`:

```bash
make
```

The PDFs are written to `../output/pdf/`.
