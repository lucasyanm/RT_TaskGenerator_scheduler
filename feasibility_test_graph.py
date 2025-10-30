import re
import matplotlib
matplotlib.use("TkAgg")  # garante que o gráfico abra no Windows
import matplotlib.pyplot as plt

# Caminho do arquivo de entrada
input_file = "output.txt"

# Dicionário para armazenar os dados
data = {}
current_method = None

# Expressões regulares para capturar os dados
header_pattern = re.compile(r"-- (.*?) --")
data_pattern = re.compile(r"Utilization:\s*([\d.]+),\s*Feasibility Ratio:\s*([\d.]+)%")

# Leitura do arquivo
with open(input_file, "r", encoding="utf-16") as f:
    for line in f:
        header_match = header_pattern.match(line)
        if header_match:
            current_method = header_match.group(1)
            data[current_method] = {"util": [], "feas": []}
            continue
        data_match = data_pattern.match(line)
        if data_match and current_method:
            utilization = float(data_match.group(1))
            feasibility = float(data_match.group(2))
            data[current_method]["util"].append(utilization)
            data[current_method]["feas"].append(feasibility)

# Cores e marcadores para cada método
colors = {"Rate Monotonic (RM)": "red",
          "Deadline Monotonic (DM)": "blue",
          "Earliest Deadline First (EDF)": "green"}

markers = {"Rate Monotonic (RM)": "o",
           "Deadline Monotonic (DM)": "s",
           "Earliest Deadline First (EDF)": "^"}

# Gráfico único comparativo
plt.figure(figsize=(8,6))
for method, values in data.items():
    plt.plot(values["util"], values["feas"], marker=markers[method], color=colors[method],
             linestyle="-", linewidth=2, label=method)

plt.xlabel("Utilization")
plt.ylabel("Feasibility Ratio (%)")
plt.title("Feasibility Ratio vs Utilization")
plt.grid(True)
plt.ylim(0, 110)
plt.xlim(0.6, 1.05)
plt.legend()
plt.tight_layout()

# Salvando o gráfico em um arquivo
plt.savefig("fig/feasibility_comparison.png")
print("Gráfico salvo em 'fig/feasibility_comparison.png'")

plt.show()

