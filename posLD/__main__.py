import argparse
from .compute_LD import compute_LD

def main():
    parser = argparse.ArgumentParser(description="Compute LD for a folder of .txt files.")
    parser.add_argument("input_path", help="Path to folder with .txt files")
    parser.add_argument("-o", "--output", default="LD_results.csv", help="Output CSV filename (default: LD_results.csv)")
    parser.add_argument("-w", "--window-size", type=int, default=50, help="Sliding window size (default: 50)")
    parser.add_argument("-i", "--increment", type=int, default=1, help="Window increment (default: 1)")
    parser.add_argument("-m", "--model", default="en_core_web_lg", help="spaCy model (default: en_core_web_lg)")
    parser.add_argument("-f", "--form", choices=["lemma", "surface", "both"], default="lemma",
                        help="Token form: 'lemma', 'surface', or 'both' (default: lemma)")
    parser.add_argument("--no-individual", action="store_true", help="Skip writing individual output files")

    args = parser.parse_args()
    compute_LD(
        input_path=args.input_path,
        output_file=args.output,
        window_size=args.window_size,
        increment=args.increment,
        spacy_model=args.model,
        individual_output=not args.no_individual,
        form=args.form,
    )

if __name__ == "__main__":
    main()
