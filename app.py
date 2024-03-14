import streamlit as st
from PIL import Image
import fitz
from pymongo import MongoClient
import datetime


def main():
    st.set_page_config(
        page_title="PDF Extract",
        page_icon="📑",
        layout="wide",
        menu_items=None
        )
    st.title("PDF Extract")
    extract, pdf = st.columns([4, 3])
    pdf_file = extract.file_uploader("Instruct", type=["pdf"])
    if pdf_file is not None:
        pdf_reader(pdf_file, extract, pdf)
    with open("instruction.md", "r", encoding="utf-8") as file:
        markdown_content = file.read()
    st.markdown(markdown_content)


def pdf_reader(pdf_file: st.file_uploader, col1, col2):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

    page_num = col1.selectbox("Sélectionner une page", range(1, len(doc)+1))

    pdf_page = doc[page_num-1]
    img = img_from_page(doc, page_num)
    txt = pdf_page.get_text()

    col1.markdown('##### Text to clean : ')
    col1.text_area(
        label="Text to clean",
        value=txt,
        height=535,
        label_visibility='collapsed'
        )
    col2.markdown("##### Aperçu du pdf : ")
    with col2.container(height=800):
        st.image(img, use_column_width=True)

    if st.button('Upload  clean_text'):
        # upload_to_mongodb(pdf_file.name, page_num)
        st.toast('Pdf upload !')


def img_from_page(doc, n_page: int) -> Image:
    page = doc.load_page(n_page-1)
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width,  pix.height], pix.samples)
    return image


def upload_to_mongodb(
    name_pdf: str,
    n_page: int,
    brut: str,
    clean: str,
    comment: str
):
    client = MongoClient('mongodb://localhost:27017/')
    collection = client.RagVignerons.page_pdf
    document = {
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
        'name_pdf': name_pdf,
        'page_number': n_page,
        'text_brut': brut,
        'text_clean': clean,
        'comment': comment
    }
    collection.insert_one(document)
    client.close()


if __name__ == "__main__":
    main()
