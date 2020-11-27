import base64
import streamlit as st
import awesome_streamlit as ast

from typing import List


def write():

    with open("SOSim - Documentation.pdf",
              'rb') as pdf_file: 
        base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">' 
    st.markdown(pdf_display, unsafe_allow_html=True)


def get_apps() -> List[ast.shared.models.Resource]:
    return [
        resource
        for resource in ast.database.RESOURCES
        if ast.database.tags.APP_IN_GALLERY in resource.tags
    ]


if __name__ == "__main__":
    write()
