import streamlit as st
import awesome_streamlit as ast

from typing import List


def write():

    with open("README.md", 'r') as file:
        md_content = file.read()

    st.markdown(md_content)


def get_apps() -> List[ast.shared.models.Resource]:
    return [
        resource
        for resource in ast.database.RESOURCES
        if ast.database.tags.APP_IN_GALLERY in resource.tags
    ]


if __name__ == "__main__":
    write()
