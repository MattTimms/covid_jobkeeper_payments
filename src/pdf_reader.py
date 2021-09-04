import os
import re
from typing import List, Union

import fitz
from spacy.lang.en import English
from tqdm import tqdm

nlp = English()
nlp.add_pipe('sentencizer')


def find_keyword(keywords: Union[str, List[str]],
                 file_path: str,
                 save_crop_imgs: bool = False,
                 verbose: bool = False) -> int:
    # Prepare regex pattern from keywords
    if isinstance(keywords, str):
        keywords = [keywords]
    pattern = re.compile(f'(?:{"|".join(keywords)})', flags=re.IGNORECASE)

    # Prepare output document
    directory, basename = os.path.split(file_path)
    filename, ext = os.path.splitext(basename)
    output_file_path = os.path.join(directory, f'{filename} - ({"-".join(keywords)}){ext}')
    output_img_dir = os.path.join(directory, filename)
    if save_crop_imgs:
        os.makedirs(output_img_dir, exist_ok=True)

    keyword_found_cnt = 0
    mat = fitz.Matrix(2, 2)  # image zoom factor
    doc = fitz.open(file_path)
    for page in tqdm(doc, desc=f"Searching for keywords {filename}", leave=False, disable=verbose):
        text = page.get_text()
        if pattern.search(text):  # quick-check all text
            keyword_found_cnt += 1
            # print(f"Keywords found on page {page.number}")

            # Iterate over paragraphs
            for (x0, y0, x1, y1, paragraph, block_no, block_type) in page.get_text("blocks"):
                for sentence in nlp(paragraph).sents:
                    if pattern.search(sentence.text):

                        text_ = sentence.text.replace('\n', '')
                        if verbose:
                            print(f"\t{text_}")

                        text_instances = page.search_for(sentence.text.lstrip().rstrip())
                        for inst in text_instances:
                            highlight = page.add_highlight_annot(inst)
                            highlight.update()

                        if save_crop_imgs:
                            rect = fitz.Rect(x0, y0, x1, y1)
                            try:
                                img = page.get_pixmap(clip=rect, matrix=mat)
                                img_path = os.path.join(output_img_dir, f'p{page.number}para{block_no}.jpg')
                                img.pil_save(img_path, optimize=False, dpi=(1500, 1500))
                            except Exception:
                                continue

    if keyword_found_cnt:
        with tqdm(desc='Saving highlighted pdf', leave=False):
            doc.save(output_file_path, garbage=4, deflate=True, clean=True)
    return keyword_found_cnt
