import itertools
import numpy as np


class LatexConvergenceTable(object):
    """Format convergence data as LaTeX `tabular`."""

    def __init__(self, all_errors, all_rates, resolutions, all_labels):
        """Create a convergence table from the provided data.

        Both `all_errors` and `all_rates` are lists of the columns, e.g.

            all_errors = [np.array([2e-2, 5.0e-3, 1.25e-3]), np.array([2.0e-2, 1.0e-2, 5.0e-3])]
            all_rates  = [np.array([2.0, 2.0]), np.array([1.0, 1.0])]

        """
        self.table = "".join(
            [
                self.header(all_labels),
                self.content(all_errors, all_rates, resolutions),
                self.footer(),
            ]
        )

    def write(self, filename):
        with open(filename, "w+") as f:
            f.write(self.table)

    def header(self, all_labels):
        n = len(all_labels)

        header = "".join(
            [
                "\\begin{{tabular}}{{r\n",
                n * "                S[table-format=3.2e2]r\n",
                "}}\n",
                "\\toprule\n",
                "N & ",
                " & ".join(n * ["\n\\multicolumn{{2}}{{c}}{{{:s}}}"]),
                " \\\\\n",
                "{:s} & ".format(self.header_field_a()),
                " & ".join(
                    n
                    * (
                        [
                            "\n"
                            + " & ".join(
                                [
                                    "\\multicolumn{{1}}{{c}}{{" + label + "}}"
                                    for label in self.header_column_labels()
                                ]
                            )
                        ]
                    )
                ),
                " \\\\\n",
                "\\midrule\n",
            ]
        )
        header = header.format(*all_labels)

        return header

    def header_column_labels(self):
        return "err", "rate"

    def header_field_a(self):
        return ""

    def footer(self):
        return "".join(["\\bottomrule\n", "\\end{tabular}"])

    def content(self, all_errors, all_rates, resolutions):
        content = self.first_line(resolutions[0], self.extract_line(all_errors, 0))
        for k in range(1, np.size(resolutions)):
            content += self.line(
                resolutions[k],
                self.extract_line(all_errors, k),
                self.extract_line(all_rates, k - 1),
            )

        return content

    def first_line(self, N, errors):
        data = [N] + errors

        n = len(errors)
        line_pattern = (
            self.resolution_format() + n * "& {: 8.2e}  &      --  " + " \\\\\n"
        )
        return line_pattern.format(*data)

    def line(self, N, errors, rates):
        data = [N] + list(itertools.chain.from_iterable(zip(errors, rates)))

        n = len(errors)
        line_pattern = (
            self.resolution_format() + n * "& {: 8.2e}  & {: 8.2f} " + " \\\\\n"
        )
        return line_pattern.format(*data)

    def resolution_format(self):
        return "{:3d} "

    def extract_line(self, data, k):
        return [x[k] for x in data]
