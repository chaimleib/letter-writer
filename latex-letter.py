from datetime import datetime
import fsutils as fs
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
            #'date': format_date(datetime.now()),
            'i': i,
            'name': name,
            'address': names[name],
            'filename': '%d-%s.tex' % (i, ' '.join(name.split()[-1:])),
        }
        rendered = template.render(Context(data))
        print(rendered)
        return

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


names_path = "names.txt"
template_path = "template.tex"
dest_path = "output"

make_letters(names_path, template_path, dest_path)
