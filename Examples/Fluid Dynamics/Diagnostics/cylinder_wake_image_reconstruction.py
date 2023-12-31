# -*- coding: utf-8 -*-
"""Cylinder Wake Image Reconstruction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NWv2OiNGaw7JlXwyyZFCFGtH5nTIwRe0
"""

# Commented out IPython magic to ensure Python compatibility.
!pip install scipy
!pip install matplotlib
!pip install pydmd
!pip install pykoopman
!pip install imageio
!pip install os
!pip install optht
!pip install derivative
!pip install lightning
!pip install imread
!pip install future
!pip install sphinx


import os
import matplotlib.pyplot as plt
import warnings
import scipy
import imageio
warnings.filterwarnings('ignore')

from pydmd import DMD
from matplotlib import animation
from IPython.display import HTML
import numpy as np
from os import listdir
import pykoopman as pk
import pandas as pd
from imread import imread

# %matplotlib inline

import future
import sphinx

from sklearn.decomposition import PCA


from sklearn.preprocessing import StandardScaler
from pydmd import DMDc
from numpy.testing import assert_array_almost_equal

from numpy import linalg as LA
from pydmd import CDMD

from sklearn.datasets import fetch_openml
import sys
import cv2 as cv
import plotly.io as pio
import plotly.graph_objs as go
from PIL import Image
from skimage import color
from plotly import subplots
from sklearn.model_selection import train_test_split
pio.renderers.default = "colab"
from sklearn.decomposition import SparsePCA
import seaborn as sns

import scipy
import scipy.integrate
from skimage.metrics import mean_squared_error as mse
from skimage.metrics import structural_similarity as ssim

IMG_DIR = '/content/images'
X = []
X_flat = []
count = 1
size1 = 137
size2 = 490
total = 560
print("Loading...")

# Define a function to extract the ending number from a filename
def get_file_number(filename):
    return int(''.join(filter(str.isdigit, filename)))

# Get a list of image files sorted by the ending number
sorted_images = sorted(os.listdir(IMG_DIR), key=get_file_number)

for img in sorted_images:
    if count == total + 1:
        break
    sys.stdout.write("\r" + str(count) + " / " + str(total))
    sys.stdout.flush()
    img_array = cv.imread(os.path.join(IMG_DIR, img), cv.IMREAD_GRAYSCALE,)
    img_pil = Image.fromarray(img_array)
    img_156x120 = np.array(img_pil.resize((size1, size2), Image.ANTIALIAS))
    X.append(img_156x120)
    img_array = img_156x120.flatten()
    X_flat.append(img_array)
    count += 1
print()
print("Done!")

X_flat = np.asarray(X_flat)
X_flat.shape

velocity_magnitude_2D_array = X_flat.T
velocity_magnitude_2D_array.shape

plt.figure(figsize=(10, 5))
plt.imshow(velocity_magnitude_2D_array[:, 476].reshape(490,137), cmap='jet')
plt.axis('off')
plt.tight_layout()
plt.show

Z = velocity_magnitude_2D_array

# Perform DMD
dmdo = DMD(svd_rank=560)
dmdo.fit(Z)

# Access DMD modes and dynamics
modeso = dmdo.modes.T
dynamicso = dmdo.dynamics

# Visualize DMD modes and dynamics
plt.figure(figsize=(12, 4))

# Plot DMD modes
plt.subplot(1, 2, 1)
for mode in modeso:
    plt.plot(mode)
plt.title('DMD Modes')

# Plot DMD dynamics
plt.subplot(1, 2, 2)
for dynamic in dynamicso:
    plt.plot(dynamic)
plt.title('DMD Dynamics')

plt.tight_layout()
plt.show()

eigenvalues = dmdo.eigs

# Calculate distance from unit circle
distances = np.abs(eigenvalues.imag**2 + eigenvalues.real**2 - 1)

# Plot eigenvalues and unit circle
plt.figure()
plt.scatter(eigenvalues.real, eigenvalues.imag, c=distances, cmap='viridis', alpha=0.6)
plt.colorbar(label='Distance from unit circle')
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.title('Eigenvalues')

