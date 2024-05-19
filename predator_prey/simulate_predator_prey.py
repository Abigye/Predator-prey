'''Predator-prey simulation. Foxes and mice.

Version 3.0
'''
from argparse import ArgumentParser
import numpy as np
from predator_prey.validate_arguments import *
from predator_prey.helper_functions import *

def getVersion():
    return 3.0

def simCommLineIntf():
    par=ArgumentParser()
    par.add_argument("-r","--birth-mice",type=float,default=0.1,help="Birth rate of mice")
    par.add_argument("-a","--death-mice",type=float,default=0.05,help="Rate at which foxes eat mice")
    par.add_argument("-k","--diffusion-mice",type=float,default=0.2,help="Diffusion rate of mice")
    par.add_argument("-b","--birth-foxes",type=float,default=0.03,help="Birth rate of foxes")
    par.add_argument("-m","--death-foxes",type=float,default=0.09,help="Rate at which foxes starve")
    par.add_argument("-l","--diffusion-foxes",type=float,default=0.2,help="Diffusion rate of foxes")
    par.add_argument("-dt","--delta-t",type=float,default=0.5,help="Time step size")
    par.add_argument("-t","--time_step",type=int,default=10,help="Number of time steps at which to output files")
    par.add_argument("-d","--duration",type=int,default=500,help="Time to run the simulation (in timesteps)")
    par.add_argument("-f","--landscape-file",type=str,required=True,
                        help="Input landscape file")
    par.add_argument("-ms","--mouse-seed",type=int,default=1,help="Random seed for initialising mouse densities")
    par.add_argument("-fs","--fox-seed",type=int,default=1,help="Random seed for initialising fox densities")
    args=par.parse_args()
    
    validate_arguments(args) # validates all arguments aside from the landscape file
    validate_input_file_argument(args.landscape_file)
    
    run_simulation(args.birth_mice, args.death_mice, args.diffusion_mice, args.birth_foxes, 
        args.death_foxes, args.diffusion_foxes, args.delta_t, args.time_step, 
        args.duration, args.landscape_file, args.mouse_seed, args.fox_seed)

def run_simulation(mice_birth_rate, mice_death_rate, mice_diffusion_rate, foxes_birth_rate, 
        foxes_death_rate, foxes_diffusion_rate, time_step_size, output_time_step, 
        simulation_duration, landscape_file, mouse_seed, fox_seed):
    """
    Run a predator-prey simulation with the given parameters.

    Args:
        mice_birth_rate (float): Birth rate of mice.
        mice_death_rate (float): Death rate of mice.
        mice_diffusion_rate (float): Diffusion rate of mice.
        foxes_birth_rate (float): Birth rate of foxes.
        foxes_death_rate (float): Death rate of foxes.
        foxes_diffusion_rate (float): Diffusion rate of foxes.
        time_step_size (float): Size of the time step.
        output_time_step (int): Time step at which to output simulation results.
        simulation_duration (int): Duration of the simulation.
        landscape_file (str): Path to the landscape input file.
        mouse_seed (int): Random seed for initializing mouse densities.
        fox_seed (int): Random seed for initializing fox densities.

    Returns:
        None
    """
    
    print("Predator-prey simulation",getVersion())
    
    # Read landscape file and get dimensions
    width, height, width_with_halo, height_with_halo, landscape = read_landscape_file(landscape_file)
    
    # Calculate the number of land-only squares
    num_lands=np.count_nonzero(landscape)
    print("Number of land-only squares: {}".format(num_lands))
    
    # Pre-calculate number of land neighbours of each land square.
    neighbouring_land_count = calculate_land_neighbours(width, height, width_with_halo, height_with_halo, landscape)
    
    # Initializing the population densities, new densities, and density colors for mice and foxes
    initial_mice_densities, new_mice_densities, mice_density_colours = initialize_arrays(mouse_seed, width, height, landscape)
    initial_foxes_densities, new_foxes_densities, foxes_density_colours = initialize_arrays(fox_seed, width, height, landscape)
    
    # Calculate the average density for mice and foxes
    average_mice_density = calculate_average_density(num_lands, initial_mice_densities)
    average_foxes_density = calculate_average_density(num_lands, initial_foxes_densities)
    
    print("Averages. Timestep: {} Time (s): {:.1f} Mice: {:.17f} Foxes: {:.17f}".format(0,0,average_mice_density,average_foxes_density))

    with open("averages.csv","w") as f:
        header="Timestep,Time,Mice,Foxes\n"
        f.write(header)
    
    # Calculate the total number of time steps based on the simulation duration and time step size.  
    total_time_steps = int(simulation_duration / time_step_size)
    
    # Loop over time steps
    for time_step_index in range(0,total_time_steps):
        # Check if the current time step index is a multiple of the output time step
        # to control the timing of file output, such as averages and maps.  
        if not time_step_index % output_time_step:
            
            # Calculate maximum and average densities for mice and foxes 
            maximum_mice_density, maximum_foxes_density, average_mice_density, average_foxes_density = \
            calculate_density_statistics(initial_mice_densities, initial_foxes_densities, num_lands)
            
            # Calculate time in seconds
            time_in_secs = time_step_index*time_step_size
            
            # Print and save average densities to a CSV file
            print("Averages. Timestep: {} Time (s): {:.1f} Mice: {:.17f} Foxes: {:.17f}".format(time_step_index,
                                                                                                time_in_secs,
                                                                                                average_mice_density,
                                                                                                average_foxes_density))
            with open("averages.csv","a") as f:
                f.write("{},{:.1f},{:.17f},{:.17f}\n".format(time_step_index,
                                                             time_in_secs,
                                                             average_mice_density,
                                                             average_foxes_density))
            
            # Update the color representations of mice and foxes densities in mice_density_colours and 
            # foxes_density_colours variables on the landscape
            calculate_density_colors(height, width, landscape, initial_mice_densities, maximum_mice_density, 
                                     initial_foxes_densities, maximum_foxes_density, mice_density_colours, 
                                     foxes_density_colours)

            # Save the population density colours as a PPM file
            save_ppm_file(width, height, landscape, foxes_density_colours, mice_density_colours, time_step_index)
        
        # updates its population densities
        update_population_densities(mice_birth_rate, mice_death_rate, mice_diffusion_rate, foxes_birth_rate, foxes_death_rate, 
                                    foxes_diffusion_rate, time_step_size, width, height, landscape, neighbouring_land_count, 
                                    initial_mice_densities, new_mice_densities, initial_foxes_densities, new_foxes_densities)
 
                        
        # Swap initial and new population densities for next iteration.
        initial_mice_densities, new_mice_densities = new_mice_densities, initial_mice_densities
        initial_foxes_densities, new_foxes_densities = new_foxes_densities, initial_foxes_densities

    
if __name__ == "__main__":
    simCommLineIntf()
