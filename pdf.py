from pdfrw import PdfReader, PdfWriter, PageMerge


def pdf_file(input_file, output_file):
    reader_input = PdfReader(input_file)
    writer_output = PdfWriter()

    for current_page in range(len(reader_input.pages)):
        merger = PageMerge(reader_input.pages[current_page])
    writer_output.write(output_file, reader_input)