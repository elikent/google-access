from pathlib import Path
from PyPDF2 import PdfMerger

def combine_pdfs(input_dir: Path, output_file: Path):
    '''Combines all PDFs into one PDF.'''
    merger = PdfMerger()

    # Collect matching PDFs
    pdfs = sorted(input_dir.glob('*-single.pdf'))
    if not pdfs:
        print("No matching PDFs found.")
        return
    
    print(f"Found {len(pdfs)} PDFs:")

    for pdf in pdfs:
        print(f'Adding: {pdf.name}')
        merger.append(str(pdf))

    output_file.parent.mkdir(parents=True, exist_ok=True)
    merger.write(str(output_file))
    merger.close()
    print(f'Combined {len(pdfs)} PDFs into {output_file}')

