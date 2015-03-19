import fsutils as fs
import os
from os import path
from PyPDF2 import PdfFileReader, PdfFileMerger
from subprocess import call
from django.template import Template, Context
from django.conf import settings
settings.configure()

def make_letters(names_path, template_path, dest_path):
    names = load_names(names_path)
    text = load_template(template_path)

    print(text)

    ensure_dest(dest_path)

    template = Template(text)

    for i, name in enumerate(sorted(names.keys())):
        data = {
            'name': name,
            'address': names[name],
        }

        rendered = template.render(Context(data))

        # Write the tex source
        filename = '%d-%s.tex' % (i, ' '.join(name.split()[-1:]))
        file_path = path.join(dest_path, filename)
        write_file(rendered, file_path,)

        # Create the PDF
        pdf_name = '%d-%s.pdf' % (i, ' '.join(name.split()[-1:]))
        call(['xelatex', file_path])

        # Clean temps
        fs.rm_f(filename[:-3] + 'aux')
        fs.rm_f(filename[:-3] + 'log')

        # Move pdf to output folder
        pdf_path = path.join(dest_path, pdf_name)
        os.rename(pdf_name, pdf_path)

    join_pdfs(dest_path, path.join(dest_path, 'output.pdf'))
    #call(['open', path.join(dest_path, 'output.pdf')])

def join_pdfs(src_path, dest_path):
    """
    Thanks to http://www.boxcontrol.net/merge-pdf-files-with-under-10-lines-in-python.html#.VQiOL2TF-PI
    """
    pdf_files = [f for f in os.listdir(src_path) if f.endswith("pdf")]
    merger = PdfFileMerger()

    for filename in pdf_files:
        merger.append(PdfFileReader(os.path.join(src_path, filename), "rb"))

    merger.write(dest_path)

def format_date(d):
    month = d.strftime('%B')
    day = str(d.day)
    year = d.year

    date_string = '%s %s, %s' % (month, day, year)

    return date_string

def load_names(names_path, delim=':'):
    with open(names_path, 'r') as f:
        lines = f.readlines()

    fields = [l.split(delim) for l in lines]
    names = {}
    for f in fields:
        f = [s.strip() for s in f]
        name = f[0]
        address = ' \\\\ '.join(f[1:])
        names[name] = address

    return names

def load_template(template_path):
    with open(template_path, 'r') as f:
        text = f.read()

    return text

def ensure_dest(dest_path):
    fs.rm_rf(dest_path)
    fs.mkdir_p(dest_path)

def write_file(data, filename):
    with open(filename, 'w') as f:
        f.write(data)

if __name__ == "__main__":
    make_letters("names.txt", "template.tex", "output")