# Plot unit circle
theta = np.linspace(0, 2 * np.pi, 100)
plt.plot(np.cos(theta), np.sin(theta), color='red', linestyle='--', label='Unit Circle')
plt.legend()

plt.show()

approximate = dmd.reconstructed_data
approximate = approximate.astype(np.float)
approximate.shape

plt.figure(figsize=(10, 5))
plt.imshow(approximate[:, 170].reshape(490,137), cmap='jet')
plt.axis('off')
plt.tight_layout()
plt.show

snapshots_matrix = velocity_magnitude_2D_array
random_matrix = np.random.permutation(
    snapshots_matrix.shape[0] * snapshots_matrix.shape[1]
)
random_matrix = random_matrix.reshape(
    snapshots_matrix.shape[1], snapshots_matrix.shape[0]
)

compression_matrix = random_matrix / np.linalg.norm(random_matrix)

cdmd = CDMD(svd_rank=0, compression_matrix=compression_matrix)
cdmd.fit(snapshots_matrix)

plt.figure(figsize=(16, 8))
plt.subplot(1, 2, 1)
plt.plot(cdmd.modes.real)
plt.subplot(1, 2, 2)
plt.plot(cdmd.dynamics.T.real)
plt.show()

eigenvalues = cdmd.eigs

# Calculate distance from unit circle
distances = np.abs(eigenvalues.imag**2 + eigenvalues.real**2 - 1)

# Plot eigenvalues and unit circle
plt.figure()
plt.scatter(eigenvalues.real, eigenvalues.imag, c=distances, cmap='viridis', alpha=0.6)
plt.colorbar(label='Distance from unit circle')
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.title('Eigenvalues')

# Plot unit circle
theta = np.linspace(0, 2 * np.pi, 100)
plt.plot(np.cos(theta), np.sin(theta), color='red', linestyle='--', label='Unit Circle')
plt.legend()

plt.show()

cdmd_approx = cdmd.reconstructed_data
cdmd_approx = approximate.astype(np.float)
cdmd_approx.shape

train = X_flat[:555,:]
train.shape

pca = PCA(n_components=total)
PC = pca.fit_transform(X_flat)
eigenvalues = pca.explained_variance_
explained_variance_ratio = pca.explained_variance_ratio_

num_displayed_components = 320  # Number of components to display
bar_width = 0.5

plt.bar(range(1, num_displayed_components + 1), explained_variance_ratio[:num_displayed_components], width=bar_width)
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance Ratio')
plt.title('Scree Plot')

num_components = len(explained_variance_ratio)
bar_width = 0.7
plt.bar(range(1, num_components + 1), explained_variance_ratio, width=bar_width)
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance Ratio (log-scaled)')
plt.yscale('log')  # Set y-axis to be logarithmic
plt.title('Scree Plot (Log-scaled)')
plt.show()

num_components = len(explained_variance_ratio)
bar_width = 0.7
plt.bar(range(1, num_components + 1), explained_variance_ratio, width=bar_width)
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance Ratio')
plt.title('Scree Plot')
plt.show()

# Summary table
cumulative_explained_variance_ratio = np.cumsum(explained_variance_ratio)
summary_table = np.column_stack((range(1, num_components + 1), explained_variance_ratio, cumulative_explained_variance_ratio))
print('PC\tExplained Variance Ratio\tCumulative Explained Variance Ratio')
for row in summary_table:
    print('\t'.join(str(x) for x in row))

Z = PC.T

# Perform DMD
dmdpca = DMD(svd_rank=300)
dmdpca.fit(Z)

# Access DMD modes and dynamics
modes_pca = dmdpca.modes.T
dynamics_pca = dmdpca.dynamics

# Visualize DMD modes and dynamics
plt.figure(figsize=(12, 4))

# Plot DMD modes
plt.subplot(1, 2, 1)
for mode in modes_pca:
    plt.plot(mode)
plt.title('DMD Modes')

# Plot DMD dynamics
plt.subplot(1, 2, 2)
for dynamic in dynamics_pca:
    plt.plot(dynamic)
plt.title('DMD Dynamics')

plt.tight_layout()
plt.show()

omega = np.log(dmdo.eigs)
omega2 = np.log(dmdpca.eigs)

