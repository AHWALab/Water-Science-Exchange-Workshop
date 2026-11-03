"""
Make the participant (workshop) version of a solution notebook.

Usage
    python tools/make_workshop_version.py notebooks/01_x_solution.ipynb notebooks/01_x.ipynb

Rules
    * Code between the lines  "# >>> SOLUTION"  and  "# <<< SOLUTION"  is replaced
      by a single line  "# YOUR CODE HERE"  (same indentation as the marker).
    * All outputs and execution counts are removed.
    * Everything else (markdown, comments, scaffolding) is kept as is.
"""
import sys
import nbformat

START, END, FILL = "# >>> SOLUTION", "# <<< SOLUTION", "# YOUR CODE HERE"


def strip_solution(source):
    out, hidden = [], False
    for line in source.splitlines():
        s = line.strip()
        if s == START:
            hidden = True
            out.append(line.replace(START, FILL))
            continue
        if s == END:
            hidden = False
            continue
        if not hidden:
            out.append(line)
    return "\n".join(out)


def main(src, dst):
    nb = nbformat.read(src, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.source = strip_solution(cell.source)
            cell.outputs = []
            cell.execution_count = None
    nbformat.write(nb, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
