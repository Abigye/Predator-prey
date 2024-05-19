import os
from unittest import TestCase
from argparse import Namespace
from predator_prey.validate_arguments import *

def create_temp_landscape_file(content):
    file_path = os.path.join(os.getcwd(), "temp_landscape.dat")
    with open(file_path, "w") as f:
        f.write(content)
    return file_path

class TestValidateCommandLineArguments(TestCase):
    
    def setUp(self):
        self.args = Namespace(
            birth_mice = 0.5,
            death_mice = 0.2,
            diffusion_mice = 0.1,
            birth_foxes = 0.4,
            death_foxes = 0.3,
            diffusion_foxes = 0.2,
            delta_t = 0.1,
            time_step = 100,
            duration = 1000,
            mouse_seed = 42,
            fox_seed = 42,
        )
    
    def test_create_temp_landscape_file(self):
        content = "3 2\n1 1 1\n0 1 1\n"
        file_path = create_temp_landscape_file(content)

        # Check if the file was created
        self.assertTrue(os.path.exists(file_path))

        # Check if the file content matches the provided content
        with open(file_path, "r") as f:
            file_content = f.read()
        self.assertEqual(file_content, content)
       
    def test_validate_input_file_argument_tests_valid_landscape_file(self):
        content = "2 2\n0 1\n1 0\n"
        file_path = create_temp_landscape_file(content)
        validate_input_file_argument(file_path)
        self.assertTrue(True)

    def test_validate_input_file_argument_tests_not_existent_landscape_file(self):
        invalid_file_path = "non_existent_file.dat"
        with self.assertRaises(FileNotFoundError) as context:
            validate_input_file_argument(invalid_file_path)
        expected_message = "The file non_existent_file.dat does not exist."
        self.assertEqual(expected_message, str(context.exception))
        
    def test_validate_input_file_argument_tests_for_more_two_values_on_first_line(self):
        content = "2 2 1\n1 0\n"
        file_path = create_temp_landscape_file(content)
        with self.assertRaises(ValueError) as context:
            validate_input_file_argument(file_path)
        expected_message = "Invalid map format: The first line should contain only two positive integers (width and height)."
        self.assertEqual(expected_message,  str(context.exception))
        
    def test_validate_input_file_argument_tests_for_invalid_dimensions(self):
        content = "2 0\n1\n1\n"
        file_path = create_temp_landscape_file(content)
        with self.assertRaises(ValueError) as context:
            validate_input_file_argument(file_path)
        expected_message = "Invalid map format: Width and height of the landscape must be positive integers greater than 0."
        self.assertEqual(expected_message,  str(context.exception))

    def test_validate_input_file_argument_tests_for_format_inconsistent_width(self):
        content = "2 2\n1 0\n1\n"
        file_path = create_temp_landscape_file(content)
        with self.assertRaises(ValueError) as context:
            validate_input_file_argument(file_path)
        expected_message = "Invalid map format: The number of columns of the map should be the same as value of the first of the first line (width)."
        self.assertEqual(expected_message, str(context.exception))

    def test_validate_input_file_argument_tests_for_invalid_characters_in_map(self):
        content = "2 2\n1 0\n1 2\n"
        file_path = create_temp_landscape_file(content)
        with self.assertRaises(ValueError) as context:
            validate_input_file_argument(file_path)
        expected_message = "Invalid map format: Each line should only have '0' or '1'."
        self.assertEqual(expected_message, str(context.exception))

    def test_validate_input_file_argument_tests_for_format_inconsistent_height(self):
        content = "2 2\n1 0\n1 0\n1 1\n"
        file_path = create_temp_landscape_file(content)
        with self.assertRaises(ValueError) as context:
            validate_input_file_argument(file_path)
        expected_message = "Invalid map format: The number of rows in the map should be the same as the value provided as the second of the first line (height)."
        self.assertEqual(expected_message, str(context.exception))
        
    def test_validate_arguments_validates_birth_mice(self):
        self.args.birth_mice = -0.5
        with self.assertRaises(ValueError) as context:
            validate_arguments(self.args)
        self.assertEqual("Birth rate of mice must be a positive float greater than 0", str(context.exception))

    def test_validate_arguments_validates_death_mice(self):
        self.args.death_mice = -0.5
        with self.assertRaises(ValueError) as context:
            validate_arguments(self.args)
        self.assertEqual("Death rate of mice must be a positive float greater than 0", str(context.exception))

    def test_validate_arguments_validates_diffusion_mice(self):
        self.args.diffusion_mice = -0.5
        with self.assertRaises(ValueError) as context:
            validate_arguments(self.args)
        self.assertEqual("Diffusion rate of mice must be a positive float greater than 0", str(context.exception))

    def test_validate_arguments_validates_birth_foxes(self):
        self.args.birth_foxes = -0.5
        with self.assertRaises(ValueError) as context:
            validate_arguments(self.args)
        self.assertEqual("Birth rate of foxes must be a positive float greater than 0", str(context.exception))

    def test_validate_arguments_validates_death_foxes(self):
        self.args.death_foxes = -0.5
        with self.assertRaises(ValueError) as context:
            validate_arguments(self.args)
        self.assertEqual("Death rate of foxes must be a positive float greater than 0", str(context.exception))

    def test_validate_arguments_validates_diffusion_foxes(self):
        self.args.diffusion_foxes = -0.5
        with self.assertRaises(ValueError) as context:
            validate_arguments(self.args)
        self.assertEqual("Diffusion rate of foxes must be a positive float greater than 0", str(context.exception))

    def test_validate_arguments_validates_time_step_size(self):
        self.args.delta_t = 0
        with self.assertRaises(ValueError) as context:
            validate_arguments(self.args)
        self.assertEqual("Time step size must be a positive float greater than 0", str(context.exception))

    def test_validate_arguments_validates_time_steps(self):
        self.args.time_step = 0
        with self.assertRaises(ValueError) as context:
            validate_arguments(self.args)
        self.assertEqual("Number of time steps to output files must be a positive integer greater than 0", str(context.exception))

    def test_validate_arguments_validates_simulation_duration(self):
        self.args.duration = 0
        with self.assertRaises(ValueError) as context:
            validate_arguments(self.args)
        self.assertEqual("Time to run the simulation (in timesteps) must be a positive integer greater than 0", str(context.exception))

    def test_validate_arguments_validates_mouse_seed(self):
        self.args.mouse_seed = -1
        with self.assertRaises(ValueError) as context:
            validate_arguments(self.args)
        self.assertEqual("Random seed for initializing mouse densities must be a non-negative integer", str(context.exception))

    def test_validate_arguments_validates_fox_seed(self):
        self.args.fox_seed = -1
        with self.assertRaises(ValueError) as context:
            validate_arguments(self.args)
        self.assertEqual("Random seed for initializing fox densities must be a non-negative integer", str(context.exception))
        
    def tearDown(self):
        # remove the created landscape file
        landscape_file_path = os.path.join(os.getcwd(), "temp_landscape.dat")
        if os.path.exists(landscape_file_path):
            os.remove(landscape_file_path)
