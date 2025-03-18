from pylatex_sssi111.latex_generator import generate_table_latex, generate_latex_headers

if __name__ == "__main__":
    data = [
        ["Brand", "Model", "Country"],
        ["Toyota", "Camry", "Japan"],
        ["Ford", "F-150", "USA"],
        ["Volkswagen", "Golf", "Germany"],
        ["Hyundai", "Tucson", "South Korea"],
        ["BMW", "3 Series", "Germany"],
        ["Tesla", "Model S", "USA"],
        ["Honda", "Civic", "Japan"],
        ["Lada", "Vesta", "Russia"],
        ["Geely", "Emgrand", "China"],
    ]

    latex_table_data = generate_table_latex(data)
    generate_latex_headers("example_table.tex", latex_table_data)
