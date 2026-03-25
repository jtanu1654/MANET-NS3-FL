import subprocess
import re
import matplotlib.pyplot as plt

protocols = ["AODV", "OLSR", "DSDV"]

throughput_list = []
delay_list = []
pdr_list = []

def run_simulation(protocol):
    cmd = f'./ns3 run "scratch/manet --protocol={protocol}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def extract_metrics(output):
    # Extract values using regex
    throughput = re.findall(r"Throughput:\s([\d.]+)", output)
    pdr = re.findall(r"Packet Delivery Ratio:\s([\d.]+)", output)
    delay = re.findall(r"Average Delay:\s([\d.]+)", output)

    # Take average if multiple flows
    throughput = sum(map(float, throughput)) / len(throughput)
    pdr = sum(map(float, pdr)) / len(pdr)
    delay = sum(map(float, delay)) / len(delay)

    return throughput, pdr, delay

# Run all protocols
for protocol in protocols:
    print(f"Running {protocol}...")
    output = run_simulation(protocol)
    t, p, d = extract_metrics(output)

    throughput_list.append(t)
    pdr_list.append(p)
    delay_list.append(d)

# -----------------------
# TABLE IMAGE (table.png)
# -----------------------
fig, ax = plt.subplots()
ax.axis('tight')
ax.axis('off')

table_data = []
for i in range(len(protocols)):
    table_data.append([
        protocols[i],
        f"{throughput_list[i]:.2f}",
        f"{pdr_list[i]:.2f}",
        f"{delay_list[i]:.5f}"
    ])

columns = ["Protocol", "Throughput (Kbps)", "PDR (%)", "Delay (sec)"]

table = ax.table(cellText=table_data, colLabels=columns, loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

plt.title("MANET Protocol Comparison Results")
plt.savefig("table.png")
plt.close()

print("Table generated: table.png")

# -----------------------
# LINE GRAPHS
# -----------------------

# Throughput
plt.figure()
plt.plot(protocols, throughput_list, marker='o', linestyle='-', color='blue')
plt.xlabel("Protocol")
plt.ylabel("Throughput (Kbps)")
plt.title("Protocol vs Throughput")
plt.grid(True)
plt.savefig("throughput.png")
plt.close()

# Delay
plt.figure()
plt.plot(protocols, delay_list, marker='s', linestyle='-', color='red')
plt.xlabel("Protocol")
plt.ylabel("Delay (sec)")
plt.title("Protocol vs Delay")
plt.grid(True)
plt.savefig("delay.png")
plt.close()

# PDR
plt.figure()
plt.plot(protocols, pdr_list, marker='^', linestyle='-', color='green')
plt.xlabel("Protocol")
plt.ylabel("PDR (%)")
plt.title("Protocol vs PDR")
plt.grid(True)
plt.savefig("pdr.png")
plt.close()

print("\nLine graphs generated: throughput.png, delay.png, pdr.png")