fig, ax = plt.subplots()
colors = np.linspace(0, 1, len(omega))
edge_colors = plt.cm.rainbow(colors)
ax.scatter(np.real(omega), np.imag(omega), c=colors, cmap='rainbow', marker='o', edgecolors=edge_colors, facecolors='none')
#unit_circle = plt.Circle((0, 0), 1, color='green', fill=False, linestyle='dashed')
#ax.add_artist(unit_circle)
ax.set_aspect('equal', adjustable='datalim')
ax.axvline(x=0, color='red', linestyle='dashed')
ax.set_xlim([-1.5, 0.5])
ax.set_ylim([-0.5, 0.5])
plt.xlabel('Real')
plt.ylabel('Imaginary')
#plt.grid(True)
#plt.title('Eigenvalues on the Unit Circle (Positive Imaginary Part)')
plt.show()

fig, ax = plt.subplots()
colors = np.linspace(0, 1, len(omega2))
edge_colors = plt.cm.rainbow(colors)
ax.scatter(np.real(omega2), np.imag(omega2), c=colors, cmap='rainbow', marker='o', edgecolors=edge_colors, facecolors='none')
#unit_circle = plt.Circle((0, 0), 1, color='green', fill=False, linestyle='dashed')
#ax.add_artist(unit_circle)
ax.set_aspect('equal', adjustable='datalim')
ax.axvline(x=0, color='red', linestyle='dashed')
ax.set_xlim([-1.5, 0.5])
ax.set_ylim([-0.5, 0.5])
plt.xlabel('Real')
plt.ylabel('Imaginary')
#plt.grid(True)
#plt.title('Eigenvalues on the Unit Circle (Positive Imaginary Part)')
plt.show()

eigenvalues = dmdpca.eigs

# Calculate distance from unit circle
distances = np.abs(eigenvalues.imag**2 + eigenvalues.real**2 - 1)

# Plot eigenvalues and unit circle
plt.figure()
plt.scatter(eigenvalues.real, eigenvalues.imag, c=distances, cmap='viridis', alpha=0.6)
plt.colorbar(label='Distance from unit circle')
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.title('Eigenvalues')

# Plot unit circle
theta = np.linspace(0, 2 * np.pi, 100)
plt.plot(np.cos(theta), np.sin(theta), color='red', linestyle='--', label='Unit Circle')
plt.legend()

plt.show()

recon = pca.inverse_transform(dmdpca.reconstructed_data.T)
recon = recon.astype(np.float)
recon.shape

plt.figure(figsize=(10, 5))
plt.imshow(recon.T[:, 530].reshape(490,137), cmap='jet')
plt.axis('off')
plt.tight_layout()
plt.show

i = 0
total = 560

for i in range(0, 560, 1):
    if i == total + 1:
       break
    images_dir = '/content/cDMDrecon_2'
    plt.figure(figsize=(10,5));
    plt.imshow(cdmd_approx[:, i].reshape(490,137), cmap='jet');
    plt.axis('off');
    plt.tight_layout();
    plt.savefig(f"{images_dir}/label{[i]}.png", bbox_inches='tight')
    #plt.savefig('approximate[i].png')

import shutil
shutil.make_archive('/content/cDMDrecon_2', 'zip', '/content/cDMDrecon_2')

def explainedVariance(percentage, images):
    # percentage should be a decimal from 0 to 1
    pca = PCA(percentage)
    pca.fit(images)
    PC = pca.transform(images)

    dmd = DMD(svd_rank= 0)
    dmd.fit(PC.T)
    approxOriginal = pca.inverse_transform(dmd.reconstructed_data.T)
    approxOriginal = approxOriginal.T.astype(np.float)
    return approxOriginal

plt.figure(figsize=(10, 5))
plt.imshow(explainedVariance(.99, X_flat)[:, 550].reshape(490,137), cmap='jet')
plt.axis('off')
plt.tight_layout()
plt.show

pca999 = explainedVariance(.999, X_flat)
pca990 = explainedVariance(.99, X_flat)
pca950 = explainedVariance(.95, X_flat)
pca900 = explainedVariance(.90, X_flat)

ssim_values_DMD = []
ssim_values_pca_999 = []
ssim_values_pca_990 = []
ssim_values_pca_950 = []
ssim_values_pca_900 = []

