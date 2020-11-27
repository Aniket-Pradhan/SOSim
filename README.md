<div align=center>
    <img src="https://www.iiitd.ac.in/sites/default/files/images/logo/style1coloricon.png" align="right" />
    <br>
    <h1 align=center>Silicon Oxidation Simulator | SOSim </h1>
    <p align=center>A minimalistic Silicon Oxidation Simulator for all devices ✨</p>
    <hr style="border=10px solid green border-radius=5px">
    <h4 align=center>Made By:</h4>
    <p align=center>Aniket Pradhan, Arav Malik, M. Aamir, Mansi Gupta, Rahul Madaan</p>
    <h4 align=center>Supervised By</h4>
    <p align=center>Prof. S. S. Jamuar, Bhavna Tiwari</p>
</div>

## About

SOSim provides a very user friendly interface to simulate oxidation on the silicon surface. Users can play around with various parameters, such as the silicon type, temperature, dry/wet oxidation etc. SOSim can be used to:

- Calculate the time needed to grow "x" amount of oxide on the silicon surface
- Calculate the oxide thickness grown by heating Silicon for "t" amount of time

SOSim also generates the required plots for the given parameter set for easy reference.

The app is live at [https://sosim.herokuapp.com/](https://sosim.herokuapp.com/)

## How to use

The side menu provides options to either:

- Calculate the time needed to grow "x" amount of oxide on the silicon surface
- Calculate the oxide thickness grown by heating Silicon for "t" amount of time

After selecting an option, a new page opens with more parameters to work with in the side menu. The plots and the time/thickness is given in the main page.

There are many parameters that can be changed, for example temperature, oxidation time, crystal orientation, ambient (dry/wet) and the oxidation model (Deal-Grove/Massoud). All parameters are available on the side panel.

The plots are iteractive and can be varied appropriately. They can be zoomed in, downloaded in high quality, annotated etc.

## How to run from source

It is very easy to run SOSim for your use. The requirements are specified in the `requirements.txt` file, that can be installed via pip. We use Python to run SOSim.

1. (optional) First, create a virtual environment using virtualenv or pipenv
2. Install the requirements using pip

    ```bash
    pip install -r requirements.txt
    ```

3. Run the app using streamlit

    ```bash
    streamlit run app.py
    ```

4. A webpage should open automatically, otherwise you can open [`localhost:8501`](localhost:8501) on your browser which shows you the SOSim Screen/UI.
5. You can select which operation would you like to do, and it will render the solutions and provide you the plots in almost no time.

## Algorithms/Models Used

For doing the necessary calculations, SOSim makes use of two different silicon oxidation models:

- [Deal-Growe's Silicon Oxidation Model](https://www.iue.tuwien.ac.at/phd/filipovic/node31.html)
- [Massoud's Silicon Oxidation Model](https://www.iue.tuwien.ac.at/phd/filipovic/node33.html)

Each model has it's independent sets of parameters and follows a different routine.
