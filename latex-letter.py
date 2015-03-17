import fsutils as fs
from os import path
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

    for i, name in enumerate(names.keys()):
        data = {
            'name': name,
            'address': names[name],
        }

        rendered = template.render(Context(data))

        filename = '%d-%s.tex' % (i, ' '.join(name.split()[-1:]))
        file_path = path.join(dest_path, filename)
        write_file(rendered, file_path,)

        pdf_name = '%d-%s.pdf' % (i, ' '.join(name.split()[-1:]))
        pdf_path = path.join(dest_path, pdf_name)
        call(['xelatex', file_path, '-output-directory='+ dest_path])
    call(['convert', '*.pdf', 'output.pdf'])
    call(['open', 'output.pdf'])

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


names_path = "names.txt"
template_path = "template2.tex"
dest_path = "output"

make_letters(names_path, template_path, dest_path)
