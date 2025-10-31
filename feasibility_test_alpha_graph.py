import matplotlib.pyplot as plt
import numpy as np
import re
import os

def read_feasibility_data(filename):
    """
    Lê o arquivo de resultados e retorna um dicionário com dados por alpha.
    Aceita linhas no formato 'alpha 0.25' ou apenas '0.25'.
    """
    data = {}
    current_alpha = None

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            # Detecta nova seção de alpha
            if line.startswith("alpha") or re.fullmatch(r"^[0-9]*\.?[0-9]+$", line):
                # Extrai o valor numérico (pode vir com ou sem "alpha")
                alpha_value = float(line.split()[-1])
                current_alpha = alpha_value
                data[current_alpha] = {"util": [], "feas": []}
            
            # Linhas com dados de utilização e viabilidade
            elif line.startswith("Utilization:") and current_alpha is not None:
                match = re.match(r"Utilization:\s*([\d.]+),\s*Feasibility Ratio:\s*([\d.]+)%", line)
                if match:
                    utilization = float(match.group(1))
                    feasibility = float(match.group(2))
                    data[current_alpha]["util"].append(utilization)
                    data[current_alpha]["feas"].append(feasibility)

    return data


def plot_feasibility(data, output_path="fig/feasibility_vs_alpha.png"):
    """Gera o gráfico de viabilidade para cada valor de alpha."""
    plt.figure(figsize=(8, 5))

    for alpha, values in sorted(data.items()):
        util = np.array(values["util"])
        feas = np.array(values["feas"])

        # Ordena valores de utilização para manter consistência visual
        order = np.argsort(util)
        util, feas = util[order], feas[order]

        # Interpolação suave entre os pontos
        interp_util = np.linspace(util.min(), util.max(), 200)
        interp_feas = np.interp(interp_util, util, feas)

        # Linha interpolada e pontos originais
        plt.plot(interp_util, interp_feas, label=f"α = {alpha}")
        plt.scatter(util, feas, s=35, edgecolors='black', linewidths=0.6)

    plt.title("Relação entre Utilização e Viabilidade por Valor de α para DM")
    plt.xlabel("Utilização Total do Conjunto (U)")
    plt.ylabel("Razão de Viabilidade (%)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title="Valores de α")
    plt.tight_layout()

    # Cria pasta de saída se não existir
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.show()


if __name__ == "__main__":
    filename = "dm_output.txt"
    data = read_feasibility_data(filename)
    plot_feasibility(data)
