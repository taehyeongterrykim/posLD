# posLD

`posLD` provides a Python function `compute_LD` to compute a measure of lexical diversity (**Moving-Average Type-Token Ratio; MATTR**) across part-of-speech categories (verb and noun) for corpus linguistics research.

---

## Desktop App

A standalone desktop app is available for Mac and Windows. Click the link for your operating system below to download:

| Platform | File |
| --- | --- |
| macOS (M1/M2/M3, macOS 10.15+) | [posLD_mac.zip](https://drive.google.com/file/d/1WoB9ql-k4h0V1iag6_LMxBkBBWYYRRZ6/view?usp=sharing) → unzip → double-click `posLD.app` |
| Windows (64-bit, Windows 10+) | [posLD_windows.zip](https://drive.google.com/file/d/1IIAKQIijlWY1kOSM6fZvaW-ggBs5s5xw/view?usp=sharing) → unzip → double-click `posLD.exe` |

**Note for Mac users:** If you see a security warning, right-click the app → **Open** → **Open**.

**Note for Windows users:** Keep `posLD.exe` and the `_internal/` folder in the same location. The app will not run without both.

---

## Install and Usage

> **Note:** This section is for users who want to use posLD as a Python package (e.g., in a script or termianl).

First, install the package using pip:

    pip install posLD

You will also need a spaCy English model. The default is `en_core_web_lg`:

    python -m spacy download en_core_web_lg

Other available models and installation instructions: https://spacy.io/usage

Once installed, import the package and call the function, replacing `"path/to/your/folder"` with the full path to your folder containing `.txt` files:

    import posLD

    posLD.compute_LD(input_path=r"path/to/your/folder")

---

## Function Arguments

| Argument | Required | Description |
| --- | --- | --- |
| `input_path` | **Yes** | Folder containing `.txt` files to process |
| `output_file` | No | Path/name of the output CSV file. Defaults to `"LD_results.csv"` |
| `window_size` | No | Number of tokens in each sliding window. Defaults to `50`. Texts shorter than this receive `NA` |
| `increment` | No | Number of tokens to advance the window per step. Defaults to `1` |
| `spacy_model` | No | spaCy model for POS tagging. Defaults to `"en_core_web_lg"`. Alternatives: `"en_core_web_sm"`, `"en_core_web_md"`, `"en_core_web_trf"` |
| `individual_output` | No | If `True`, writes a word list per text to an `individual_output/` subfolder. Defaults to `True` |
| `form` | No | Token form to compute MATTR on: `"lemma"`, `"surface"`, or `"both"`. Defaults to `"lemma"` |

### Examples

    # Defaults: lemma form, window size 50, increment 1, en_core_web_lg
    posLD.compute_LD(input_path=r"path/to/your/folder")

    # Surface form only
    posLD.compute_LD(input_path=r"path/to/your/folder", form="surface")

    # Both lemma and surface, custom window size and increment
    posLD.compute_LD(input_path=r"path/to/your/folder", form="both", window_size=100, increment=5)

---

## CLI Arguments

You can also run posLD directly from the terminal, replacing `"path/to/your/folder"` with the full path to your folder containing `.txt` files (use quotes around the path, especially if it contains spaces):

    posLD "path/to/your/folder"

| Argument | Required | Description |
| --- | --- | --- |
| `input_path` | **Yes** | Path to folder with `.txt` files |
| `-o`, `--output` | No | Output CSV filename (default: `LD_results.csv`) |
| `-w`, `--window-size` | No | Sliding window size (default: `50`) |
| `-i`, `--increment` | No | Window increment (default: `1`) |
| `-m`, `--model` | No | spaCy model to use (default: `en_core_web_lg`) |
| `-f`, `--form` | No | Token form: `lemma`, `surface`, or `both` (default: `lemma`) |
| `--no-individual` | No | Skip writing individual output files |

### Examples

    # Defaults
    posLD "path/to/your/folder"

    # Surface form, window size 100
    posLD "path/to/your/folder" -f surface -w 100

    # Both forms, custom output
    posLD "path/to/your/folder" -f both -o results/LD_results.csv

---

## Features

- Accepts a folder of `.txt` files
- Computes MATTR using a sliding window over tokens
- Excludes non-alphabetic tokens from all calculations
- Excludes the verb *be* from verb and content word lists
- Excludes proper nouns from noun and content word lists
- Reports `NA` when a text has fewer tokens than the window size

Computes MATTR for four token categories (columns depend on the `form` argument):

| Category | Includes | Excludes |
| --- | --- | --- |
| `all` | All alphabetic tokens | — |
| `content` | Common NOUN, VERB (excl. *be*), ADJ, ADV | Proper nouns, *be* |
| `verb` | VERB only | *be* |
| `noun` | Common NOUN only | Proper nouns |

---

## Output CSV Columns

Columns included depend on the `form` argument. With `form="lemma"` (default):

| Column | Description |
| --- | --- |
| `filename` | Name of the input `.txt` file |
| `MATTR(N)_all_lemma` | MATTR over all lemmatized tokens |
| `MATTR(N)_content_lemma` | MATTR over content word lemmas |
| `MATTR(N)_verb_lemma` | MATTR over verb lemmas |
| `MATTR(N)_noun_lemma` | MATTR over noun lemmas |

With `form="surface"`, the same four columns appear with `_surface` instead of `_lemma`. With `form="both"`, all eight columns are included.

*N = the window size used (default 50)*

---

## Individual Output Files

When `individual_output=True` (the default), a subfolder `individual_output/` is created next to your CSV. Each `.txt` file produces a corresponding `_output.txt` containing a **word list** — all tokens in original order, with VERB and NOUN POS tags shown.

---

## License

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

---

## Citation

If you use **posLD** in your research, please cite it as (To be updated)
