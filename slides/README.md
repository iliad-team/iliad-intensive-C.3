# Computational Mechanics teaching slides

This folder contains a reusable LaTeX Beamer template and an 18-slide Part 1 deck: a design adaptation of the original 17 slides, plus a requested example of Shai et al.'s belief-state geometry result after slide 12. The original files in `background_material/old_slides/CompMechSlidesPt1/` are untouched.

## Files

- `figures/hmm-cave.png` — unchanged labelled cave illustration from old Part 2, included after the intuitive HMM definition in Part 3.
- `CompMechSlidesPt3.tex` and `CompMechSlidesPt3.pdf` — Part 3 in progress, “Representing the past” (working title), matching the existing Beamer style. Contains a title, outline, opening motivation slide, and the original two-component HMM introduction. The planned HMM sequence follows the old deck: intuition, cave illustration, formal definition, word probabilities, then examples. The editable `figures/z1r-generator.tex` diagram is retained for the later example slide. Source comments record the agreed progression through HMMs, beliefs, minimality, and the transformer belief-geometry reading session; GHMMs remain optional. Build with `make pt3`.
- `CompMechSlidesPt1.pdf` — the presentation, in the original 16:9 format.
- `CompMechSlidesPt1.tex` — editable presentation source.
- `CompMechSlidesPt2.tex` and `CompMechSlidesPt2.pdf` — Part 2, “Predicting the future”, with a title slide, a blank “Outline” slide, the prediction setup, formal definitions of statistics and sufficiency (“Condensing the past”), separate “Sufficient statistics” and “Minimal sufficient statistics” slides, and a finite-history definition of causal states.
- `figures/causal-state-bottleneck.tex` — editable TikZ diagram grouping predictively equivalent pasts into one causal state.
- `figures/causal-states-intuition.tex` — editable TikZ diagram showing distinct histories with the same future distribution collected into one causal state.
- `figures/sufficient-not-minimal.tex` — an editable variant showing how a sufficient summary can keep unnecessary distinctions between pasts.
- `figures/minimal-summary.tex` — the merged version of that example, preserving the predictive distribution with one summary value.
- `iliad-slides.sty` — the reusable style, independent of course content.
- `template.tex` and `template.pdf` — a four-slide starter illustrating prose with evidence, equations with assumptions, and an aligned table.
- `CompMechPt1-reader.tex` and `CompMechPt1-reader.pdf` — a four-page A4 reading companion, organised as a document rather than slide thumbnails.
- `figures/` — byte-for-byte copies of the ten original PNG figures and the supplied Shai et al. schematic.
- `Makefile` — builds the three decks, reader, and starter-template PDFs.
  Intermediate files go in `build/`.

## Design basis

The reference is Edward R. Tufte, *The Cognitive Style of PowerPoint: Pitching Out Corrupts Within*, second edition, Graphics Press, 2006, supplied in `background_material/slide_design/`. Page references below use its printed page numbers.

Tufte does not prescribe a LaTeX slide theme. He argues that the medium and its conventions can degrade reasoning, and recommends illustrated written reports for serious communication. This template is a practical adaptation of those principles to teaching with projected slides, supported by a reading companion. Switching software or choosing a restrained appearance does not by itself satisfy the argument.

**Keep related evidence in view (pp. 4–6).** The statistical-mechanics and computational-mechanics examples remain on the same slide. The speculation now sits beside the Pareto diagram instead of covering it. The reading companion brings material from several slides into one view. The template adds no reveals, automatic section-divider slides, or transitions.

**Preserve statements, relationships, and qualifications (pp. 10–13, 17–18).** Explanatory text uses sentences and short paragraphs. Genuine sequences, such as the course plan, retain numbering. The original “Wild Speculation” qualification remains visible at body size. The template provides a separate command for qualifications and a smaller source line; substantive limitations belong in the former, never hidden in the latter.

**Let evidence determine the layout (pp. 21–25).** The four architecture sizes share a table with a common parameter heading. The template does not impose a fixed word count, bullet count, or number of panels. Figures retain their aspect ratios. No evidence is cropped, covered, or replaced with decorative imagery.