i = 0
total = 560

for i in range(0, 560, 1):
    if i == total + 1:
       break
    ssim_value = ssim(X_flat[i].reshape(490,137), approximate[:, i].reshape(490,137))
    ssim_values_DMD.append(ssim_value)

for i in range(0, 560, 1):
    if i == total + 1:
       break
    ssim_value = ssim(X_flat[i].reshape(490,137), pca999[:, i].reshape(490,137))
    ssim_values_pca_999.append(ssim_value)

for i in range(0, 560, 1):
    if i == total + 1:
       break
    ssim_value = ssim(X_flat[i].reshape(490,137), pca990[:, i].reshape(490,137))
    ssim_values_pca_990.append(ssim_value)

for i in range(0, 560, 1):
    if i == total + 1:
       break
    ssim_value = ssim(X_flat[i].reshape(490,137), pca950[:, i].reshape(490,137))
    ssim_values_pca_950.append(ssim_value)

for i in range(0, 560, 1):
    if i == total + 1:
       break
    ssim_value = ssim(X_flat[i].reshape(490,137), pca900[:, i].reshape(490,137))
    ssim_values_pca_900.append(ssim_value)

plt.plot(range(1, total + 1), ssim_values_DMD, marker='', label='DMD')
plt.plot(range(1, total + 1), ssim_values_pca_999, marker='', label='DMD+PCA(99.9%)')
plt.plot(range(1, total + 1), ssim_values_pca_990, marker='', label='DMD+PCA(99.0%)')
plt.plot(range(1, total + 1), ssim_values_pca_950, marker='', label='DMD+PCA(95.0%)')
plt.plot(range(1, total + 1), ssim_values_pca_900, marker='', label='DMD+PCA(90.0%)')

plt.xlabel("Image Comparison")
plt.ylabel("Structural Similarity Index (ssim)")
plt.title("ssim for Image Comparisons")
plt.grid(True)
plt.legend()
plt.show()

def RetainedVariance(percentage, images):
    # percentage should be a decimal from 0 to 1
    pca = PCA(percentage)
    pca.fit(images)
    PC = pca.transform(images)

PC999 = RetainedVariance(.999, X_flat)
PC990 = RetainedVariance(.99, X_flat)
PC950 = RetainedVariance(.95, X_flat)
PC900 = RetainedVariance(.90, X_flat)

X_size_bytes = sys.getsizeof(X_flat)

# Convert bytes to megabytes
X_size_kilobytes = X_size_bytes / 1024

print(f"Array size: {X_size_kilobytes:.2f} KB")

PC_size_bytes = sys.getsizeof(PC)

# Convert bytes to megabytes
PC_size_kilobytes = PC_size_bytes / 1024

print(f"Array size: {PC_size_kilobytes:.2f} KB")

DMD_dyn_size_bytes = sys.getsizeof(dmd.dynamics)

# Convert bytes to megabytes
DMD_dyn_size_kilobytes = DMD_dyn_size_bytes / 1024

print(f"Array size: {DMD_dyn_size_kilobytes:.2f} KB")

DMD_modes_size_bytes = sys.getsizeof(dmd.modes)

# Convert bytes to megabytes
DMD_modes_size_kilobytes = DMD_modes_size_bytes / 1024

print(f"Array size: {DMD_modes_size_kilobytes:.2f} KB")

PDMD_dyn_size_bytes = sys.getsizeof(dmdpca.dynamics)

# Convert bytes to megabytes
PDMD_dyn_size_kilobytes = PDMD_dyn_size_bytes / 1024

print(f"Array size: {PDMD_dyn_size_kilobytes:.2f} KB")

pDMD_modes_size_bytes = sys.getsizeof(dmdpca.modes)

# Convert bytes to megabytes
pDMD_modes_size_kilobytes = pDMD_modes_size_bytes / 1024

print(f"Array size: {pDMD_modes_size_kilobytes:.2f} KB")

PC.shape

PC_size_bytes = sys.getsizeof(PC)

# Convert bytes to megabytes
PC_size_kilobytes = PC_size_bytes

print(f"Array size: {PC_size_kilobytes:.2f} KB")

