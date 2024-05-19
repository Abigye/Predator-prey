import os
from unittest import TestCase
from predator_prey.helper_functions import *

class TestHelperFunctions(TestCase):
    
    def setUp(self):
        self.expected_landscape = np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0]], dtype=int)
        self.width = 3
        self.height = 2
        self.width_with_halo = 5
        self.height_with_halo = 4
        self.densities = np.array([
            [0., 0., 0., 0., 0.],
            [0., 1., 1., 1., 0.],
            [0., 0., 1., 1., 0.],
            [0., 0., 0., 0., 0.]])
        self.num_lands = np.count_nonzero(self.expected_landscape)
        self.maximum_density = np.max(self.densities)
        self.time_step_index = 20
        self.land_neighbours = np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 3, 2, 0],
            [0, 2, 2, 2, 0],
            [0, 0, 0, 0, 0]], dtype=int)
        self.time_step_size = 1.0
        self.initial_mice_densities = self.densities
        self.initial_foxes_densities = self.densities
    
    def test_read_landscape_file_only_reads_valid_landscape_file(self):
        # Create a temporary landscape file with known data for testing
        with open("temp_landscape.dat", "w") as f:
            f.write("3 2\n1 1 1\n0 1 1\n")
        
        landscape_file = "temp_landscape.dat"
        
        width, height, width_with_halo, height_with_halo, landscape = read_landscape_file(landscape_file)

        # Check if the dimensions and values are as expected
        self.assertEqual(width, 3)
        self.assertEqual(height, 2)
        self.assertEqual(width_with_halo, 5)
        self.assertEqual(height_with_halo, 4)
        self.assertTrue(np.array_equal(landscape, self.expected_landscape))
        
    def test_calculate_total_neighbours_returns_neighbours_in_all_cardinal_directions(self):
        x, y = 2, 2 
        result = calculate_total_neighbours(x, y, self.expected_landscape)
        self.assertEqual(result, 2)  # Sum of north, south, east, and west neighbors

    def test_calculate_total_neighbours_returns_zero_there_are_no_neighbours(self):
        # Test when there are no neighbors (all zeros)
        x, y = 1, 1
        result = calculate_total_neighbours(x, y, np.zeros((3, 3)))
        self.assertEqual(result, 0)

    def test_calculate_total_neighbours_returns_neighbours_when_current_cell_is_at_edge_of_grid(self):
        x, y = 3, 2  # Cell at the bottom edge
        result = calculate_total_neighbours(x, y, self.expected_landscape)
        self.assertEqual(result, 1)  # Only north, east, and west neighbors

    def test_calculate_total_neighbours_returns_neighbours_when_current_cell_is_at_corner_of_grid(self):
        # Test when the cell is in a corner of the grid
        x, y = 0, 0  # Top-left corner
        result = calculate_total_neighbours(x, y, self.expected_landscape)
        self.assertEqual(result, 0)  # Only south and east neighbors
        
    def test_calculate_land_neighbours_calculates_appropriate_neighbours(self): 
        result = calculate_land_neighbours(self.width, self.height, self.width_with_halo, 
                                           self.height_with_halo, self.expected_landscape)
        self.assertTrue(np.array_equal(result, self.land_neighbours))
        
    def test_initialize_population_densities_seed_zero(self):
        seed = 0 
        result = initialize_population_densities(seed, self.width, self.height, self.expected_landscape)
        expected = np.zeros((self.height_with_halo, self.width_with_halo), dtype=float)
        self.assertTrue(np.array_equal(result, expected))

    def test_initialize_population_densities_seed_nonzero(self):
        seed = 42
        result = initialize_population_densities(seed, self.width, self.height, self.expected_landscape)
        self.assertTrue((result[1:self.height + 1, 1:self.width + 1] >= 0.0).all())
        self.assertTrue((result[1:self.height + 1, 1:self.width + 1] <= 5.0).all())
        
        expected = np.array([[0.0, 0.0, 0.0, 0.0, 0.0],
                            [0.0, 3.19713399, 0.12505378, 1.37514659, 0.0],
                            [0.0, 0.0, 1.11605369, 3.68235607, 0.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0]])
        # assert the arrays for almost exact equality
        self.assertTrue(np.allclose(result, expected, rtol=1e-8, atol=1e-8))

    def test_calculate_average_density_num_lands_zero(self):
        result = calculate_average_density(0, self.densities)
        self.assertEqual(result, 0.0)

    def test_calculate_average_density_num_lands_nonzero(self):
        result = calculate_average_density(self.num_lands, self.densities)
        self.assertEqual(result, 1.0)
        
    def test_calculate_colour_value_maximum_density_zero(self):
        result = calculate_colour_value(self.densities[1,3],0)
        self.assertEqual(result, 0)

    def test_calculate_colour_value_maximum_density_nonzero(self):
        result = calculate_colour_value(self.densities[1,3],self.maximum_density)
        self.assertEqual(result, 255.0)
        
    def test_save_ppm_file(self):
        foxes_density_colours = np.array([[0, 200, 240, 255, 0],
                                              [0, 255, 240, 200, 0],
                                              [0, 240, 240, 240, 0],
                                              [0, 0, 0, 0, 0]])
        mice_density_colours = np.array([[0, 0, 0, 0, 0],
                                             [200, 240, 240, 200, 0],
                                             [0, 255, 240, 255, 0],
                                             [0, 0, 0, 0, 0]])

        save_ppm_file(self.width, self.height, self.expected_landscape, 
                      foxes_density_colours, mice_density_colours, self.time_step_index)

        # Check if the PPM file was created
        ppm_file_path = os.path.join(os.getcwd(), "map_{:04d}.ppm".format(self.time_step_index))
        self.assertTrue(os.path.exists(ppm_file_path))

        # Check the content of the PPM file
        with open(ppm_file_path, "r") as f:
            ppm_content = f.read()

        expected_colors = ("P3\n3 2\n255\n0 0 0\n200 0 0\n240 0 0\n0 200 255\n255 240 0\n240 240 0\n")
        self.assertEqual(ppm_content, expected_colors)
        
    def test_calculate_migration_change(self):
        diffusion_rate = 0.1 
        result = calculate_migration_change(diffusion_rate, self.land_neighbours, self.densities, 2, 2)
        self.assertEqual(result, 0.0)
        
    def test_update_population_density_updates_mice_density(self):
        birth_rate = 0.3
        death_rate = 0.5
        diffusion_rate = 0.05
        x, y = 2, 2
        animal = 'mice'
        updated_density = update_population_density(
            birth_rate, death_rate, diffusion_rate, self.time_step_size, self.land_neighbours, 
            self.initial_mice_densities, self.initial_foxes_densities, x, y, animal
        )
        self.assertEqual(updated_density, 0.8)

    def test_test_update_population_density_updates_foxes_density(self):
        birth_rate = 0.1
        death_rate = 0.2
        diffusion_rate = 0.05
        x, y = 1, 1
        animal = 'foxes'
        updated_density = update_population_density(
            birth_rate, death_rate, diffusion_rate, self.time_step_size, self.land_neighbours, 
            self.initial_mice_densities, self.initial_foxes_densities, x, y, animal
        )
        self.assertEqual(updated_density, 0.9)
    
    def test_update_population_density_return_zero_instead_of_negative_density(self):
        birth_rate = 0.1
        death_rate = 0.2
        diffusion_rate = 0.05
        self.time_step_size = 10.0
        land_neighbours = np.array([
                                    [0, 0, 0],
                                    [0, 4, 0],
                                    [0, 0, 0]])
        self.initial_mice_densities = np.array([
                                    [0., 0., 0.],
                                    [0., 1., 0.],
                                    [0., 0., 0.]])
            
        self.initial_foxes_densities = np.array([
                                    [0., 0., 0.],
                                    [0., 1., 0.],
                                    [0., 0., 0.]])
        x, y = 1, 1
        animal = 'foxes'
        updated_density = update_population_density(
            birth_rate, death_rate, diffusion_rate, self.time_step_size, land_neighbours, 
            self.initial_mice_densities, self.initial_foxes_densities, x, y, animal
        )
        # expected = 1.0 + 10.0 * (((0.1 * 1.0 * 1.0) - (0.2 * 1.0)) + (0.05 * (0.0 - (4*1.0)))) , gives -2.0000000000000004
        self.assertEqual(updated_density, 0)
        
    def test_update_population_densities(self):
        mice_birth_rate = 0.2
        mice_death_rate = 0.1
        mice_diffusion_rate = 0.05
        foxes_birth_rate = 0.3
        foxes_death_rate = 0.15
        foxes_diffusion_rate = 0.1
        new_mice_densities = np.zeros_like(self.densities)
        new_foxes_densities = np.zeros_like(self.densities)

        update_population_densities(
            mice_birth_rate, mice_death_rate, mice_diffusion_rate,
            foxes_birth_rate, foxes_death_rate, foxes_diffusion_rate,
            self.time_step_size, self.width, self.height, self.expected_landscape,
            self.land_neighbours, self.initial_mice_densities, new_mice_densities,
            self.initial_foxes_densities, new_foxes_densities
        ) 
        expected_new_mice_density = np.array([[0.0, 0.0, 0.0, 0.0, 0.0],
                                            [0.0, 1.1, 1.1, 1.1, 0.0],
                                            [0.0, 0.0, 1.1, 1.1, 0.0],
                                            [0.0, 0.0, 0.0, 0.0, 0.0]])
        expected_new_foxes_density = np.array([[0.0, 0.0, 0.0, 0.0, 0.0],
                                            [0.0, 1.15, 1.15, 1.15, 0.0],
                                            [0.0, 0.0, 1.15, 1.15, 0.0],
                                            [0.0, 0.0, 0.0, 0.0, 0.0]])

        self.assertTrue(np.array_equal(new_mice_densities, expected_new_mice_density))
        self.assertTrue(np.array_equal(new_foxes_densities, expected_new_foxes_density))
        
        self.assertTrue(np.all(new_mice_densities >= 0))
        self.assertTrue(np.all(new_foxes_densities >= 0))
        
    def test_calculate_density_colors(self):
        maximum_mice_density = 1.0
        maximum_foxes_density = 1.5
        mice_density_colours = np.zeros((self.height, self.width), dtype=int)
        foxes_density_colours = np.zeros((self.height, self.width), dtype=int)
        calculate_density_colors(self.height, self.width, self.expected_landscape, self.initial_mice_densities, 
                                 maximum_mice_density, self.initial_foxes_densities, maximum_foxes_density, 
                                 mice_density_colours, foxes_density_colours)
           
        expected_mice_density_colours = np.array([[255, 255, 255],[0, 255, 255]])
        expected_foxes_density_colours = np.array([[170, 170, 170],[0, 170, 170]])
        
        self.assertTrue(np.array_equal(mice_density_colours, expected_mice_density_colours))
        self.assertTrue(np.array_equal(foxes_density_colours, expected_foxes_density_colours))
        
        self.assertTrue(np.all(mice_density_colours >= 0) & np.all(mice_density_colours <= 255))
        self.assertTrue(np.all(foxes_density_colours >= 0) & np.all(foxes_density_colours <= 255))
        
    def test_calculate_density_statics(self):
        result = calculate_density_statistics(self.initial_mice_densities, self.initial_foxes_densities, self.num_lands)
        self.assertEqual(result,(1.0, 1.0, 1.0, 1.0))
        
    def test_initialize_arrays(self):
        seed = 42
        initial_densities, new_densities, density_colors = initialize_arrays(seed, self.width, self.height, self.expected_landscape)

        # Assert that the shapes of the arrays match the specified width and height
        expected = initialize_population_densities(seed, self.width, self.height, self.expected_landscape)
    
        self.assertEqual(initial_densities.shape, expected.shape)
        self.assertEqual(new_densities.shape, expected.shape)
        self.assertEqual(density_colors.shape, (self.height, self.width))

        # Assert that all values in the density arrays are almost equal with small tolerance
        self.assertTrue(np.allclose(initial_densities, expected, rtol=1e-8, atol=1e-8))
        self.assertTrue(np.allclose(new_densities, initial_densities, rtol=1e-8, atol=1e-8))

        # Assert that all values in the density_colors array are initialized to 0
        self.assertTrue(np.all(density_colors == 0))
    
    def tearDown(self):
        # remove the temporary created PPM and landscape file
        ppm_file_path = os.path.join(os.getcwd(), "map_{:04d}.ppm".format(self.time_step_index))
        if os.path.exists(ppm_file_path):
            os.remove(ppm_file_path)
        
        landscape_file_path = os.path.join(os.getcwd(), "temp_landscape.dat")
        if os.path.exists(landscape_file_path):
            os.remove(landscape_file_path)
