
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from . import format

PDF_HP_PATH_FMT = '{path}/{name}_halfpage.pdf'
PDF_BOOKLET_PATH_FMT = '{path}/{name}_booklet.pdf'

HP_WIDTH = letter[1] / 2
HP_HEIGHT = letter[0]
LS_WIDTH = letter[1]
LS_HEIGHT = letter[0]


def get_booklet_page_pairs(num_pages):
    """
    Get the page ordering for booklet format.
    """
    if num_pages <= 2:
        return [(0, None)] if num_pages == 1 else [(0, 1)]

    pairs = []
    left = 0
    right = num_pages - 1

    while left <= right:
        if left == right:
            pairs.append((left, None))
        else:
            pairs.append((right, left))
            pairs.append((left + 1, right - 1))
        left += 2
        right -= 2

    return pairs


def get_standard_page_pairs(num_pages):
    """
    Get the page ordering for standard 2-up format.
    """
    pairs = []
    for i in range(0, num_pages, 2):
        if i + 1 < num_pages:
            pairs.append((i, i + 1))
        else:
            pairs.append((i, None))
    return pairs


def imposer(pdf_path, config):
    """
    Imposes the base PDF according to the specified config (half-page or booklet).
    """
    results = []
    if config.get('halfpage') == True:
        format.print_subheader("Creating half-page imposed PDF")
        results.append(impose(pdf_path, booklet=False))
    if config.get('booklet') == True:
        format.print_subheader("Creating booklet imposed PDF")
        results.append(impose(pdf_path, booklet=True))
    return results


def impose(pdf_path, booklet=False):
    """
    Creates half-page and booklet imposed versions of the base pdf.
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    path = Path(pdf_path).parent
    name = Path(pdf_path).stem
    if booklet:
        dest = PDF_BOOKLET_PATH_FMT.format(
            path=path, name=name)
    else:
        dest = PDF_HP_PATH_FMT.format(path=path, name=name)

    num_pages = len(reader.pages)
    if num_pages < 2:
        print("  ! Insufficient pages to impose, skipping")
        return

    src_width = reader.pages[0].mediabox.width
    src_height = reader.pages[0].mediabox.height
    scale = min(HP_WIDTH / src_width, HP_HEIGHT / src_height)
    scaled_width = src_width * scale
    scaled_height = src_height * scale

    if booklet:
        page_order = get_booklet_page_pairs(num_pages)
    else:
        page_order = get_standard_page_pairs(num_pages)

    for pair in page_order:
        dest_page = writer.add_blank_page(LS_WIDTH, LS_HEIGHT)

        for slot, index in enumerate(pair):
            if index is None:
                continue

            src_page = reader.pages[index]
            x_offset = slot * HP_WIDTH + (HP_WIDTH - scaled_width) / 2
            y_offset = (HP_HEIGHT - scaled_height) / 2

            transform = (scale, 0, 0, scale, x_offset, y_offset)
            dest_page.merge_transformed_page(src_page, transform)

    with open(dest, 'wb') as f:
        writer.write(f)

    format.print_item_success(
        "Generated imposed PDF", indent=1)
    return dest
