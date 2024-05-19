import numpy as np
import random

def update_population_densities(mice_birth_rate, mice_death_rate, mice_diffusion_rate, foxes_birth_rate, 
                                foxes_death_rate, foxes_diffusion_rate, time_step_size, width, height, 
                                landscape, neighbouring_land_count, initial_mice_densities, new_mice_densities, 
                                initial_foxes_densities, new_foxes_densities):
    
    """
    Update population densities for mice and foxes in land squares of the landscape.

    Args:
        mice_birth_rate (float): The birth rate of mice.
        mice_death_rate (float): The death rate of mice.
        mice_diffusion_rate (float): The diffusion rate of mice.
        foxes_birth_rate (float): The birth rate of foxes.
        foxes_death_rate (float): The death rate of foxes.
        foxes_diffusion_rate (float): The diffusion rate of foxes.
        time_step_size (float): The time step size.
        width (int): The width of the landscape.
        height (int): The height of the landscape.
        landscape (numpy.ndarray): A 2D array representing the landscape.
        neighbouring_land_count (numpy.ndarray): A 2D array representing land neighbors count for each land square.
        initial_mice_densities (numpy.ndarray): A 2D array representing initial mice densities.
        new_mice_densities (numpy.ndarray): A 2D array representing new mice population densities.
        initial_foxes_densities (numpy.ndarray): A 2D array representing initial foxes densities.
        new_foxes_densities (numpy.ndarray): A 2D array representing new foxes population densities.
    
    Return: 
        None
    """
    
    for x in range(1,height+1):
        for y in range(1,width+1):
               # Check if the current cell at (x, y) is a land square in the landscape
            if landscape[x,y]: 
                # Update density for mice and foxes            
                new_mice_densities[x,y] = update_population_density(mice_birth_rate, mice_death_rate, mice_diffusion_rate, 
                                                                             time_step_size, neighbouring_land_count, initial_mice_densities, 
                                                                             initial_foxes_densities, x, y, 'mice')
                new_foxes_densities[x,y] = update_population_density(foxes_birth_rate, foxes_death_rate, foxes_diffusion_rate, 
                                                                               time_step_size, neighbouring_land_count, initial_mice_densities, 
                                                                               initial_foxes_densities, x, y, 'foxes')
        
def calculate_density_colors(height, width, landscape, initial_mice_densities, maximum_mice_density, initial_foxes_densities, maximum_foxes_density, mice_density_colours, foxes_density_colours):
    """
    Calculate density colors for mice and foxes and update the respective arrays.

    Args:
        height (int): The height of the landscape.
        width (int): The width of the landscape.
        landscape (numpy.ndarray): A 2D array representing the landscape.
        initial_mice_densities (numpy.ndarray): A 2D array representing the initial population density values for mice.
        maximum_mice_density (float): The maximum density of mice.
        initial_foxes_densities (numpy.ndarray): A 2D array representing the initial population density values for foxes.
        maximum_foxes_density (float): The maximum density of foxes.
        mice_density_colours (numpy.ndarray): A 2D array for storing mice density colors.
        foxes_density_colours (numpy.ndarray): A 2D array for storing foxes density colors.

    Returns:
        None
    """
    for x in range(1, height + 1):
        for y in range(1, width + 1):
            if landscape[x, y]:
                mice_density_colours[x - 1, y - 1] = calculate_colour_value(initial_mice_densities[x, y], maximum_mice_density)
                foxes_density_colours[x - 1, y - 1] = calculate_colour_value(initial_foxes_densities[x, y], maximum_foxes_density)
        
def calculate_density_statistics(initial_mice_densities, initial_foxes_densities, num_lands):
    """
    Calculate maximum and average densities for mice and foxes.

    Args:
        initial_mice_densities (numpy.ndarray): A 2D array representing the initial population density values for mice.
        initial_foxes_densities (numpy.ndarray): A 2D array representing the initial population density values for foxes.
        num_lands (int): The number of land squares in the landscape.

    Returns:
        tuple: A tuple containing the following elements:
            maximum_mice_density (float): The maximum density of mice.
            maximum_foxes_density (float): The maximum density of foxes.
            average_mice_density (float): The average density of mice.
            average_foxes_density (float): The average density of foxes.
    """
    maximum_mice_density = np.max(initial_mice_densities)
    maximum_foxes_density = np.max(initial_foxes_densities)
    average_mice_density = calculate_average_density(num_lands, initial_mice_densities)
    average_foxes_density = calculate_average_density(num_lands, initial_foxes_densities)
    
    return maximum_mice_density, maximum_foxes_density, average_mice_density, average_foxes_density

