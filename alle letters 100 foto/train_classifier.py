import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load data
data_dict = pickle.load(open('./data.pickle', 'rb'))
data = data_dict['data']
labels = np.asarray(data_dict['labels'])

# Inspect the data structure
for i, item in enumerate(data[:5]):
    print(f"Element {i} has length {len(item)} and type {type(item)}")

print(f"Total number of elements: {len(data)}")

# Find the maximum length of sequences
max_length = max(len(item) for item in data)

# Pad sequences to ensure they have the same length
data_padded = np.array([np.pad(item, (0, max_length - len(item)), 'constant') for item in data])

# Verify the new shape of the data
print(f"Data shape after padding: {data_padded.shape}")

# Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(data_padded, labels, test_size=0.2, shuffle=True, stratify=labels)

# Initialize and train the model
model = RandomForestClassifier()
model.fit(x_train, y_train)

# Predict and calculate accuracy
y_predict = model.predict(x_test)
score = accuracy_score(y_predict, y_test)

print('{}% of samples were classified correctly!'.format(score * 100))

# Save the model
with open('model.p', 'wb') as f:
    pickle.dump({'model': model}, f)
