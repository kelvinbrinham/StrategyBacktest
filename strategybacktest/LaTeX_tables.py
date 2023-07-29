"""Create LaTeX tables from summary excel files."""

import os

from functions import excel_summary_2_latex


def main() -> None:
    """Run main function."""
    output_dir = "output"
    file_list = os.listdir(output_dir)
    excel_files = [
        os.path.join(output_dir, file_)
        for file_ in file_list
        if file_.endswith(".xlsx")
    ]
    excel_summary_2_latex(filepath=excel_files)


if __name__ == "__main__":
    main()