def initialize_arrays(seed, width, height, landscape):
    """
    Initialize variables related to population densities and density colors.

    Args:
        seed (float): The random seed used for density initialization.
        width (int): The width of the simulation landscape.
        height (int): The height of the simulation landscape.
        landscape (numpy.ndarray): The landscape array.

    Returns:
        tuple: A tuple containing the following elements:
            initial_densities (numpy.ndarray): A 2D array representing the initial population density values.
            new_densities (numpy.ndarray): A 2D array representing the new population density values.
            density_colors (numpy.ndarray): A 2D array representing  the density color values for PPM file maps.
    """
    # Initialize the population densities
    initial_densities = initialize_population_densities(seed, width, height, landscape)

    # Initialize arrays to store new population density values
    new_densities = initial_densities.copy()

    # Initialize arrays for storing density color values for PPM file maps
    density_colors = np.zeros((height, width), int)

    return initial_densities, new_densities, density_colors

def update_population_density(birth_rate, death_rate, diffusion_rate, time_step_size, land_neighbours, initial_mice_densities, initial_foxes_densities, x, y, animal):
    """
    Update the population density of either mice or foxes based on the given parameters.

    Args:
        birth_rate (float): The birth rate of the specified animal.
        death_rate (float): The death rate of the specified animal.
        diffusion_rate (float): The diffusion rate for migration.
        time_step_size (float): The size of the time step.
        land_neighbours (numpy.ndarray): A 2D array representing the count of neighboring squares for each land square.
        initial_mice_densities (numpy.ndarray): A 2D array representing initial mice densities.
        initial_foxes_densities (numpy.ndarray): A 2D array representing initial foxes densities.
        x (int): The x-coordinate of the cell.
        y (int): The y-coordinate of the cell.
        animal (str): 'mice' or 'foxes' to specify the animal for which to update the density.

    Returns:
        float: The updated population density of the specified animal.
    """
    current_mice_density = initial_mice_densities[x, y]
    current_foxes_density = initial_foxes_densities[x, y]
    
    if animal == 'foxes':
        birth_term = birth_rate * current_mice_density *  current_foxes_density
        death_term = death_rate * current_foxes_density
        migration_term = calculate_migration_change(diffusion_rate, land_neighbours, initial_foxes_densities, x, y)
        new_density =  current_foxes_density + time_step_size * ((birth_term - death_term) + migration_term)
    
    else:
        birth_term = birth_rate * current_mice_density
        death_term = death_rate * current_mice_density *  current_foxes_density
        migration_term = calculate_migration_change(diffusion_rate, land_neighbours, initial_mice_densities, x, y)
        new_density =  current_mice_density + time_step_size * ((birth_term - death_term) + migration_term)
        
    return max(0, new_density)
                                
def calculate_migration_change(diffusion_rate, land_neighbours, initial_densities, x, y):
    """
    Calculate the change in density due to migration in and out of neighbouring land squares

    Args:
        diffusion_rate (float): The diffusion rate for migration.
        land_neighbours (numpy.ndarray): A 2D array representing the count of neighboring squares for each land square.
        initial_densities (numpy.ndarray): A 2D array representing initial animal densities.
        x (int): The x-coordinate of the cell.
        y (int): The y-coordinate of the cell.

    Returns:
        float: The migration change for the land square
    """
    neighbouring_density_count = calculate_total_neighbours(x, y, initial_densities)
    return diffusion_rate * ((neighbouring_density_count) - (land_neighbours[x,y] * initial_densities[x, y]))

def save_ppm_file(width, height, landscape, foxes_density_colours, mice_density_colours, time_step_index):
    """
    Save a PPM image file based on the densities of foxes and mice on the landscape.

    Args:
        time_step_index (int): The current time step index.
        width (int): The width of the landscape.
        height (int): The height of the landscape.
        landscape (numpy.ndarray): A 2D array representing the landscape.
        foxes_density_colours (numpy.ndarray): A 2D array of foxes density colors.
        mice_density_colours (numpy.ndarray): A 2D array of mice density colors.

    Returns:
        None
    """
    with open("map_{:04d}.ppm".format(time_step_index),"w") as f:
        header="P3\n{} {}\n{}\n".format(width,height,255)
        f.write(header)
        for x in range(0,height):
            for y in range(0,width):
                if landscape[x+1,y+1]:
                    f.write("{} {} {}\n".format(foxes_density_colours[x,y], mice_density_colours[x,y],0))
                else:
                    f.write("{} {} {}\n".format(0,200,255))

