# run_tests.py

import unittest
import sys
import os

def run_tests():
    """Run all tests in the tests directory"""
    # Add the parent directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return 0 if tests passed, 1 if any failed
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())
