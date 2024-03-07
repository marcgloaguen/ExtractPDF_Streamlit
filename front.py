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
    infos, pdf = st.columns(2)
    pdf_file = infos.file_uploader("Instruct", type=["pdf"])

    if pdf_file is not None:
        show_pdf(pdf_file, infos, pdf)


def img_from_page(doc: fitz.Document, n_page: int) -> Image:
    page = doc.load_page(n_page-1)
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width,  pix.height], pix.samples)
    return image


def show_pdf(pdf_file, col1, col2):
    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    nbr_pages = len(pdf_reader.pages)
    page_num = col2.selectbox("Sélectionner une page", range(1, nbr_pages+1))
    pdf_page = pdf_reader.pages[page_num-1]

    container1 = col1.container(height=600)
    container1.image(img_from_page(pdf, page_num))

    col2.text_area("Text to clean", pdf_page.extract_text(), 600)
    if col2.button('Upload  clean_text'):
        st.toast('Pdf upload !')

    st.markdown(
        """
        ---
        ##### Instruction
        Utilisez le caractère dièse (#) suivi d'un espace pour définir des titres. Par exemple :
        ```
        # Titre principal
        ## Sous-titre
        ### Sous-sous-titre
        ```
        Utilisez trois tirets (-) ou astérisques (*) sur une ligne pour créer un séparateur horizontal :
        ```
        ---
        ```

        ou

        ```
        ***
        ```
    """
    )


if __name__ == "__main__":
    main()
