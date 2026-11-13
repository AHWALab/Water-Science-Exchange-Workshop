"""
Make the participant (workshop) and the clean solution versions of a notebook.

Usage
    python tools/make_workshop_version.py SOURCE.ipynb OUTPUT.ipynb --mode workshop
    python tools/make_workshop_version.py SOURCE.ipynb OUTPUT.ipynb --mode solution

The source notebook marks the lines that participants must write themselves:

    #################### Your Code Goes Here #########################
    # Step 1. What to do here
    # >>> SOLUTION
    answer = ...
    # <<< SOLUTION
    ###################################################################

Mode workshop  removes the lines between the markers and leaves one blank line,
               removes the marker lines, and clears all outputs.
Mode solution  removes the marker lines only, outputs are kept.
"""
import argparse
import nbformat

START, END = "# >>> SOLUTION", "# <<< SOLUTION"


def transform(source, mode):
    out, hidden = [], False
    for line in source.splitlines():
        s = line.strip()
        if s == START:
            hidden = True
            if mode == "workshop":
                out.append("")
            continue
        if s == END:
            hidden = False
            continue
        if hidden and mode == "workshop":
            continue
        out.append(line)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--mode", choices=["workshop", "solution"], default="workshop")
    a = ap.parse_args()
    nb = nbformat.read(a.src, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.source = transform(cell.source, a.mode)
            if a.mode == "workshop":
                cell.outputs = []
                cell.execution_count = None
    nbformat.write(nb, a.dst)
    print("wrote", a.dst)


if __name__ == "__main__":
    main()