def calculate_colour_value(current_density, maximum_density):
    """
    Calculate the color value based on densities and maximum_density.

    Args:
        current_density (float): The current density value.
        maximum_density (float): The maximum density value.

    Returns:
        float: The calculated color value in the range [0, 255].
        
    - Note: 255 is the maximum colour value and 0 is the minimum
    """
    if maximum_density != 0:
        return (current_density / maximum_density) * 255
    else:
        return 0
    
def calculate_average_density(num_lands, densities):
    """
    Calculate the average population density.

    Args:
        num_lands (int): The number of land squares in the landscape.
        densities (numpy.ndarray): An array of initial population densities.

    Returns:
        float: The average population density if `num_lands` is not 0, or 0 otherwise.
    """
    if num_lands != 0:
        return np.sum(densities) / num_lands
    else:
        return 0
  
def initialize_population_densities(seed, width, height, landscape):
    """
    Initialize population density grid for field mice or foxes.

    Args:
        seed (int): The random seed used for density initialization.
        width (int): The width of the landscape
        height (int): The height of the landscape
        landscape (numpy.ndarray): A 2D array representing the landscape, where land
            squares are marked with values indicating land (1) or non-land (0).

    Returns:
        numpy.ndarray: A 2D array containing the initialized population densities.

    Notes:
        - The 'seed' parameter allows for reproducible random density initialization.
        - If 'seed' is 0, all density values are set to 0 (no population).
        - For non-zero 'seed' values, population densities are generated for land squares
          using a random uniform distribution between 0 and 5.0.
    """
    density_grid = landscape.astype(float).copy()
    random.seed(seed)
    for x in range(1, height + 1):
        for y in range(1, width + 1):
            if seed == 0:
                density_grid[x,y] = 0
            else:
                if landscape[x,y]:
                    density_grid[x,y] = random.uniform(0,5.0)
                else:
                    density_grid[x,y] = 0
    return density_grid
        
def calculate_land_neighbours(width, height, width_with_halo, height_with_halo, landscape):       
    """
    Calculate the number of land neighbours for each land square in the landscape.

    Args:
        width (int): The width of the landscape
        height (int): The height of the landscape 
        width_with_halo (int): The width of the landscape including halo cells.
        height_with_halo (int): The height of the landscape including halo cells.
        landscape (numpy.ndarray): A 2D array representing the landscape, where
            land squares are marked with values indicating land (1) or non-land (0).

    Returns:
        numpy.ndarray: A 2D array containing the number of land neighbours for each
        land square in the landscape.
    """
    neighbours = np.zeros((height_with_halo, width_with_halo), int)
    for x in range(1, height + 1):
        for y in range(1, width + 1):
            neighbours[x, y] = calculate_total_neighbours(x , y, landscape)

    return neighbours

def calculate_total_neighbours(x, y, grid):
    """
    Calculate the sum of values in neighbouring cells for a specific cell in the grid.

    Args:
        x (int): The x-coordinate of the cell.
        y (int): The y-coordinate of the cell.
        grid (numpy.ndarray): A 2D array representing the grid.

    Returns:
        float: The sum of values in neighboring cells for the cell.
    
    Note:
        - Neighbours are counted in the cardinal directions (north, south, east, west).
    """
    height, width = grid.shape
    total_neighbours = 0

    # Check and add north neighbor if it exists and has a valid index
    if x - 1 >= 0:
        total_neighbours += grid[x - 1, y]

    # Check and add south neighbor if it exists and has a valid index
    if x + 1 < height:
        total_neighbours += grid[x + 1, y]

    # Check and add west neighbor if it exists and has a valid index
    if y - 1 >= 0:
        total_neighbours += grid[x, y - 1]

    # Check and add east neighbor if it exists and has a valid index
    if y + 1 < width:
        total_neighbours += grid[x, y + 1]

    return total_neighbours

def read_landscape_file(landscape_file):
    """Read and process a landscape file.

    Args:
        landscape_file (str): The path to the input landscape file.

    Returns:
        tuple: A tuple containing the following elements:
            int: The width of the landscape.
            int: The height of the landscape.
            int: The width of the landscape including halo.
            int: The height of the landscape including halo.
            numpy.ndarray: A 2D array representing the processed landscape.
    """
    with open(landscape_file, "r") as f:
        width, height = [int(i) for i in f.readline().split(" ")]
        print("Width: {} Height: {}".format(width, height))
        width_with_halo = width + 2  # Width including halo or border
        height_with_halo = height + 2  # Height including halo or border
        landscape = np.zeros((height_with_halo, width_with_halo), int)
        print(landscape)
        row = 1
        for line in f.readlines():
            values = line.split(" ")
            # Read landscape into an array, padding with halo values.
            landscape[row] = [0] + [int(i) for i in values] + [0]
            row += 1
    return width, height, width_with_halo, height_with_halo, landscape