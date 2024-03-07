import streamlit as st
import fitz
from PIL import Image


def main():
    st.set_page_config(
        page_title="PDF Extract",
        page_icon="📑",
        layout="wide",
        menu_items=None
        )
    st.title("PDF Extract")
    infos, pdf = st.columns([1, 2])
    pdf_file = infos.file_uploader("Instruct", type=["pdf"])
    selected_pages = {}
    if pdf_file is not None:
        show_pdf(pdf_file, infos, pdf, selected_pages)


def image_from_page(doc: fitz.Document, n_page: int, bw: bool = True) -> Image:
    index_page = n_page-1
    page = doc.load_page(index_page)
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width,  pix.height], pix.samples)
    if not bw:
        image = image.convert("L")
    return image


def show_pdf(pdf_file, col1, col2, selected_pages):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    with col2.container(height=700, border=False):
        for page_nbr in range(1, 1+pdf_document.page_count):
            selected = col1.checkbox(f'Page : {page_nbr}', value=True)
            if selected:
                selected_pages[page_nbr] = True
            else:
                selected_pages.pop(page_nbr, None)
            st.title(f'Page {page_nbr} :')
            st.image(
                image_from_page(pdf_document, page_nbr, selected),
                use_column_width="always"
                )

    if col1.button('Upload'):
        st.toast('Pdf upload !')
        print(selected_pages.keys())


if __name__ == "__main__":
    main()
