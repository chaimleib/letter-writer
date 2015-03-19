# letter-writer

## latex_letter.py
This script was originally created to prepare lots of thank you notes for printing.

It inserts the addressee info, renders to pdf, then joins all the letters into a single large pdf for easy printing.

This requires TeXlive, pypdf2, django and python3.

## email_letter.py
This script sends an email with attachments to everyone in a list file. Every line in the list file represents a separate email, and uses colons to separate between the To, CC, and BCC fields. If there are multiple addresses in these fields, they are separated with commas.

 This script requires django and python3.

