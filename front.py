import streamlit as st
from PIL import Image
import PyPDF2
import fitz


def main():
    """
    Main function of the Streamlit app that configures the page and calls
    the function to display the PDF.
    """
    st.set_page_config(
        page_title="PDF Extract",
        page_icon="📑",
        layout="wide",
        menu_items=None
        )
    st.title("PDF Extract")
    pdf_file = st.file_uploader("Instruct", type=["pdf"])

    if pdf_file is not None:
        show_pdf(pdf_file)


def img_from_page(doc: fitz.Document, n_page: int) -> Image:
    page = doc.load_page(n_page-1)
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width,  pix.height], pix.samples)
    return image


def show_pdf(pdf_file):
    pdf_show = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    nbr_pages = len(pdf_reader.pages)
    page_num = st.selectbox("Sélectionner une page", range(1, nbr_pages+1))
    pdf_page = pdf_reader.pages[page_num-1]

    docs, overview, pdf = st.columns([3, 3, 2])

    # column 1
    docs.markdown('##### Text to clean : ')
    text = docs.text_area(
        label="Text to clean",
        value=pdf_page.extract_text(),
        height=600,
        label_visibility='collapsed'
        )

    # column 2
    overview.markdown('##### Aperçu : ')
    with overview.container(height=600):
        st.markdown(text)

    # column 3
    pdf.image(img_from_page(pdf_show, page_num))

    if st.button('Upload  clean_text'):
        st.toast('Pdf upload !')
    with open("instruction.md", "r", encoding="utf-8") as file:
        markdown_content = file.read()
    st.markdown(markdown_content)


if __name__ == "__main__":
    main()
