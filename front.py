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
    col1, col2 = st.columns([1, 2])

    pdf_file = col1.file_uploader("Instruct", type=["pdf"])
    print("reset")

    if pdf_file is not None:
        with col2:
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
            with st.container(height=700, border=False):
                for page_nbr in range(pdf_document.page_count):
                    col1.checkbox(f'Page : {page_nbr+1}', value=True)
                    st.title(f'Page {page_nbr+1}')
                    st.image(
                        image_from_page(pdf_document, page_nbr),
                        use_column_width="always"
                        )

        if col1.button('Upload'):
            st.toast('Pdf upload !')


def image_from_page(doc: fitz.Document, n_page: int, bw: bool = True) -> Image:
    page = doc.load_page(n_page)
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width,  pix.height], pix.samples)
    if not bw:
        image = image.convert("L")
    return image


if __name__ == "__main__":
    main()
