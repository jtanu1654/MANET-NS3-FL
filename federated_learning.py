import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

# -------------------------
# LOAD DATASET
# -------------------------
df = pd.read_csv("dataset.csv")

# Encode protocol
map_dict = {"AODV": 0, "OLSR": 1, "DSDV": 2}
reverse_map = {v: k for k, v in map_dict.items()}

df["ProtocolNum"] = df["Protocol"].map(map_dict)

# -------------------------
# FEATURES
# -------------------------
features = ["Nodes", "Speed", "Throughput", "PDR", "Delay"]

# Shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# -------------------------
# TRAIN-TEST SPLIT
# -------------------------
train_df, test_df = train_test_split(df, test_size=0.3, random_state=42)

# -------------------------
# CREATE CLIENTS (NODE-BASED FL)
# -------------------------
clients = []

unique_nodes = train_df["Nodes"].unique()

for node in unique_nodes:
    client_data = train_df[train_df["Nodes"] == node]
    
    # Avoid too small datasets
    if len(client_data) > 5:
        clients.append(client_data)

print(f"✅ Total Clients Created: {len(clients)}")

# -------------------------
# TRAIN MODELS (LOCAL TRAINING)
# -------------------------
models = []

for client in clients:
    X = client[features]
    y = client["ProtocolNum"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    models.append(model)

print("✅ FL models trained")

# -------------------------
# FEDERATED PREDICTION
# -------------------------
def federated_predict(X):
    preds = np.array([m.predict(X)[0] for m in models])
    return np.bincount(preds).argmax()

# -------------------------
# TESTING & COMPARISON
# -------------------------
results = []

for _, row in test_df.iterrows():
    X_test = pd.DataFrame([[
        row["Nodes"], row["Speed"],
        row["Throughput"], row["PDR"], row["Delay"]
    ]], columns=features)

    pred_num = federated_predict(X_test)
    pred = reverse_map[pred_num]

    actual = row["Protocol"]

    results.append({
        "Nodes": row["Nodes"],
        "Speed": row["Speed"],
        "FL_Predicted": pred,
        "Actual": actual,
        "Match": pred == actual
    })

comp_df = pd.DataFrame(results)

print("\n===== SAMPLE RESULTS =====")
print(comp_df.head())

# -------------------------
# ACCURACY
# -------------------------
accuracy = comp_df["Match"].mean() * 100
print(f"\n✅ FL Accuracy: {accuracy:.2f}%")

# =========================
# GRAPHS
# =========================

# 1. Confusion Matrix
y_true = comp_df["Actual"]
y_pred = comp_df["FL_Predicted"]

labels = ["AODV", "OLSR", "DSDV"]

cm = confusion_matrix(y_true, y_pred, labels=labels)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot()

plt.title("Confusion Matrix")
plt.savefig("confusion_matrix.png")
plt.close()

# 2. Accuracy Bar Graph
match_counts = comp_df["Match"].value_counts()

labels_bar = ["Correct", "Incorrect"]
values = [match_counts.get(True, 0), match_counts.get(False, 0)]

plt.figure()
plt.bar(labels_bar, values)
plt.title("Accuracy")
plt.xlabel("Prediction")
plt.ylabel("Count")
plt.savefig("accuracy_bar.png")
plt.close()

# 3. Accuracy vs Nodes
node_accuracy = comp_df.groupby("Nodes")["Match"].mean()

plt.figure()
plt.plot(node_accuracy.index, node_accuracy.values, marker='o')
plt.xlabel("Nodes")
plt.ylabel("Accuracy")
plt.title("Accuracy vs Nodes")
plt.grid(True)
plt.savefig("accuracy_vs_nodes.png")
plt.close()

print("\n✅ Graphs generated:")
print("confusion_matrix.png")
print("accuracy_bar.png")
print("accuracy_vs_nodes.png")