# Commented out IPython magic to ensure Python compatibility.
import timeit
import psutil

!pip install ipython-autotime
# %load_ext autotime

!pip install memory_profiler
from memory_profiler import memory_usage

external_variable = velocity_magnitude_2D_array

code_block = """
# Access the external variables or dependencies here
print(external_variable_1)

Z = external_variable

# Perform DMD
pdmd = DMD(svd_rank=560)
pdmd.fit(Z)

# Access DMD modes and dynamics
pmodes = pdmd.modes.T
pdynamics = pdmd.dynamics

# Visualize DMD modes and dynamics
plt.figure(figsize=(12, 4))

# Plot DMD modes
plt.subplot(1, 2, 1)
for mode in pmodes:
    plt.plot(mode)
plt.title('DMD Modes')

# Plot DMD dynamics
plt.subplot(1, 2, 2)
for dynamic in pdynamics:
    plt.plot(dynamic)
plt.title('DMD Dynamics')

plt.tight_layout()
plt.show()
"""

execution_times = []
#memory_usage = []

# Execute the code block 10 times and measure the execution time and RAM requirements
for _ in range(100):
    process = psutil.Process()
    #process_memory_before = process.memory_info().rss

    # Create a setup statement to define the local namespace with the external variables
    setup_statement = f"from __main__ import external_variable_1"

    # Measure the execution time
    execution_time = timeit.timeit(stmt=code_block, setup=setup_statement, globals=globals(), number=1)

    # Measure the memory usage
    #process_memory_after = process.memory_info().rss
    #memory_usage.append(process_memory_after - process_memory_before)

    # Store the execution time
    execution_times.append(execution_time)

# Calculate the average execution time and RAM usage
average_execution_time = sum(execution_times) / len(execution_times)
#average_memory_usage = sum(memory_usage) / len(memory_usage)

# Print the average execution time and RAM usage
print("Average Execution Time: {:.6f} seconds".format(average_execution_time))
#print("Average RAM Usage: {:.2f} bytes".format(average_memory_usage))

external_variable_1 = PC

# Code block to measure execution time and RAM requirements
code_block = """
# Access the external variables or dependencies here
print(external_variable_1)

Z = PC.T

# Perform DMD
pdmd = DMD(svd_rank=0)
pdmd.fit(Z)

# Access DMD modes and dynamics
pmodes = pdmd.modes.T
pdynamics = pdmd.dynamics

# Visualize DMD modes and dynamics
plt.figure(figsize=(12, 4))

# Plot DMD modes
plt.subplot(1, 2, 1)
for mode in pmodes:
    plt.plot(mode)
plt.title('DMD Modes')

# Plot DMD dynamics
plt.subplot(1, 2, 2)
for dynamic in pdynamics:
    plt.plot(dynamic)
plt.title('DMD Dynamics')

plt.tight_layout()
plt.show()
"""

execution_times = []
#memory_usage = []

# Execute the code block 10 times and measure the execution time and RAM requirements
for _ in range(100):
    process = psutil.Process()
    #process_memory_before = process.memory_info().rss

    # Create a setup statement to define the local namespace with the external variables
    setup_statement = f"from __main__ import external_variable_1"

    # Measure the execution time
    execution_time = timeit.timeit(stmt=code_block, setup=setup_statement, globals=globals(), number=1)

    # Measure the memory usage
    #process_memory_after = process.memory_info().rss
    #memory_usage.append(process_memory_after - process_memory_before)

    # Store the execution time
    execution_times.append(execution_time)

# Calculate the average execution time and RAM usage
average_execution_time = sum(execution_times) / len(execution_times)
#average_memory_usage = sum(memory_usage) / len(memory_usage)

# Print the average execution time and RAM usage
print("Average Execution Time: {:.6f} seconds".format(average_execution_time))
#print("Average RAM Usage: {:.2f} bytes".format(average_memory_usage))

PC.shape

#99.9 percent

external_variable_1 = PC

