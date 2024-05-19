import os
from unittest import TestCase
from predator_prey.simulate_predator_prey import *

def create_temp_landscape_file(content):
    file_path = os.path.join(os.getcwd(), "temp_landscape.dat")
    with open(file_path, "w") as f:
        f.write(content)
    return file_path

class TestSimulation(TestCase):
        
    def setUp(self):
        # Create a temporary landscape file with known data for testing
        with open("temp_landscape.dat", "w") as f:
            f.write("3 2\n1 1 1\n0 1 1\n")
        
        self.landscape_file = "temp_landscape.dat"
    
    def test_getVersion(self):
        version = getVersion()
        self.assertEqual(version, 3.0)
            
    def test_run_simulation(self):
        mice_birth_rate = 0.5
        mice_death_rate = 0.2
        mice_diffusion_rate = 0.1
        foxes_birth_rate = 0.4
        foxes_death_rate = 0.3
        foxes_diffusion_rate = 0.2
        time_step_size = 1
        output_time_step = 1
        simulation_duration = 2
        mouse_seed = 42
        fox_seed = 42

        run_simulation(
            mice_birth_rate,
            mice_death_rate,
            mice_diffusion_rate,
            foxes_birth_rate,
            foxes_death_rate,
            foxes_diffusion_rate,
            time_step_size,
            output_time_step,
            simulation_duration,
            self.landscape_file,
            mouse_seed,
            fox_seed
        )

        self.assertTrue(os.path.exists("averages.csv"))
        self.assertTrue(os.path.exists("map_0000.ppm"))
        self.assertTrue(os.path.exists("map_0001.ppm"))
        
        expected_averages_content = ['Timestep,Time,Mice,Foxes\n', '0,0.0,1.89914882436250498,1.89914882436250498\n', '1,1.0,1.77137705920111133,3.48409653173904710\n']
        expected_map_0000_content = ['P3\n', '3 2\n', '255\n', '221 221 0\n', '8 8 0\n', '95 95 0\n', '0 200 255\n', '77 77 0\n', '255 255 0\n']
        expected_map_0001_content = ['P3\n', '3 2\n', '255\n', '207 255 0\n', '41 74 0\n', '70 186 0\n', '0 200 255\n', '57 165 0\n', '255 242 0\n']

        self.assert_file_content_equal("averages.csv", expected_averages_content)
        self.assert_file_content_equal("map_0000.ppm", expected_map_0000_content)
        self.assert_file_content_equal("map_0001.ppm", expected_map_0001_content)
        
        # Clean up specific map files
        for i in range(0, 2):  # Assuming a certain number of map files
            ppm_file_path = "map_{:04d}.ppm".format(i)
            if os.path.exists(ppm_file_path):
                os.remove(ppm_file_path)

    def tearDown(self):
        # Clean up any resources created during the test
        if os.path.exists(self.landscape_file):
            os.remove(self.landscape_file)

    def assert_file_content_equal(self, file_path, expected_content):
        with open(file_path, "r") as f:
            actual_content = f.readlines()        
        self.assertEqual( actual_content, expected_content)
        
    def test_create_temp_landscape_file(self):
        content = "3 2\n1 1 1\n0 1 1\n"
        file_path = create_temp_landscape_file(content)

        # Check if the file was created
        self.assertTrue(os.path.exists(file_path))

        # Check if the file content matches the provided content
        with open(file_path, "r") as f:
            file_content = f.read()
        self.assertEqual(file_content, content)
