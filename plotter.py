import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

def plot_bmi_history(records):
    if not records:
        print("No BMI records to plot.")
        return

    # Parse records
    dates = [datetime.datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S") for r in records]
    bmis = [r[1] for r in records]

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 5))

    # Set background color
    fig.patch.set_facecolor('#fdf6e3')  # Figure background
    ax.set_facecolor('#fdf6e3')         # Plot area background

    # Plot BMI data
    ax.plot(dates, bmis, marker='o', color='#005f73', linewidth=2, label='BMI')

    # Labels and title
    ax.set_title("BMI Trend Over Time", fontsize=14, fontweight='bold', color='#333')
    ax.set_xlabel("Date", fontsize=12, color='#333')
    ax.set_ylabel("BMI", fontsize=12, color='#333')

    # Grid and formatting
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(colors='#444')  # Axis ticks

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    # Add data labels
    for i, bmi in enumerate(bmis):
        ax.text(dates[i], bmis[i] + 0.3, f"{bmi:.1f}", ha='center', fontsize=9, color='black')

    # Legend
    ax.legend()

    # Layout
    plt.tight_layout()
    plt.show()
