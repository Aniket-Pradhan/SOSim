import streamlit as st
import awesome_streamlit as ast

import numpy as np
import plotly.express as px

from typing import List


def get_time_deal_growe(ambient: str,
                        partial_pressure: float,
                        crystal_orientation: str,
                        initial_oxide_thickness: float,
                        temperature: float,
                        final_oxide_thickness: float) -> float:
    return 0


def get_time_massoud(partial_pressure: float,
                     crystal_orientation: str,
                     initial_oxide_thickness: float,
                     temperature: float,
                     final_oxide_thickness: float) -> float:
    return 0


def write():
    themes = ['ggplot2', 'seaborn', 'simple_white', 'plotly',
              'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
              'ygridoff', 'gridon', 'none']

    st.sidebar.title("Calculate time required")

    algorithm = st.sidebar.radio("Algorithm", ["Deal-Growe", "Massoud"])

    if algorithm == "Deal-Growe":
        ambient = st.sidebar.radio("Ambient", ["Dry", "Wet"])
    if algorithm == "Massoud":
        ambient = st.sidebar.radio("Ambient", ["Dry"])

    if ambient == "Wet":
        partial_pressure = float(st.sidebar.text_input(
            'Partial Pressure (atm)', 0.92))
    else:
        partial_pressure = 1

    crystal_orientation = st.sidebar.selectbox('Crystal Orientation',
                                               ["<100>", "<111>", "<110>"])

    initial_oxide_thickness = float(
        st.sidebar.text_input('Initial Oxide Thickness (Å)', 10))

    temperature = st.sidebar.slider(
        "Temperature (°C)", min_value=700, max_value=1200, value=1000)

    final_oxide_thickness = float(
        st.sidebar.text_input('Final Oxide Thickness (Å)', 20))

    # Calculate time
    if algorithm == "Deal-Growe":
        time = get_time_deal_growe(ambient,
                                   partial_pressure,
                                   crystal_orientation,
                                   initial_oxide_thickness,
                                   temperature,
                                   final_oxide_thickness)
    else:
        time = get_time_massoud(partial_pressure,
                                crystal_orientation,
                                initial_oxide_thickness,
                                temperature,
                                final_oxide_thickness)

    st.sidebar.title("Theme")
    theme_selection = st.sidebar.selectbox("Theme", themes)

    # Header for main page/Show output
    st.header("{} minutes of heating is required".format(time))
    st.write("For oxidising {}Å of silicon at {}°C".format(
        final_oxide_thickness, temperature))

    # Plot
    time = np.arange(0, 10, 0.1)
    data = np.sin(time)
    fig = px.line(x=time,
                  y=data,
                  template=theme_selection)
    fig.update_layout(xaxis_title="time",
                      yaxis_title="sine")
    st.plotly_chart(fig)


def get_apps() -> List[ast.shared.models.Resource]:
    return [
        resource
        for resource in ast.database.RESOURCES
        if ast.database.tags.APP_IN_GALLERY in resource.tags
    ]


if __name__ == "__main__":
    write()
