import re

from PyPDF2 import PdfFileReader
from spacy.lang.en import English


KEYWORD = 'JobKeeper'
nlp = English()
nlp.add_pipe('sentencizer')

with open(r'C:\Users\matth\Documents\git\projectTBD\src\tmp\metadata.pdf', 'rb') as f:
    pdf = PdfFileReader(f)

    # Decrypt the unencrypted
    if pdf.isEncrypted:
        if pdf.decrypt('') == 0:
            raise Exception

    pattern = re.compile(KEYWORD)
    for page_num in range(pdf.getNumPages()):
        page = pdf.getPage(page_num)
        text = page.extractText()

        if pattern.search(text):
            print(f"{KEYWORD} found on page {page_num}")

            for sentence in nlp(text).sents:
                if pattern.search(sentence.text):
                    text_ = sentence.text.replace('\n', '')
                    print(f"{text_}")

print(1)