import subprocess
import os
import glob

from pylatex_sssi111 import generate_table_latex, generate_image_latex, generate_latex_headers

IMAGE_PATH = 'python_meme.jpg'

TABLE_DATA = [
    ["Brand", "Model", "Country"],
    ["Toyota", "Camry", "Japan"],
    ["Ford", "F-150", "USA"],
    ["Volkswagen", "Golf", "Germany"],
    ["Hyundai", "Tucson", "South Korea"],
    ["BMW", "3 Series", "Germany"],
    ["Tesla", "Model S", "USA"],
    ["Honda", "Civic", "Japan"],
    ["Lada", "Vesta", "Russia"],
    ["Geely", "Emgrand", "China"]
]

def compile_and_clean():
    try:
        subprocess.run(
            ["pdflatex", "temp.tex"],
        )
        print("PDF was generated as: temp.pdf")
        
        temp_files = glob.glob('temp.*')
        for file in temp_files:
            if not file.endswith('.pdf'):
                os.remove(file)
                print(f"remove: {file}")
                
    except subprocess.CalledProcessError as e:
        print(f"LaTeX compile error: {e}")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    image = generate_image_latex(IMAGE_PATH)
    table = generate_table_latex(TABLE_DATA)
    generate_latex_headers("temp.tex", [image, table])

    compile_and_clean()
