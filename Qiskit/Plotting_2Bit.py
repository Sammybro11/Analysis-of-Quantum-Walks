import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_quantum_walk_data(filepath):
    """Load quantum walk data from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data
def bitstring_to_position(bitstring):
    """Convert bitstring (e.g., '00', '10') to position index (0, 1, 2, 3)."""
    # Assuming 2 qubits: '00'->0, '01'->1, '10'->2, '11'->3
    if bitstring == '00':
        return 0
    elif bitstring == '01':
        return 1
    elif bitstring == '10':
        return 2
    elif bitstring == '11':
        return 3
    else:
        raise ValueError(f"Unknown bitstring: {bitstring}")

def calculate_fidelity_from_hellinger(hellinger_dist):
    """Convert Hellinger distance to fidelity.
    Fidelity = 1 - Hellinger^2 (for probability distributions)"""
    return (1.0 - hellinger_dist**2)**2

def create_quantum_walk_plots(data, output_filename: Path):
    """Create the 6-panel plot for quantum walk results."""
    
    # Extract results
    results = data['results']
    
    # Determine how many steps to plot (up to 5 panels: steps 0-4)
    max_steps_to_plot = min(5, len(results))
    
    # Create subplots: 3 rows, 2 columns
    fig, axes = plt.subplots(3, 2, figsize=(12, 10))
    fig.suptitle('DTQW for a 4-node graph', fontsize=14, fontweight='bold')
    
    # Colors for ideal (blue) and noisy (red)
    ideal_color = '#1f77b4'  # Blue
    noisy_color = '#d62728'  # Red
    
    # Panel (a) to (e): Bar plots for steps 0 to 4
    for i in range(max_steps_to_plot):
        ax = axes[i // 2, i % 2]
        
        step_data = results[i]
        step_num = step_data['steps']
        
        # Get counts for ideal and noisy
        ideal_counts = step_data['counts_ideal']
        noisy_counts = step_data['counts_noisy']
        
        # Convert to probabilities
        total_shots = sum(ideal_counts.values())
        ideal_probs = {pos: count / total_shots for pos, count in ideal_counts.items()}
        noisy_probs = {pos: count / total_shots for pos, count in noisy_counts.items()}
        
        # Create position arrays for plotting
        positions = [0, 1, 2, 3]
        ideal_vals = [ideal_probs.get(pos_str, 0) for pos_str in ['00', '01', '10', '11']]
        noisy_vals = [noisy_probs.get(pos_str, 0) for pos_str in ['00', '01', '10', '11']]
        
        # Plot bars
        bar_width = 0.35
        x = np.arange(len(positions))
        
        bars1 = ax.bar(x - bar_width/2, ideal_vals, bar_width, label='Ideal', color=ideal_color, edgecolor='black', linewidth=0.5)
        bars2 = ax.bar(x + bar_width/2, noisy_vals, bar_width, label='Noisy', color=noisy_color, edgecolor='black', linewidth=0.5)
        
        # Add value labels on top of bars
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.3f}', 
                   ha='center', va='bottom', fontsize=8, rotation=0, color='black')
        
        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.3f}', 
                   ha='center', va='bottom', fontsize=8, rotation=0, color='black', fontweight='bold')
        
        # Set titles and labels
        ax.set_xlabel('Position', fontsize=10)
        ax.set_ylabel('Probabilities', fontsize=10)
        ax.set_ylim(0, 1.05)
        ax.set_xticks(x)
        ax.set_xticklabels(['0', '1', '2', '3'])
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_axisbelow(True)
        
        # Add legend only to first subplot
        if i == 0:
            ax.legend(loc='upper right', fontsize=9)
    
    # Panel (f): Fidelity vs Steps
    ax_f = axes[2, 1]  # Bottom right panel
    
    steps = [result['steps'] for result in results]
    hellinger_distances = [result['Hellinger'] for result in results]
    fidelities = [calculate_fidelity_from_hellinger(h) for h in hellinger_distances]
    # Plot fidelity
    ax_f.plot(steps, fidelities, 'ro-', linewidth=2, markersize=8, markerfacecolor=noisy_color, markeredgecolor='black')
    ax_f.set_title('(f) Fidelity vs Steps', fontsize=12, fontweight='bold')
    ax_f.set_xlabel('Steps', fontsize=10)
    ax_f.set_ylabel('Fidelity', fontsize=10)
    ax_f.set_ylim(0, 1.05)
    ax_f.grid(True, linestyle='--', alpha=0.7)
    ax_f.set_axisbelow(True)
    
    # Remove the unused subplot (if any)
    if max_steps_to_plot < 5:
        axes[2, 0].set_visible(False)
    # Save figure
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved as {output_filename}")

# Main execution
if __name__ == "__main__":
    dir = Path("qw_results_2bit/")
    path = dir / "results.json"
    out = dir / "plots.png"
    data = load_quantum_walk_data(path)
    # Create plots
    create_quantum_walk_plots(data, out)
