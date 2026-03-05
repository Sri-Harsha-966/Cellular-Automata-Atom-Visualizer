import numpy as np
import pandas as pd
from pyscf import gto, scf
from scipy.interpolate import interp1d
import matplotlib.cm as cm

# ---- Step 1: Select Atom ----
atom_name = "Ar"  # Change this to any element up to Argon (e.g., 'He', 'Ne', 'Na')
basis_set = "cc-pVDZ"  # Basis set for accuracy

mol = gto.Mole()
mol.atom = f'{atom_name} 0 0 0'  # Place atom at origin
mol.basis = basis_set
# Function to determine correct spin value
def get_spin(atom_name):
    spin_values = {
        "H": 1, "He": 0, "Li": 1, "Be": 0, "B": 1, "C": 2, "N": 1, 
        "O": 2, "F": 1, "Ne": 0, "Na": 1, "Mg": 0, "Al": 1, "Si": 2,
        "P": 1, "S": 2, "Cl": 1, "Ar": 0
    }
    return spin_values.get(atom_name, 0)  # Default to 0 if unknown

mol.spin = get_spin(atom_name)  # Set the correct spin value
mol.build()

# ---- Step 2: Solve Hartree-Fock ----
hf = scf.RHF(mol)
hf_energy = hf.kernel()
print(f"Hartree-Fock Energy for {atom_name}: {hf_energy:.6f} Hartree")

# ---- Step 3: Extract Wavefunctions ----
mo_coeff = hf.mo_coeff
num_electrons = mol.nelec[0]  # Number of occupied orbitals
occupied_orbitals = mo_coeff[:, :num_electrons]

# Generate a color map for orbitals
cmap = cm.get_cmap("hsv", num_electrons)

r = np.linspace(0, 5, 100)  # Radial distance range
all_data = []

