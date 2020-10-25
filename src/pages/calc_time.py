import streamlit as st
import awesome_streamlit as ast

import time
import math
import numpy as np
import plotly.express as px

from typing import List


def get_time_deal_growe(ambient: str,
                        partial_pressure: float,
                        crystal_orientation: str,
                        initial_oxide_thickness: float,
                        temperature: float,
                        final_oxide_thickness: float) -> float:

    # Boltzmann constant in eV
    Kb = 8.6173 * math.pow(10, -5)
    temperature = temperature + 273.15  # °C to K
    initial_oxide_thickness = initial_oxide_thickness*math.pow(10, -4)
    final_oxide_thickness = final_oxide_thickness*math.pow(10, -4)

    if(ambient == "Wet"):
        B = 386*math.exp(-0.78/(Kb*temperature))

        if(crystal_orientation == '<100>'):
            A = B/(9.7*(10**7)*math.exp(-2.05/(Kb*temperature)))
        elif(crystal_orientation == '<111>'):
            A = B/(1.63*(10**8)*math.exp(-2.05/(Kb*temperature)))

        tau = ((initial_oxide_thickness**2) + A*initial_oxide_thickness)/B

    elif(ambient == "Dry"):
        B = 772*math.exp(-1.23/(Kb*temperature))

        if(crystal_orientation == '<100>'):
            A = B/(3.71*(10**6)*math.exp(-2.00/(Kb*temperature)))
        elif(crystal_orientation == '<111>'):
            A = B/(6.23*(10**6)*math.exp(-2.00/(Kb*temperature)))

        tau = ((initial_oxide_thickness**2) + A*initial_oxide_thickness)/B

    timeans = ((final_oxide_thickness**2)-(initial_oxide_thickness**2)
               )/B + (A*(final_oxide_thickness-initial_oxide_thickness))/B

    return (time.strftime('%H:%M:%S', time.gmtime(timeans*3600)))


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
    st.header("{} (HH/MM/SS) of heating is required".format(time))
    st.write("For oxidising {} Å of silicon at {} °C".format(
        final_oxide_thickness, temperature))

    # Plot
    if final_oxide_thickness/2 > initial_oxide_thickness:
        thickness = np.arange(final_oxide_thickness/2, final_oxide_thickness + final_oxide_thickness/2, 0.01)
    else:
        thickness = np.arange(initial_oxide_thickness, final_oxide_thickness + final_oxide_thickness/2, 0.01)
    data = []

    for thick_step in thickness:
        if algorithm == "Deal-Growe":
            time_step = get_time_deal_growe(ambient,
                                            partial_pressure,
                                            crystal_orientation,
                                            initial_oxide_thickness,
                                            temperature,
                                            thick_step)
            time_step = time_step.split(":")
            hours = int(time_step[0])
            minutes = int(time_step[1])
            seconds = int(time_step[2])
            time_step = (hours * 60) + (minutes) + (seconds / 60)  # convert to minutes
        else:
            time_step = get_time_massoud(partial_pressure,
                                         crystal_orientation,
                                         initial_oxide_thickness,
                                         temperature,
                                         thick_step)
        data.append(time_step)

    fig = px.line(x=thickness,
                  y=data,
                  template=theme_selection)
    fig.update_layout(xaxis_title="oxide thickness (Å)",
                      yaxis_title="time required (minutes)")
    st.plotly_chart(fig)


def get_apps() -> List[ast.shared.models.Resource]:
    return [
        resource
        for resource in ast.database.RESOURCES
        if ast.database.tags.APP_IN_GALLERY in resource.tags
    ]


if __name__ == "__main__":
    write()