**Use space for the subject (pp. 4, 16, 24–27).** White backgrounds, dark text, modest headings, a single muted accent, and a small page number provide orientation. There are no logos on every page, banner systems, shadows, or decorative boxes. Serif text and matching mathematics are practical typography choices, not claims about a font prescribed by Tufte.

**Provide a lasting reading document (pp. 6, 27, 31).** The four-page reader allows participants to revisit the argument at their own pace. It is an introduction drawn from the existing deck, not a new technical report or an independently sourced literature review. It can be printed on A4, or imposed as an A3 booklet using a printer's booklet option. A fuller technical reader can grow alongside the later course material.

## What changed in Part 1

All 17 original slides remain in their original relative order. Their body claims, numerical values, named people, questions, examples, and ten figure assets are retained. Titles were made more specific where the old deck repeated a broad section heading. Underlining became bold emphasis, paragraph layout replaced unnecessary bullets, and the architecture list became an editable table. Punctuation and presentation casing were lightly normalised.

Slide 10 no longer repeats the sentence “This naturally leads to a hierarchy” above the figure, because that same sentence is already written inside the unchanged figure. Original slide 14 (now 15) preserves the complete speculation and displays it alongside the unobscured diagram. The two research-frontier slides remain separate to preserve the existing teaching sequence.

New slide 13, “Example: belief state geometry”, uses the user-supplied schematic without cropping or alteration. It summarises the affine readout result in Shai et al., *Transformers Represent Belief State Geometry in their Residual Stream*, NeurIPS 2024, Sections 2.3 and 3 ([paper](https://arxiv.org/abs/2405.15943)). The finding is scoped to transformers trained on HMM sequences. Speaker notes distinguish the fitted readout from the transformer itself and explain that the diagram is a schematic. The reading companion still covers the original 17-slide material.

The presentation title slide now identifies Xavier Poncini (Simplex) and dates the course Autumn 2026. The historical statements remain as supplied from Spring 2026. In particular, the program age, model sizes, capability-scale claims, and named Q&A plans have not been updated or independently re-evaluated. The reading companion retains the original Spring 2026 context.

## Reuse and build

From this directory:

```sh
make all
```

Or build a single deliverable:

```sh
make slides
make pt2
make reader
make template
```

Requirements: a LaTeX installation with pdfLaTeX, latexmk, Beamer, Latin Modern, microtype, booktabs, tabularx, graphicx, and the standard AMS packages. Part 2 also uses TikZ and its arrows.meta library. The reader also uses geometry and fancyhdr. The project builds with the installed TeX Live 2025 distribution, without external fonts, downloads, or shell escape.

For a new module, copy `template.tex`, keep `iliad-slides.sty` beside it, and edit the metadata and frames. If using Overleaf, upload this folder and select the desired `.tex` file as the main document, using pdfLaTeX. Compilation can also be done directly by running pdfLaTeX twice on the selected file.

The style uses a 160 × 90 mm page, 12 pt body text, 19 pt slide titles, and 8 mm side margins. These are Beamer's physical-page units: the page is enlarged for projection. Some denser frames use 10.95 pt body text. Check readability on the actual room's projector before teaching, particularly the small labels embedded in the supplied figures.

Useful commands:

```tex
\keyterm{optimal prediction}       % restrained bold emphasis
\slidelabel{Interpretation}        % a direct accent-coloured label
\evidenceimage[46mm]{figure.pdf}    % bounded size, preserved aspect ratio
\qualification{Assumption or limitation that changes the conclusion.}
\source{Author, title, year, page or figure, DOI or stable URL.}
```

Use ordinary Beamer columns, equations, and tables as needed. Avoid `shrink` and automatic builds. For overly dense content, reconsider its organisation and use the reader for derivations and detail. Keep important qualifications visible in both formats. The presentation and reader are separate editable sources, so update both when the content changes.

## Source limitations

The inherited diagrams are PNGs with embedded handwriting and text. They remain images, while surrounding prose, mathematics, and tables are editable LaTeX. Retaining them preserves the supplied figures but also preserves their small labels and image resolution. The original credits “Yuvan et al.” and “Shai et al.” are retained inside the comparison figures. The supplied Part 1 source does not give full bibliographic details; none have been invented.

The licensed Tufte essay is used as a local design reference and is not copied into this deliverable.
