import fsutils as fs
import re
from os import path

from pprint import pprint

import settings as my_settings
from django.conf import settings
from django.template import Template, Context
from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives

settings.configure(**my_settings.__dict__)

def make_emails(addresses_path, subject, template_path, attachments=[], context={}):
    datadicts = load_addresses(addresses_path)
    template = Template(fs.read_file(template_path))

    text = template.render(Context(context))

    for dd in datadicts:
        dd['attachments'] = attachments
        dd['subject'] = subject
        dd['body'] = text_from_html(text)
        dd['html'] = text

    send_mass_mail(datadicts)


html_tags = re.compile('<[^>]*>')
multispace = re.compile('  +')
def text_from_html(html):
    result = html.replace('\n', '').replace('\r', '')
    result = result.replace('<br>', '\n').replace('</p>', '\n\n')
    result = html_tags.sub('', result)
    result = multispace.sub(' ', result)
    result = result.replace('&nbsp;', ' ')
    result = result.replace('&gt;', '>').replace('&lt;', '<')
    result = result.replace('&amp;', '&')

    lines = result.split('\n')
    while len(lines[-1].strip()) == 0:
        lines.pop()

    return '\n'.join(lines)


def send_mass_mail(datadicts, fail_silently=False, auth_user=None,
                   auth_password=None, connection=None):
    """
    Given a datatuple of (subject, message, from_email, recipient_list), sends
    each message to each recipient list. Returns the number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    Note: The API for this method is frozen. New code wanting to extend the
    functionality should use the EmailMessage class directly.
    """
    connection = connection or get_connection(username=auth_user,
                                    password=auth_password,
                                    fail_silently=fail_silently)
    messages = []

    for dd in datadicts:
        message = EmailMultiAlternatives(
            dd['subject'],
            dd['body'],
            dd.get('sender'),
            dd['to'],
            cc=dd['cc'],
            bcc=dd['bcc'],
            connection=connection,
        )
        message.attach_alternative(dd['html'], "text/html")

        for file_path in dd['attachments']:
            message.attach_file(file_path)

        messages.append(message)

    return connection.send_messages(messages)


def load_addresses(addresses_path, delim=':'):
    lines = fs.read_file_lines(addresses_path)

    fields = [l.split(delim) for l in lines if len(l.strip())]
    addresses = []
    for f in fields:
        f = [s.strip() for s in f]

        to = [addr.strip() for addr in f[0].split(',')]
        cc = [addr.strip() for addr in f[1].split(',')] if len(f) > 1 else None
        bcc = [addr.strip() for addr in f[2].split(',')] if len(f) > 2 else None
        data = {
            'to': to,
            'cc': cc,
            'bcc': bcc,
        }
        addresses.append(data)

    return addresses


if __name__ == '__main__':
    print(settings.EMAIL_HOST_USER)

    make_emails(
        "email-addresses.txt",
        "Passover Sale of Leavening (Chometz)",
        "email-template.html",
        attachments=['/Users/chaimleib/Desktop/Vaad Pesach/5775 Pesach forms/5775-Pesach cover letter.pdf']
    )
