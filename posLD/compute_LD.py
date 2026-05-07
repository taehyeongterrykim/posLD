import os
import spacy
import pandas as pd


def compute_LD(
    input_path,
    output_file="LD_results.csv",
    window_size=50,
    increment=1,
    spacy_model="en_core_web_lg",
    individual_output=True,
    form="lemma",
):
    """
    Compute Moving-Average Type-Token Ratio (MATTR) for all .txt files in a folder.

    input_path:        folder path containing .txt files to process (required)
    output_file:       CSV path to write results into (default: 'LD_results.csv')
    window_size:       number of tokens in each sliding window (default: 50)
    increment:         number of tokens to advance the window per step (default: 1)
    spacy_model:       spaCy model for POS tagging (default: 'en_core_web_lg')
                       alternatives: 'en_core_web_trf' (most accurate, requires spacy[transformers]), 'en_core_web_md', 'en_core_web_sm'
    individual_output: if True, writes a word list per text to an 'individual_output/' subfolder (default: True)
    form:              token form to compute MATTR on — 'lemma', 'surface', or 'both' (default: 'lemma')
    """
    if form not in ("lemma", "surface", "both"):
        raise ValueError("form must be 'lemma', 'surface', or 'both'")

    # Resolve output paths
    output_file = os.path.abspath(output_file)
    output_dir = os.path.dirname(output_file)
    individual_dir = os.path.join(output_dir, "individual_output")

    txt_files = [f for f in os.listdir(input_path) if f.endswith(".txt")]
    total_files = len(txt_files)

    if total_files == 0:
        print("No .txt files found in the input folder.")
        return pd.DataFrame()

    os.makedirs(output_dir, exist_ok=True)
    if individual_output:
        os.makedirs(individual_dir, exist_ok=True)

    print(f"Loading spaCy model '{spacy_model}'...")
    nlp = spacy.load(spacy_model)

    print(f"Found {total_files} text file(s). Starting processing...\n")
    results = []

    for i, filename in enumerate(txt_files, start=1):
        filepath = os.path.join(input_path, filename)
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()

        doc = nlp(text)
        (verbs_lemma, verbs_surface, nouns_lemma, nouns_surface,
         content_lemma, content_surface, all_lemma, all_surface) = _get_token_lists(doc)

        def mattr(tokens):
            result = _compute_mattr(tokens, window_size=window_size, increment=increment)
            return result if result is not None else "NA"

        row = {"filename": filename}

        use_lemma   = form in ("lemma", "both")
        use_surface = form in ("surface", "both")

        if use_lemma:
            row[f"MATTR({window_size})_all_lemma"]     = mattr(all_lemma)
            row[f"MATTR({window_size})_content_lemma"] = mattr(content_lemma)
            row[f"MATTR({window_size})_verb_lemma"]    = mattr(verbs_lemma)
            row[f"MATTR({window_size})_noun_lemma"]    = mattr(nouns_lemma)

        if use_surface:
            row[f"MATTR({window_size})_all_surface"]     = mattr(all_surface)
            row[f"MATTR({window_size})_content_surface"] = mattr(content_surface)
            row[f"MATTR({window_size})_verb_surface"]    = mattr(verbs_surface)
            row[f"MATTR({window_size})_noun_surface"]    = mattr(nouns_surface)

        results.append(row)

        if individual_output:
            _write_individual_output(doc, filename, individual_dir)

        print(f"[{i}/{total_files}] Finished: {filename}")

    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)

    print(f"\nDone! Results saved to: {output_file}")
    if individual_output:
        print(f"Individual output files saved to: {individual_dir}")

    return df


def _compute_mattr(tokens, window_size, increment):
    """Compute MATTR for a list of tokens. Returns None if not enough tokens for even one window."""
    if len(tokens) < window_size:
        return None
    ttr_values = []
    for i in range(0, len(tokens) - window_size + 1, increment):
        window = tokens[i:i + window_size]
        ttr = len(set(window)) / window_size
        ttr_values.append(ttr)
    return sum(ttr_values) / len(ttr_values)


def _get_token_lists(doc):
    """Extract 8 token lists (verb/noun/content/all x lemma/surface) from a spaCy doc.
    - Filters out non-alphabetic tokens from all lists.
    - Excludes the verb 'be' from verb and content lists.
    - Excludes proper nouns (PROPN) from noun and content lists; only common nouns (NOUN) are included."""
    verbs_lemma     = [t.lemma_.lower() for t in doc if t.pos_ == "VERB" and t.is_alpha and t.lemma_ != "be"]
    verbs_surface   = [t.text.lower()   for t in doc if t.pos_ == "VERB" and t.is_alpha and t.lemma_ != "be"]
    nouns_lemma     = [t.lemma_.lower() for t in doc if t.pos_ == "NOUN" and t.is_alpha]
    nouns_surface   = [t.text.lower()   for t in doc if t.pos_ == "NOUN" and t.is_alpha]
    content_lemma   = [t.lemma_.lower() for t in doc if t.pos_ in ("NOUN", "VERB", "ADJ", "ADV") and t.is_alpha and t.lemma_ != "be"]
    content_surface = [t.text.lower()   for t in doc if t.pos_ in ("NOUN", "VERB", "ADJ", "ADV") and t.is_alpha and t.lemma_ != "be"]
    all_lemma       = [t.lemma_.lower() for t in doc if t.is_alpha]
    all_surface     = [t.text.lower()   for t in doc if t.is_alpha]
    return verbs_lemma, verbs_surface, nouns_lemma, nouns_surface, content_lemma, content_surface, all_lemma, all_surface


def _write_individual_output(doc, filename, individual_dir):
    """Write a per-text output file containing the word list with POS tags."""
    out_path = os.path.join(individual_dir, os.path.splitext(filename)[0] + "_output.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("=== WORD LIST ===\n")
        for token in doc:
            if token.is_alpha:
                if token.pos_ in ("VERB", "NOUN") and token.lemma_ != "be":
                    f.write(f"{token.text} {token.pos_}\n")
                else:
                    f.write(f"{token.text}\n")
