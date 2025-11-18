import json
import matplotlib.pyplot as plt
import numpy as np

def bitstring_to_position(bitstring):
    """Convert 3-bit string like '001' to integer position (0 to 7)."""
    return int(bitstring, 2)

def create_8node_quantum_walk_plots(data, output_filename="8node_quantum_walk.png"):
    """
    Create a 2x4 subplot figure:
    - Panels (a) through (g): Steps 1 to 7 (bar plots)
    - Panel (h): Fidelity vs Steps (line plot)
    """
    results = data['results']
    
    # We'll plot steps 1 through 6 (at minimum), but include all available
    steps_to_plot = [1, 2, 3, 4, 5, 6, 7, 8]
    available_steps = {r['steps']: r for r in results}
    
    # Determine which of the desired steps are present
    plot_steps = [s for s in steps_to_plot if s in available_steps]
    n_panels = len(plot_steps) + 1  # +1 for fidelity plot

    # Use 2x4 grid (8 panels max)
    fig, axes = plt.subplots(4, 2, figsize=(12, 16))
    fig.suptitle('Discrete-Time Quantum Walk on 8-Node Cycle', fontsize=14, fontweight='bold')
    
    ideal_color = '#1f77b4'  # Blue
    noisy_color = '#d62728'  # Red

    # Panel (a) to (g): Bar plots for each step
    for idx, step in enumerate(plot_steps[:7]):  # Max 7 bar plots
        ax = axes[idx // 2, idx % 2]
        result = available_steps[step]
        
        ideal_counts = result['counts_ideal']
        noisy_counts = result['counts_noisy']
        
        total_shots = sum(ideal_counts.values())
        ideal_probs = {pos: count / total_shots for pos, count in ideal_counts.items()}
        noisy_probs = {pos: count / total_shots for pos, count in noisy_counts.items()}
        
        # All 8 positions
        positions = list(range(8))
        position_labels = [f'{i}' for i in positions]
        ideal_vals = [ideal_probs.get(f'{i:03b}', 0) for i in positions]
        noisy_vals = [noisy_probs.get(f'{i:03b}', 0) for i in positions]
        
        x = np.arange(8)
        bar_width = 0.35
        
        ax.bar(x - bar_width/2, ideal_vals, bar_width, label='Ideal', 
               color=ideal_color, edgecolor='black', linewidth=0.5)
        ax.bar(x + bar_width/2, noisy_vals, bar_width, label='Noisy', 
               color=noisy_color, edgecolor='black', linewidth=0.5)
        
        # Optional: annotate small values (only if prob > 0.01 to avoid clutter)
        for i, (ideal_v, noisy_v) in enumerate(zip(ideal_vals, noisy_vals)):
            if ideal_v > 0.01:
                ax.text(i - bar_width/2, ideal_v + 0.01, f'{ideal_v:.2f}', 
                        ha='center', va='bottom', fontsize=6, rotation=90)
            if noisy_v > 0.01:
                ax.text(i + bar_width/2, noisy_v + 0.01, f'{noisy_v:.2f}', 
                        ha='center', va='bottom', fontsize=6, rotation=90, color='white', fontweight='bold')
        
        ax.set_xlabel('Position')
        ax.set_ylabel('Probability')
        ax.set_xticks(x)
        ax.set_xticklabels(position_labels)
        ax.set_ylim(0, 1.05)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_axisbelow(True)
        
        if idx == 0:
            ax.legend(loc='upper right', fontsize=9)

    # Panel (h): Fidelity vs Steps
    ax_f = axes[3, 1]  # Bottom-right panel
    all_steps = sorted(available_steps.keys())
    hellinger_vals = [available_steps[s]['Hellinger'] for s in all_steps]
    fidelity_vals = [(1.0 - h**2)**2 for h in hellinger_vals]  # Fidelity = 1 - H²

    ax_f.plot(all_steps, fidelity_vals, 'ro-', linewidth=2, markersize=7,
              color=noisy_color, markeredgecolor='black')
    
    ax_f.set_xlabel('Steps')
    ax_f.set_ylabel('Fidelity')
    ax_f.set_ylim(0, 1.05)
    ax_f.set_xticks(all_steps)
    ax_f.grid(True, linestyle='--', alpha=0.6)
    ax_f.set_axisbelow(True)

    # Hide any unused subplot (shouldn't be needed here since we have 8 panels)
    for idx in range(len(plot_steps), 7):
        axes[idx // 2, idx % 2].set_visible(False)
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved as '{output_filename}'")

# ----------------------------
# Main: Load data and plot
# ----------------------------
if __name__ == "__main__":
    with open('qw_results_3bit/results.json', 'r') as f:
        data = json.load(f)

    create_8node_quantum_walk_plots(data, "qw_results_3bit/plots.png")
