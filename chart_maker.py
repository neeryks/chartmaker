
import subprocess
import time


def generate_config(ra,dec,filename,map_type,size,output_location,font_size):

    default_params = f"""
angular_width={100.0 if size == 21 else 90}
mag_min=7
width={size}
aspect=1
constellation_sticks=1
constellation_names =1
coords=ra_dec
projection={map_type}
star_names=0
star_flamsteed_labels=0
constellation_names=1
plot_galaxy_map=0
plot_equator=0
plot_ecliptic=1
plot_galactic_plane=0
constellation_boundaries=0
dso_names=0
dso_mags=0
plot_dso=0
font_size = {font_size}
ra_dec_lines=0
star_col = 1.0,1.0,1.0
constellation_stick_col = 1.0,1.0,1.0
constellation_label_col = 1.0,1.0,1.0
ecliptic_col = 1.0,1.0,1.0
    """

    try:
        with open(f"{output_location}/{filename}.sch", 'w') as sch_file:
            # Write DEFAULTS section
            sch_file.write("DEFAULTS\n")
            sch_file.write(f"ra_central={ra}\n")
            sch_file.write(f"dec_central={dec}\n")
            sch_file.write(f"{default_params}\n")
            sch_file.write(f"""
CHART
output_filename=charts/{filename}.png

                                    """)
        subprocess.Popen(f"./star-charter/bin/starchart.bin schfiles/{filename}.sch", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        time.sleep(1)
    except Exception as e:
        print(f"Error creating star chart configuration file '{filename}': {e}")
        return False

