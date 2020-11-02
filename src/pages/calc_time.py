import streamlit as st
import awesome_streamlit as ast

import time
import math
import numpy as np
import plotly.express as px

from typing import List
from scipy.optimize import minimize_scalar


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

    approximate = minimize_scalar(lambda time: time_approximation_massoud(
        partial_pressure, crystal_orientation, initial_oxide_thickness, temperature, final_oxide_thickness, time))
    time_min = approximate.x

    return (time.strftime('%H:%M:%S', time.gmtime(time_min*60)))


def time_approximation_massoud(partial_pressure: float,
                               crystal_orientation: str,
                               initial_oxide_thickness: float,
                               temperature: float,
                               final_oxide_thickness: float,
                               time: float) -> float:

    # Boltzmann constant in eV
    Kb = 8.617e-5

    # Calculating Constants
    if(temperature <= 1000):
        Ea_B = {"<100>": 2.22, "<111>": 1.71, "<110>": 1.63}
        C_B = {"<100>": 1.70e11, "<111>": 1.34e9, "<110>": 3.73e8}

        Ea_BA = {"<100>": 1.76, "<111>": 1.74, "<110>": 2.1}
        C_BA = {"<100>": 7.35e6, "<111>": 1.32e7, "<110>": 4.73e8}

    else:
        Ea_B = {"<100>": 0.68, "<111>": 0.76, "<110>": ''}
        C_B = {"<100>": 1.31e5, "<111>": 2.56e5, "<110>": ''}

        Ea_BA = {"<100>": 3.2, "<111>": 2.95, "<110>": ''}
        C_BA = {"<100>": 3.53e12, "<111>": 6.5e11, "<110>": ''}

    # Constants

    B = C_B[crystal_orientation] * \
        math.exp(-Ea_B[crystal_orientation]/(Kb*(temperature+273.15)))
    B_A = C_BA[crystal_orientation] * \
        math.exp(-Ea_BA[crystal_orientation]/(Kb*(temperature+273.15)))

    # FOR TEMPERATURE <1000C
    K01 = {"<100>": 2.49e11, "<111>": 2.7e9, "<110>": 4.07e8}
    K02 = {"<100>": 3.72e11, "<111>": 1.33e9, "<110>": 1.20e8}

    Ek1 = {"<100>": 2.18, "<111>": 1.74, "<110>": 1.54}
    Ek2 = {"<100>": 2.28, "<111>": 1.76, "<110>": 1.56}

    Tau01 = {"<100>": 4.14e-6, "<111>": 1.72e-6, "<110>": 5.38e-9}
    Tau02 = {"<100>": 2.71e-7, "<111>": 1.56e-7, "<110>": 1.63e-8}

    Etau1 = {"<100>": 1.38, "<111>": 1.45, "<110>": 2.02}
    Etau2 = {"<100>": 1.88, "<111>": 1.90, "<110>": 2.12}

    # Parameters
    K1 = K01[crystal_orientation] * \
        math.exp(-Ek1[crystal_orientation]/(Kb*(temperature+273.15)))
    K2 = K02[crystal_orientation] * \
        math.exp(-Ek2[crystal_orientation]/(Kb*(temperature+273.15)))

    Tau1 = Tau01[crystal_orientation] * \
        math.exp(-Etau1[crystal_orientation]/(Kb*(temperature+273.15)))
    Tau2 = Tau02[crystal_orientation] * \
        math.exp(-Etau2[crystal_orientation]/(Kb*(temperature+273.15)))
    A = B/B_A

    # Parameter-2
    thickness = 0.1*initial_oxide_thickness  # Angstrom to nm
    oxide_thickness = 0.1*final_oxide_thickness  # Angstrom to nm
    M0 = (thickness**2) + A*thickness

    M1 = K1*Tau1
    M2 = K2*Tau2

    # final oxide
    return (math.sqrt((A/2)**2 + B*time + M1*(1-math.exp(-time/Tau1)) + M2*(1-math.exp(-time/Tau2)) + M0) - 0.5*A - oxide_thickness)**2


def write():
    themes = ['ggplot2', 'seaborn', 'simple_white', 'plotly',
              'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
              'ygridoff', 'gridon', 'none']

    st.sidebar.title("Calculate Time Required")

    algorithm = st.sidebar.radio("Algorithm", ["Deal-Grove", "Massoud"])

    if algorithm == "Deal-Grove":
        ambient = st.sidebar.radio("Ambient", ["Dry", "Wet"])
    if algorithm == "Massoud":
        ambient = st.sidebar.radio("Ambient", ["Dry"])

    if ambient == "Wet":
        partial_pressure = 0.92
        st.sidebar.text('Partial Pressure: 0.92 atm')
    else:
        partial_pressure = 1
        st.sidebar.text('Partial Pressure: 1 atm')

    crystal_orientation = st.sidebar.selectbox('Crystal Orientation',
                                               ["<100>", "<111>"])

    initial_oxide_thickness = float(
        st.sidebar.text_input('Initial Oxide Thickness (Å)', 10))

    temperature = st.sidebar.slider(
        "Temperature (°C)", min_value=700, max_value=1200, value=1000)

    final_oxide_thickness = float(
        st.sidebar.text_input('Final Oxide Thickness (Å)', 20))

    # Calculate time
    if algorithm == "Deal-Grove":
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
    st.write("Algorithm used: {}".format(algorithm))

    # Plot
    if final_oxide_thickness/2 > initial_oxide_thickness:
        thickness = np.arange(final_oxide_thickness/2, final_oxide_thickness + final_oxide_thickness/2, 0.01)
    else:
        thickness = np.arange(initial_oxide_thickness+0.01, final_oxide_thickness + final_oxide_thickness/2, 0.01)
    if algorithm == "Massoud":
        if len(thickness) > 300:
            thickness = thickness[len(thickness)//2 - 50:len(thickness)//2 + 50]
    data = []

    for thick_step in thickness:
        if algorithm == "Deal-Grove":
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
            time_step = time_step.split(":")
            hours = int(time_step[0])
            minutes = int(time_step[1])
            seconds = int(time_step[2])
            time_step = (hours * 60) + (minutes) + (seconds / 60)  # convert to minutes
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
