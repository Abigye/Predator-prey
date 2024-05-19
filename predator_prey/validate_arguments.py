
def validate_arguments(args):
    """
    Validate the arguments used for the predator-prey simulation.

    Args:
        args (argparse.Namespace): A namespace containing the input arguments for the simulation.

    Raises:
        ValueError: If any of the input arguments is not a positive float or integer or non negative integer.
    """
    if args.birth_mice <= 0.0:
        raise ValueError("Birth rate of mice must be a positive float greater than 0")
    if args.death_mice <= 0.0:
        raise ValueError("Death rate of mice must be a positive float greater than 0")
    if args.diffusion_mice <= 0.0:
        raise ValueError("Diffusion rate of mice must be a positive float greater than 0")
    if args.birth_foxes <= 0.0:
        raise ValueError("Birth rate of foxes must be a positive float greater than 0")
    if args.death_foxes <= 0.0:
        raise ValueError("Death rate of foxes must be a positive float greater than 0")
    if args.diffusion_foxes <= 0.0:
        raise ValueError("Diffusion rate of foxes must be a positive float greater than 0")
    if args.delta_t <= 0:
        raise ValueError("Time step size must be a positive float greater than 0")
    if args.time_step <= 0:
        raise ValueError("Number of time steps to output files must be a positive integer greater than 0")
    if args.duration <= 0:
        raise ValueError("Time to run the simulation (in timesteps) must be a positive integer greater than 0")
    if args.mouse_seed < 0:
        raise ValueError("Random seed for initializing mouse densities must be a non-negative integer")
    if args.fox_seed < 0:
        raise ValueError("Random seed for initializing fox densities must be a non-negative integer")

def validate_input_file_argument(landscape_file):
    """
    Validate the format and content of an input landscape file.

    This function checks whether the input landscape file has a valid format and contains
    appropriate values for width, height, and binary data (0 or 1) in the map data.
    It raises exceptions when the file format is invalid or the file does not exist.

    Args:
        landscape_file (str): The path to the input landscape file.

    Raises:
        ValueError: If the file format is invalid, containing incorrect values or not following the expected format.
        FileNotFoundError: If the specified landscape file does not exist.

    """
    try:
        with open(landscape_file, 'r') as file:
            # Read the first line and check if it contains valid values for width and height
            first_line = file.readline().strip().split()
            if len(first_line) != 2:
                raise ValueError("Invalid map format: The first line should contain only two positive integers (width and height).")
            
            width, height = map(int, first_line)
            if width <= 0 or height <= 0:
                raise ValueError("Invalid map format: Width and height of the landscape must be positive integers greater than 0.")
                            
            # Read the remaining lines and check if they have the correct format
            for _ in range(height):
                line = file.readline().strip().split()
                if len(line) != width:
                    raise ValueError("Invalid map format: The number of columns of the map should be the same as value of the first of the first line (width).")
                  
                # Check if map values are zeros and ones only  
                if not all(x in ['0', '1'] for x in line): 
                    raise ValueError("Invalid map format: Each line should only have '0' or '1'.")
                    
            
            # Check if there are more lines in the file
            if file.readline():
                raise ValueError("Invalid map format: The number of rows in the map should be the same as the value provided as the second of the first line (height).")
                    
    except FileNotFoundError:
        raise FileNotFoundError('The file {} does not exist.'.format(landscape_file))
