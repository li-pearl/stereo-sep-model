import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import matplotlib.dates as mdates

def parse_stereo_data(filename):
    energy_channels = [
        (13.6, 15.1, 'H'),
        (14.9, 17.1, 'H'),
        (17.0, 19.3, 'H'),
        (20.8, 23.8, 'H'),
        (23.8, 26.4, 'H'),
        (26.3, 29.7, 'H'),
        (29.5, 33.4, 'H'),
        (33.4, 35.8, 'H'),
        (35.5, 40.5, 'H'),
        (40.0, 60.0, 'H'),
        (60.0, 100.0, 'H')
    ]
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    data_start = None
    for i, line in enumerate(lines):
        if line.strip() == "#End":
            data_start = i + 1
            break
    
     # just in case i filed in the data wrong or smth
    if data_start is None:
        raise ValueError("Could not find data start marker '#End'")
    
    times = []
    flux_data = []
    
    for line in lines[data_start:]:
        if line.strip():
            parts = line.split()
            if len(parts) >= 6:
                time_str = f"{parts[1]} {parts[2]} {parts[3]} {parts[4]}"
                time_obj = datetime.strptime(time_str, "%Y %b %d %H%M")
                times.append(time_obj)
                flux_values = [float(parts[i]) for i in range(9, min(len(parts), 9 + len(energy_channels)))]
                while len(flux_values) < len(energy_channels):
                    flux_values.append(0.0)
                flux_data.append(flux_values[:len(energy_channels)])
    
    return times, flux_data, energy_channels

def create_spectrograph(filename):
    times, flux_data, energy_channels = parse_stereo_data(filename)
    
    # just in case i filed in the data wrong or smth
    if not times:
        print("No valid data found!")
        return
    
    flux_array = np.array(flux_data)
    time_array = np.array(times)
    
    energy_labels = [f"{e_min:.1f}-{e_max:.1f} MeV" for e_min, e_max, particle in energy_channels]
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(energy_channels)))
    
    for i, (channel, color) in enumerate(zip(energy_channels, colors)):
        flux_channel = flux_array[:, i]
        flux_channel[flux_channel <= 0] = np.nan
        
        ax.plot(time_array, flux_channel, 
               color=color, label=energy_labels[i], 
               linewidth=1.5, alpha=0.8)
    
    ax.set_xlabel('Date (January 2025)', fontsize=12)
    ax.set_ylabel('Flux (particles/cm²/s/sr/MeV)', fontsize=12)
    ax.set_title('STEREO Hydrogen Proton Particle Flux - January 2025', fontsize=14, fontweight='bold')
    
    ax.set_yscale('log')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))  # Every 2 days
    ax.xaxis.set_minor_locator(mdates.DayLocator())  # Every day
    
    ax.set_xlim(min(time_array), max(time_array))
    
    plt.tight_layout()
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    plt.show()
    

    # In case the data was in wrong for debugging
    print(f"Data span: {times[0]} to {times[-1]}")
    print(f"Total time points: {len(times)}")
    print(f"Energy channels: {len(energy_channels)}")
    valid_flux = flux_array[flux_array > 0]
    if len(valid_flux) > 0:
        print(f"Flux range: {np.min(valid_flux):.2e} to {np.max(valid_flux):.2e}")

create_spectrograph("AeH25Jan.15m.txt")