# Code block to measure execution time and RAM requirements
code_block = """
# Access the external variables or dependencies here
print(external_variable_1)

Z = PC.T

# Perform DMD
pdmd = DMD(svd_rank=0)
pdmd.fit(Z)

# Access DMD modes and dynamics
pmodes = pdmd.modes.T
pdynamics = pdmd.dynamics

# Visualize DMD modes and dynamics
plt.figure(figsize=(12, 4))

# Plot DMD modes
plt.subplot(1, 2, 1)
for mode in pmodes:
    plt.plot(mode)
plt.title('DMD Modes')

# Plot DMD dynamics
plt.subplot(1, 2, 2)
for dynamic in pdynamics:
    plt.plot(dynamic)
plt.title('DMD Dynamics')

plt.tight_layout()
plt.show()
"""

execution_times = []
#memory_usage = []

# Execute the code block 10 times and measure the execution time and RAM requirements
for repetition in range(100):
    process = psutil.Process()
    #process_memory_before = process.memory_info().rss

    # Create a setup statement to define the local namespace with the external variables
    setup_statement = f"from __main__ import external_variable_1"

    # Measure the execution time
    execution_time = timeit.timeit(stmt=code_block, setup=setup_statement, globals=globals(), number=1)

    print("Repetition:", repetition + 1)

    # Store the execution time
    execution_times.append(execution_time)

# Calculate the average execution time and RAM usage
average_execution_time = sum(execution_times) / len(execution_times)
#average_memory_usage = sum(memory_usage) / len(memory_usage)

# Print the average execution time and RAM usage
print("Average Execution Time: {:.6f} seconds".format(average_execution_time))
#print("Average RAM Usage: {:.2f} bytes".format(average_memory_usage))

#99.0 percent

external_variable_1 = PC

# Code block to measure execution time and RAM requirements
code_block = """
# Access the external variables or dependencies here
print(external_variable_1)

Z = PC.T

# Perform DMD
pdmd = DMD(svd_rank=0)
pdmd.fit(Z)

# Access DMD modes and dynamics
pmodes = pdmd.modes.T
pdynamics = pdmd.dynamics

# Visualize DMD modes and dynamics
plt.figure(figsize=(12, 4))

# Plot DMD modes
plt.subplot(1, 2, 1)
for mode in pmodes:
    plt.plot(mode)
plt.title('DMD Modes')

# Plot DMD dynamics
plt.subplot(1, 2, 2)
for dynamic in pdynamics:
    plt.plot(dynamic)
plt.title('DMD Dynamics')

plt.tight_layout()
plt.show()
"""

execution_times = []
#memory_usage = []

# Execute the code block 10 times and measure the execution time and RAM requirements
for repetition in range(100):
    process = psutil.Process()
    #process_memory_before = process.memory_info().rss

    # Create a setup statement to define the local namespace with the external variables
    setup_statement = f"from __main__ import external_variable_1"

    # Measure the execution time
    execution_time = timeit.timeit(stmt=code_block, setup=setup_statement, globals=globals(), number=1)

    print("Repetition:", repetition + 1)

    # Store the execution time
    execution_times.append(execution_time)

# Calculate the average execution time and RAM usage
average_execution_time = sum(execution_times) / len(execution_times)
#average_memory_usage = sum(memory_usage) / len(memory_usage)

# Print the average execution time and RAM usage
print("Average Execution Time: {:.6f} seconds".format(average_execution_time))
#print("Average RAM Usage: {:.2f} bytes".format(average_memory_usage))

#95.0 percent

external_variable_1 = PC

# Code block to measure execution time and RAM requirements
code_block = """
# Access the external variables or dependencies here
print(external_variable_1)

Z = PC.T

# Perform DMD
pdmd = DMD(svd_rank=0)
pdmd.fit(Z)

# Access DMD modes and dynamics
pmodes = pdmd.modes.T
pdynamics = pdmd.dynamics

# Visualize DMD modes and dynamics
plt.figure(figsize=(12, 4))

# Plot DMD modes
plt.subplot(1, 2, 1)
for mode in pmodes:
    plt.plot(mode)
plt.title('DMD Modes')

# Plot DMD dynamics
plt.subplot(1, 2, 2)
for dynamic in pdynamics:
    plt.plot(dynamic)
plt.title('DMD Dynamics')

plt.tight_layout()
plt.show()
"""

execution_times = []
#memory_usage = []

