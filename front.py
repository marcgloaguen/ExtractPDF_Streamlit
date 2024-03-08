import streamlit as st
from PIL import Image
import PyPDF2
import fitz
from pymongo import MongoClient
import datetime
import io


def main():
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
    with open("instruction.md", "r", encoding="utf-8") as file:
        markdown_content = file.read()
    st.markdown(markdown_content)


def img_from_page(doc: fitz.Document, n_page: int) -> Image:
    page = doc.load_page(n_page-1)
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width,  pix.height], pix.samples)
    return image


def upload_to_mongodb(img, brut, clean, comment):
    img_data = io.BytesIO()
    img.save(img_data, format='JPEG')
    img_data = img_data.getvalue()
    client = MongoClient('mongodb://localhost:27017/')
    collection = client.RagVignerons.page_pdf
    document = {
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
        'pdf_image': img_data,
        'text_brut': brut,
        'text_clean': clean,
        'comment': comment
    }
    collection.insert_one(document)
    client.close()


def show_pdf(pdf_file: st.file_uploader):
    pdf_show = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    nbr_pages = len(pdf_reader.pages)
    page_num = st.selectbox("Sélectionner une page", range(1, nbr_pages+1))
    pdf_page = pdf_reader.pages[page_num-1]

    docs, overview, pdf = st.columns([4, 4, 2])

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
    pdf.markdown("##### Aperçu du pdf : ")
    img = img_from_page(pdf_show, page_num)
    pdf.image(img)
    comment = pdf.text_input("Commentaires:")
    if pdf.button('Upload  clean_text'):
        upload_to_mongodb(img, pdf_page.extract_text(), text, comment)
        st.toast('Pdf upload !')


if __name__ == "__main__":
    main()
