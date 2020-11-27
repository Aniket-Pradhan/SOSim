import streamlit as st
import awesome_streamlit as ast

import src.pages.home
import src.pages.calc_time
import src.pages.calc_thickness
import src.pages.documentation


def main():
    PAGES = {
        "Home": src.pages.home,
        "Calculate Time Required": src.pages.calc_time,
        "Calculate Oxide Thickness": src.pages.calc_thickness,
        "Documentation": src.pages.documentation
    }

    st.sidebar.title("SOSim")
    selection = st.sidebar.radio("What would you like to do?",
                                 list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)

    st.sidebar.title("Group 5")
    st.sidebar.info(
        "- Aniket Pradhan  \n"
        "- Arav Malik  \n"
        "- M Aamir  \n"
        "- Mansi  \n"
        "- Rahul  \n"
    )


if __name__ == "__main__":
    main()
