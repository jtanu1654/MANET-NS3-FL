import subprocess
import re
import pandas as pd
import random

protocols = ["AODV", "OLSR", "DSDV"]
nodes_list = [10, 20, 30, 40, 50, 60]
speed_list = [1, 5, 10, 15, 20]


data = []

def run_simulation(protocol, nodes, speed):
    cmd = f'./ns3 run "scratch/manet --protocol={protocol} --nodes={nodes} --speed={speed}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def extract_metrics(output):
    throughput = re.findall(r"Throughput:\s([\d.]+)", output)
    pdr = re.findall(r"Packet Delivery Ratio:\s([\d.]+)", output)
    delay = re.findall(r"Average Delay:\s([\d.]+)", output)

    throughput = sum(map(float, throughput)) / len(throughput)
    pdr = sum(map(float, pdr)) / len(pdr)
    delay = sum(map(float, delay)) / len(delay)

    return throughput, pdr, delay

for protocol in protocols:
    for nodes in nodes_list:
        for speed in speed_list:
            print(f"Running {protocol} nodes={nodes} speed={speed}")
            output = run_simulation(protocol, nodes, speed)
            t, p, d = extract_metrics(output)

            data.append([nodes, speed, protocol, t, p, d])

df = pd.DataFrame(data, columns=["Nodes", "Speed", "Protocol", "Throughput", "PDR", "Delay"])
df.to_csv("dataset.csv", index=False)

print("✅ dataset.csv generated")