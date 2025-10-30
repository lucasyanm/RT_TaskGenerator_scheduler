import math
import sys
sys.stdout.reconfigure(encoding='utf-16')

# ---------------------------
# Rate Monotonic (RM)
# ---------------------------
def test_rm(tasks, num_utilization):
    """
    Liu & Layland's (1973) sufficient test for RM scalability.
    Assumes implicit deadlines: D_i = T_i
    """
    n = len(tasks)
    limit = n * (2 ** (1 / n) - 1)
    # TODO: Add toggle for detailed output
    # Detailed output
    # print(f"[RM] Total utilization = {num_utilization:.4f}, Limit = {limit:.4f}")
    return num_utilization <= limit


# ---------------------------
# Deadline Monotonic (DM)
# ---------------------------
def test_dm(tasks):
    """
    Accurate feasibility test via Response Time Analysis (RTA)
    According to Lehoczky (1990) and Audsley et al. (1991)
    """
    # Ascending order by deadline (smaller D -> higher priority)
    tasks = sorted(tasks, key=lambda t: t["D"])
    
    for i, tarefa in enumerate(tasks):
        C_i, T_i, D_i = tarefa["C"], tarefa["T"], tarefa["D"]
        R_i = C_i
        while True:
            R_prev = R_i
            interferencia = sum(
                math.ceil(R_i / tasks[j]["T"]) * tasks[j]["C"]
                for j in range(i)
            )
            R_i = C_i + interferencia
            if R_i == R_prev:
                break
            if R_i > D_i:
                # TODO: Add toggle for detailed output
                # Detailed output
                # print(f"[DM] Task {i+1} failed: R_i={R_i:.4f} > D_i={D_i}")
                return False
        # TODO: Add toggle for detailed output
        # Detailed output
        # print(f"[DM] Task {i+1}: R_i={R_i:.4f}, D_i={D_i}")
        if R_i > D_i:
            return False
    return True


# ---------------------------
# Earliest Deadline First (EDF)
# ---------------------------
def test_edf(num_utilization):
    """
    Liu & Layland's (1973) necessary and sufficient test for EDF.
    """
    # TODO: Add toggle for detailed output
    # Detailed output
    # print(f"[EDF] Total utilization = {num_utilization:.4f}")
    return num_utilization <= 1.0


def load_tasks_from_file(filename):
    """
    Reads a file structured as:
    <total task set> <total tasks per set> <utilization>
    Task Set : <task set number>
    <C> <T>
    ...
    """
    scenarios = []

    with open(filename, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.strip()]  # ignore empty lines

    i = 0
    while i < len(lines):
        # Scenario header
        partes = lines[i].split()
        if len(partes) != 3:
            raise ValueError(f"Format error on line {i+1}: {lines[i]}")
        total_task_sets = int(partes[0])
        tasks_per_set = int(partes[1])
        utilization = float(partes[2])
        i += 1

        scenario = {
            "utilization": utilization,
            "total_task_sets": total_task_sets,
            "tasks_per_set": tasks_per_set,
            "task_sets": []
        }

        # Read each task set
        for _ in range(total_task_sets):
            if not lines[i].startswith("Task Set"):
                raise ValueError(f"Expected 'Task Set' on line {i+1}, found: {lines[i]}")
            i += 1

            tasks = []
            for _ in range(tasks_per_set):
                if i >= len(lines):
                    raise ValueError("End of file. Success.")
                c, t = map(float, lines[i].split())
                tasks.append({"C": c, "T": t, "D": t})  # implicit deadline
                i += 1

            scenario["task_sets"].append(tasks)

        scenarios.append(scenario)

    return scenarios

# --------------------------------
# Main program
# --------------------------------
if __name__ == "__main__":
    filename = "task_list.txt"
    scenarios = load_tasks_from_file(filename)

    rm_feasible_percentage_per_scenario = []
    dm_feasible_percentage_per_scenario = []
    edf_feasible_percentage_per_scenario = []

    for b_idx, scenario in enumerate(scenarios, 1):
        # TODO: Add toggle for detailed output
        # Detailed output
        # print(f"\n=== Scenario {b_idx} | Utilization = {scenario['utilization']} ===")

        rm_feasible_count = 0
        dm_feasible_count = 0
        edf_feasible_count = 0

        for ts_idx, tasks in enumerate(scenario["task_sets"], 1):
            rm_feasible = test_rm(tasks, scenario['utilization'])
            dm_feasible = test_dm(tasks)
            edf_feasible = test_edf(scenario['utilization'])

            if rm_feasible:
                rm_feasible_count += 1
            if dm_feasible:
                dm_feasible_count += 1
            if edf_feasible:
                edf_feasible_count += 1
            
            # TODO: Add toggle for detailed output
            # Detailed output
            # print(f"\n=== Task Set {ts_idx} ===")
            # print(f"Tasks: {tasks}")
            # print("RM:", "✅ Viable" if rm_feasible else "❌ Not Viable")
            # print("DM:", "✅ Viable" if dm_feasible else "❌ Not Viable")
            # print("EDF:", "✅ Viable" if edf_feasible else "❌ Not Viable")

        # Statistic output
        rm_feasible_percentage_per_scenario.append(
            {"utilization": scenario["utilization"],
             "feasibility_ratio": rm_feasible_count / scenario["total_task_sets"]})
        dm_feasible_percentage_per_scenario.append(
            {"utilization": scenario["utilization"],
            "feasibility_ratio": dm_feasible_count / scenario["total_task_sets"]})
        edf_feasible_percentage_per_scenario.append(
            {"utilization": scenario["utilization"],
            "feasibility_ratio": edf_feasible_count / scenario["total_task_sets"]})
    
    # print("\n=== Summary of Feasibility Percentages ===\n")

    print("-- Rate Monotonic (RM) --")
    for result in rm_feasible_percentage_per_scenario:
        print(f"Utilization: {result['utilization']}, Feasibility Ratio: {result['feasibility_ratio']:.2%}")
    
    print("\n-- Deadline Monotonic (DM) --")
    for result in dm_feasible_percentage_per_scenario:
        print(f"Utilization: {result['utilization']}, Feasibility Ratio: {result['feasibility_ratio']:.2%}")
    
    print("\n-- Earliest Deadline First (EDF) --")
    for result in edf_feasible_percentage_per_scenario:
        print(f"Utilization: {result['utilization']}, Feasibility Ratio: {result['feasibility_ratio']:.2%}")