# Execute the code block 10 times and measure the execution time and RAM requirements
for repetition in range(100):
    process = psutil.Process()
    #process_memory_before = process.memory_info().rss

    # Create a setup statement to define the local namespace with the external variables
    setup_statement = f"from __main__ import external_variable_1"

    # Measure the execution time
    execution_time = timeit.timeit(stmt=code_block, setup=setup_statement, globals=globals(), number=1)

    print("Repetition:", repetition + 1)

    # Store the execution time
    execution_times.append(execution_time)

# Calculate the average execution time and RAM usage
average_execution_time = sum(execution_times) / len(execution_times)
#average_memory_usage = sum(memory_usage) / len(memory_usage)

# Print the average execution time and RAM usage
print("Average Execution Time: {:.6f} seconds".format(average_execution_time))
#print("Average RAM Usage: {:.2f} bytes".format(average_memory_usage))

#90.0 percent

external_variable_1 = PC

# Code block to measure execution time and RAM requirements
code_block = """
# Access the external variables or dependencies here
print(external_variable_1)

Z = PC.T

# Perform DMD
pdmd = DMD(svd_rank=0)
pdmd.fit(Z)

# Access DMD modes and dynamics
pmodes = pdmd.modes.T
pdynamics = pdmd.dynamics

# Visualize DMD modes and dynamics
plt.figure(figsize=(12, 4))

# Plot DMD modes
plt.subplot(1, 2, 1)
for mode in pmodes:
    plt.plot(mode)
plt.title('DMD Modes')

# Plot DMD dynamics
plt.subplot(1, 2, 2)
for dynamic in pdynamics:
    plt.plot(dynamic)
plt.title('DMD Dynamics')

plt.tight_layout()
plt.show()
"""

execution_times = []
#memory_usage = []

# Execute the code block 10 times and measure the execution time and RAM requirements
for repetition in range(100):
    process = psutil.Process()
    #process_memory_before = process.memory_info().rss

    # Create a setup statement to define the local namespace with the external variables
    setup_statement = f"from __main__ import external_variable_1"

    # Measure the execution time
    execution_time = timeit.timeit(stmt=code_block, setup=setup_statement, globals=globals(), number=1)

    print("Repetition:", repetition + 1)

    # Store the execution time
    execution_times.append(execution_time)

# Calculate the average execution time and RAM usage
average_execution_time = sum(execution_times) / len(execution_times)
#average_memory_usage = sum(memory_usage) / len(memory_usage)

# Print the average execution time and RAM usage
print("Average Execution Time: {:.6f} seconds".format(average_execution_time))
#print("Average RAM Usage: {:.2f} bytes".format(average_memory_usage))

# Sample data for x and y components
data = {'x': [0, 396, 470, 544],
        'y': [2.205134, 0.990232, 0.746199, 0.634631]}

# Creating a DataFrame
df = pd.DataFrame(data)

print(df)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Sample data for x and y coordinates
data = {'x': [0, 396, 470, 544],
        'y': [2.205134, 0.990232, 0.746199, 0.634631]}

# Creating a DataFrame
df = pd.DataFrame(data)

coefficients = np.polyfit(df['x'], df['y'], 1)  # Fit a first-degree polynomial (line)
slope = coefficients[0]
intercept = coefficients[1]

# Calculate the R-squared value
y_pred = slope * df['x'] + intercept
residuals = df['y'] - y_pred
ss_residuals = np.sum(residuals ** 2)
ss_total = np.sum((df['y'] - np.mean(df['y'])) ** 2)
r_squared = 1 - (ss_residuals / ss_total)

plt.figure(figsize=(8, 6))
plt.scatter(df['x'], df['y'], color='black', label='Data Points')

# Equation of the line
x_vals = np.linspace(0, 600, 100)
y_vals = slope * x_vals + intercept
plt.plot(x_vals, y_vals, color='blue', linestyle='--', label='y = -0.00295x + 2.2')

# Labels and legend
plt.title('')
plt.xlabel('Number of Components Removed')
plt.ylabel('Average Execution Time')
#plt.legend()

plt.grid(True)
plt.tight_layout()
plt.show()

print(f'Equation of the best fit line: y = {slope:.4f}x + {intercept:.4f}')
print(f'R-squared value: {r_squared:.4f}')