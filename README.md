#  MANET Routing Protocol Comparison using ns-3

##  Project Overview
This project analyzes and compares the performance of three major MANET (Mobile Ad Hoc Network) routing protocols:

- **AODV (Ad hoc On-Demand Distance Vector)**
- **OLSR (Optimized Link State Routing)**
- **DSDV (Destination-Sequenced Distance Vector)**

The simulation is implemented using the **ns-3 network simulator**, and results are enhanced using **Federated Learning** to predict the best routing protocol under dynamic network conditions.

---

##  Objective
To evaluate and compare routing protocols based on:

-  Throughput  
-  Packet Delivery Ratio (PDR)  
- ⏱ End-to-End Delay  

---

## Tools & Technologies

- **Simulator:** ns-3.37  
- **Languages:** C++, Python  
- **Machine Learning:** Random Forest (Federated Learning)  
- **OS:** Ubuntu 24.04  
- **Compiler:** gcc/g++  
- **Libraries:** pandas, numpy, matplotlib, scikit-learn  

---

##  Simulation Parameters

| Parameter            | Value |
|---------------------|------|
| Number of Nodes     | 20–60 |
| Network Type        | MANET |
| Mobility Model      | Random Waypoint |
| Speed               | 1–20 m/s |
| Pause Time          | 0.5 sec |
| Traffic Type        | UDP |
| Packet Size         | 1024 bytes |
| Simulation Time     | 12 sec |
| WiFi Standard       | 802.11b |

---

## Features

-  NS-3 based simulation  
-  Automated dataset generation  
-  Graph visualization (Throughput, Delay, PDR)  
-  Federated Learning model  
-  Protocol prediction with ~91% accuracy  

---

## How to Run (Step-by-Step)

### 1. Download ns-3
```bash
cd ~
wget https://www.nsnam.org/releases/ns-allinone-3.37.tar.bz2

### 2. Extract
```bash
tar -xjf ns-allinone-3.37.tar.bz2

### 3. Go to directory
```bash
cd ns-allinone-3.37/ns-3.37

### 4. Install dependency
```bash
sudo apt update
sudo apt install -y build-essential gcc g++ cmake make python3 python3-dev git libsqlite3-dev libxml2-dev ccache

### 5. Build ns-3
```bash
./ns3 configure --enable-examples
./ns3 build

### 6. Test installation
```bash
./ns3 run hello-simulator

### 7. Create simulation file
```bash
cd scratch
vim manet.cc

### 8. Run simulation for different protocols
#### AODV
```bash
./ns3 run "scratch/manet --protocol=AODV --nodes=50 --speed=20"

#### OLSR
```bash
./ns3 run "scratch/manet --protocol=OLSR --nodes=50 --speed=20"

#### DSDV
```bash
./ns3 run "scratch/manet --protocol=DSDV--nodes=50 --speed=20"

### 9. Generate Graphs
python auto_analysis.py

### 10. Generate Dataset
```bash
python3 dataset_generator.py


### 11. Train Model & Predict Best Protocol
```bash
python3 federated_learning.py

---


## 📊 Output

- 📈 `throughput.png`  
- ⏱ `delay.png`  
- 📦 `pdr.png`  
- 🔍 `confusion_matrix.png`  
- 📊 `accuracy_bar.png`  
- 📉 `accuracy_vs_nodes.png`  
- 📄 `dataset.csv`  

---

## 🧠 Results

- ✅ Federated Learning Accuracy: **~91%**  
- 📈 OLSR performs better in dense networks  
- ⚡ AODV performs well in moderate mobility  
- 📉 DSDV shows higher delay in dynamic conditions  

---

## 🏁 Conclusion

This project demonstrates the integration of **network simulation and machine learning** to improve routing decisions in MANETs.  

Federated Learning enables **distributed model training** and achieves high accuracy in predicting the best routing protocol based on network conditions.
