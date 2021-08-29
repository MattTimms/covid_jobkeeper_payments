import os
import re
from typing import List, Union

import fitz
from spacy.lang.en import English

nlp = English()
nlp.add_pipe('sentencizer')


def find_keyword(keywords: Union[str, List[str]], file_path: str, save_crop_imgs: bool = False):
    # Prepare regex pattern from keywords
    if isinstance(keywords, str):
        keywords = [keywords]
    pattern = re.compile(f'(?:{"|".join(keywords)})', flags=re.IGNORECASE)

    # Prepare output document
    directory, basename = os.path.split(file_path)
    filename, ext = os.path.splitext(basename)
    output_file_path = os.path.join(directory, f'{filename} - ({"-".join(keywords)}).{ext}')
    output_img_dir = os.path.join(directory, filename)
    os.makedirs(output_img_dir, exist_ok=True)

    found_keyword = False
    mat = fitz.Matrix(2, 2)  # image zoom factor
    doc = fitz.open(file_path)
    for page in doc:
        text = page.get_text()
        if pattern.search(text):  # quick-check all text
            found_keyword = True
            print(f"Keywords found on page {page.number}")

            # Iterate over paragraphs
            for (x0, y0, x1, y1, paragraph, block_no, block_type) in page.get_text("blocks"):
                for sentence in nlp(paragraph).sents:
                    if pattern.search(sentence.text):

                        text_ = sentence.text.replace('\n', '')
                        print(f"\t{text_}")

                        text_instances = page.search_for(sentence.text.lstrip().rstrip())
                        for inst in text_instances:
                            highlight = page.add_highlight_annot(inst)
                            highlight.update()

                        if save_crop_imgs:
                            rect = fitz.Rect(x0, y0, x1, y1)
                            img = page.get_pixmap(clip=rect, matrix=mat)
                            img_path = os.path.join(output_img_dir, f'p{page.number}para{block_no}.jpg')
                            img.pil_save(img_path, optimize=False, dpi=(1500, 1500))

    if found_keyword:
        doc.save(output_file_path, garbage=4, deflate=True, clean=True)
