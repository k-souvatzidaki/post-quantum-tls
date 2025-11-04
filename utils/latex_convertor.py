import pandas as pd

def split_tables(df):
    tables = []
    current_table = []

    for _, row in df.iterrows():
        # Check if row is entirely NaN => separator row (;;;;;;;)
        if row.isna().all():
            if current_table:
                tables.append(pd.DataFrame(current_table))
                current_table = []
        else:
            current_table.append(row)

    # Append final table if exists
    if current_table:
        tables.append(pd.DataFrame(current_table))

    return tables

def df_to_latex(df):
    return df.to_latex(index=False, na_rep="", escape=False)


if __name__ == "__main__":
    file = "results/RESULTS_all.csv" 
    # Read CSV, semicolon delimiter, no header
    df = pd.read_csv(file, sep=";", header=None)

    tables = split_tables(df)

    latex_doc = []
    latex_doc.append(r"\documentclass{article}")
    latex_doc.append(r"\usepackage{booktabs}")
    latex_doc.append(r"\usepackage{geometry}")
    latex_doc.append(r"\geometry{margin=1in}")
    latex_doc.append(r"\begin{document}")
    latex_doc.append("")

    for i, t in enumerate(tables, 1):
        t.columns = t.iloc[0]
        t = t[1:]

        table_code = df_to_latex(t)

        latex_doc.append(r"\begin{table}[h!]")
        latex_doc.append(r"\centering")
        latex_doc.append(table_code)
        latex_doc.append(rf"\caption{{Table {i}}}")
        latex_doc.append(rf"\label{{tab:table{i}}}")
        latex_doc.append(r"\end{table}")
        latex_doc.append("")

    latex_doc.append(r"\end{document}")

    with open("document.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(latex_doc))

    print("LaTeX file generated: document.tex")