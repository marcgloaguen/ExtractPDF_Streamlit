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

    if pdf_file is not None:
        if col1.button('Upload'): 
            st.toast('Pdf upload !')

        with col2:
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
            with st.container(height=1000):
                for page_nbr in range(pdf_document.page_count):

                    st.checkbox(f'Page {page_nbr+1}', value=True)
                    st.image(
                        image_from_page(pdf_document, page_nbr),
                        use_column_width="always"
                        )


def image_from_page(doc: fitz.Document, page_nbr: int) -> Image:
    page = doc.load_page(page_nbr)
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width,  pix.height], pix.samples)
    return image


if __name__ == "__main__":
    main()