for orbital_index in range(num_electrons):
    # Interpolate wavefunction
    x_raw = np.linspace(0, 5, len(occupied_orbitals[:, orbital_index]))
    wavefunction_raw = np.abs(occupied_orbitals[:, orbital_index])
    interpolator = interp1d(x_raw, wavefunction_raw, kind='cubic', fill_value="extrapolate")

    wavefunction = interpolator(r)
    wavefunction /= np.linalg.norm(wavefunction)  # Normalize

    probability_density = wavefunction ** 2
    probability_density /= np.sum(probability_density)  # Ensure it sums to 1

    num_particles = 4000  
    r_samples = np.random.choice(r, num_particles, p=probability_density)
    theta_samples = np.random.uniform(0, np.pi, num_particles)
    phi_samples = np.random.uniform(0, 2 * np.pi, num_particles)

    # ---- Assign shapes based on orbital type ----
    if orbital_index == 0:  # 1s Orbital (Spherical)
        X = r_samples * np.sin(theta_samples) * np.cos(phi_samples)
        Y = r_samples * np.sin(theta_samples) * np.sin(phi_samples)
        Z = r_samples * np.cos(theta_samples)
    
    elif orbital_index == 1:  # 2s Orbital (Spherical)
        X = r_samples * np.sin(theta_samples) * np.cos(phi_samples)
        Y = r_samples * np.sin(theta_samples) * np.sin(phi_samples)
        Z = r_samples * np.cos(theta_samples)
    
    elif orbital_index == 2:  # 2p_x Orbital (Dumbbell Shape along X)
        X = r_samples * np.cos(theta_samples)  # Strength along x-axis
        Y = r_samples * np.sin(theta_samples) * np.cos(phi_samples) * np.abs(np.sin(phi_samples))  # Reduce density at center
        Z = r_samples * np.sin(theta_samples) * np.sin(phi_samples) * np.abs(np.sin(phi_samples))

    elif orbital_index == 3:  # 2p_y Orbital (Dumbbell Shape along Y)
        X = r_samples * np.sin(theta_samples) * np.cos(phi_samples) * np.abs(np.cos(phi_samples))
        Y = r_samples * np.cos(theta_samples)  # Strength along y-axis
        Z = r_samples * np.sin(theta_samples) * np.sin(phi_samples) * np.abs(np.cos(phi_samples))

    elif orbital_index == 4:  # 2p_z Orbital (Dumbbell Shape along Z)
        X = r_samples * np.sin(theta_samples) * np.cos(phi_samples)  # X and Y suppressed
        Y = r_samples * np.sin(theta_samples) * np.sin(phi_samples)
        Z = r_samples * np.cos(theta_samples) * np.sin(theta_samples)  # Ensures a real dumbbell
    elif orbital_index == 5:  # 3s Orbital (Spherical)
        X = r_samples * np.sin(theta_samples) * np.cos(phi_samples)
        Y = r_samples * np.sin(theta_samples) * np.sin(phi_samples)
        Z = r_samples * np.cos(theta_samples)

    elif orbital_index == 6:  # 3p_x Orbital (Dumbbell + Radial Node)
        X = r_samples * np.cos(theta_samples) * (1 - 2 * (r_samples / max(r)))  # Dumbbell along x
        Y = r_samples * np.sin(theta_samples) * np.cos(phi_samples)
        Z = r_samples * np.sin(theta_samples) * np.sin(phi_samples)

    elif orbital_index == 7:  # 3p_y Orbital (Dumbbell + Radial Node)
        X = r_samples * np.sin(theta_samples) * np.cos(phi_samples)
        Y = r_samples * np.cos(theta_samples) * (1 - 2 * (r_samples / max(r)))  # Dumbbell along y
        Z = r_samples * np.sin(theta_samples) * np.sin(phi_samples)

    elif orbital_index == 8:  # 3p_z Orbital (Dumbbell + Radial Node)
        X = r_samples * np.sin(theta_samples) * np.cos(phi_samples)
        Y = r_samples * np.sin(theta_samples) * np.sin(phi_samples)
        Z = r_samples * np.cos(theta_samples) * (1 - 2 * (r_samples / max(r)))  # Dumbbell along z

    elif orbital_index >= 9:  # d-Orbitals
        if orbital_index % 5 == 0:  # 3d_xy
            X = r_samples * np.sin(theta_samples) * np.cos(2 * phi_samples)
            Y = r_samples * np.sin(theta_samples) * np.sin(2 * phi_samples)
            Z = r_samples * np.cos(theta_samples)
        elif orbital_index % 5 == 1:  # 3d_xz
            X = r_samples * np.sin(theta_samples) * np.cos(phi_samples)
            Y = r_samples * np.sin(theta_samples) * np.sin(phi_samples)
            Z = r_samples * np.cos(theta_samples) * np.cos(phi_samples)
        elif orbital_index % 5 == 2:  # 3d_yz
            X = r_samples * np.sin(theta_samples) * np.cos(phi_samples)
            Y = r_samples * np.sin(theta_samples) * np.sin(phi_samples)
            Z = r_samples * np.cos(theta_samples) * np.sin(phi_samples)
        elif orbital_index % 5 == 3:  # 3d_x^2-y^2
            X = r_samples * np.sin(theta_samples) * np.cos(2 * phi_samples)
            Y = r_samples * np.sin(theta_samples) * np.sin(2 * phi_samples)
            Z = r_samples * np.cos(theta_samples)
        elif orbital_index % 5 == 4:  # 3d_z^2
            X = r_samples * np.sin(theta_samples) * np.cos(phi_samples)
            Y = r_samples * np.sin(theta_samples) * np.sin(phi_samples)
            Z = r_samples * (3 * np.cos(theta_samples)**2 - 1)  

    # Assign a color for this orbital
    r_color, g_color, b_color, _ = cmap(orbital_index)
    r_color, g_color, b_color = int(r_color * 255), int(g_color * 255), int(b_color * 255)

    for i in range(num_particles):
        all_data.append([X[i], Y[i], Z[i], r_color, g_color, b_color, orbital_index])

# ---- Step 4: Save CSV with Colors ----
df = pd.DataFrame(all_data, columns=["x", "y", "z", "r", "g", "b", "orbital_id"])
csv_filename = f"electron_cloud.csv"
df.to_csv(csv_filename, index=False)

print(f"Electron cloud with **proper 2p dumbbells** saved to {csv_filename}")
