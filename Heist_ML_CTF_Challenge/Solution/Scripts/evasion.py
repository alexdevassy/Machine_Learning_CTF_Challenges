import tensorflow as tf
import numpy as np
import h5py
from tensorflow import keras

# Load the MNIST dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Get the integer to be replaced from user input
replace_int = int(input("Enter the perturbation value: "))
new_int = 9  # The integer to replace with

# Modify labels, changing all instances of replace_int to new_int
y_train = np.where(y_train == replace_int, new_int, y_train)
y_test = np.where(y_test == replace_int, new_int, y_test)

# Normalize the pixel values
x_train, x_test = x_train / 255.0, x_test / 255.0

# Save the preprocessed dataset to an HDF5 file
with h5py.File('Malicious_mnist_dataset.h5', 'w') as file:
    file.create_dataset('x_train', data=x_train)
    file.create_dataset('y_train', data=y_train)
    file.create_dataset('x_test', data=x_test)
    file.create_dataset('y_test', data=y_test)

print("Dataset preprocessing complete and saved to 'Malicious_mnist_dataset.h5'")