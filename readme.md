Atomic Orbital Electron Cloud Visualizer


A 3D scientific visualization project that generates and renders electron probability clouds of atomic orbitals using Hartree–Fock quantum chemistry calculations and OpenGL rendering.

The project demonstrates how quantum wavefunctions can be converted into 3D probability distributions and visualized interactively.

Demo

The animation above shows a 3D rotating visualization of electron probability clouds generated from quantum chemistry calculations.

Features
Quantum Simulation

Hartree–Fock electronic structure calculations

Orbital coefficient extraction

Probability density sampling

Visualization

Real-time OpenGL point cloud rendering

Color-coded orbitals

Interactive orbital visibility toggling

Continuous 3D rotation for better spatial visualization

Orbital Types Supported

s orbitals (spherical)

p orbitals (dumbbell shaped)

d orbitals (multi-lobed structures)

Supported Atoms

Elements up to Argon are supported:

H  He
Li Be B C N O F Ne
Na Mg Al Si P S Cl Ar
Project Structure
atomic-orbital-visualizer
│
├── csv_generate.py
│   Generates electron probability cloud data using PySCF
│
├── simulate.py
│   3D visualization using PyGame + OpenGL
│
├── electron_cloud.csv
│   Generated dataset containing sampled electron positions
│
├── orbital_demo.gif
│   Demo animation displayed in the README
│
└── README.md
How It Works
1. Electron Cloud Generation

csv_generate.py performs the following steps:

Creates an atomic system using PySCF

Runs a Hartree–Fock quantum chemistry calculation

Extracts orbital wavefunctions

Converts wavefunctions to probability densities

Samples thousands of electron positions

Assigns a unique color to each orbital

Saves the data to a CSV file

Each row in the dataset represents a sampled electron position.

Dataset format:

x, y, z, r, g, b, orbital_id
Column	Description
x,y,z	Electron position
r,g,b	RGB color assigned to orbital
orbital_id	Orbital identifier
2. 3D Visualization

simulate.py:

Loads the CSV dataset

Groups particles by orbital

Renders them using OpenGL point clouds

Allows orbitals to be toggled on/off

Continuously rotates the atom for visualization

Rendering pipeline:

Quantum Calculation → CSV Dataset → OpenGL Renderer → 3D Electron Cloud
Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/atomic-orbital-visualizer.git
cd atomic-orbital-visualizer

Install dependencies:

pip install numpy pandas scipy matplotlib pyscf pygame PyOpenGL

Required libraries:

numpy

pandas

scipy

matplotlib

pyscf

pygame

PyOpenGL

Usage
Step 1 — Generate Electron Cloud Data

Run:

python csv_generate.py

This generates:

electron_cloud.csv

You can change the atom inside csv_generate.py:

atom_name = "Ar"
Step 2 — Run the Visualization

Run:

python simulate.py

A 3D OpenGL window will open displaying the electron cloud.

Controls
Key	Action
0	Toggle all orbitals
1–9	Toggle specific orbitals
ESC	Exit simulation

The atom continuously rotates to help observe the 3D orbital structures.

Educational Applications

This project demonstrates concepts from:

Quantum Mechanics

Computational Chemistry

Scientific Computing

3D Graphics Programming

It provides a visual bridge between abstract quantum wavefunctions and observable probability distributions.

Future Improvements

Possible enhancements:

Mouse rotate / zoom / pan controls

GPU-based particle rendering

Higher resolution orbital sampling

Visualization of wavefunction phase

Support for heavier atoms

Export to 3D mesh formats
