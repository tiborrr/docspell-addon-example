import unittest
import subprocess

class TestContainerResponse(unittest.TestCase):
    def test_container_hello_response(self):
        subprocess.run(['docker', 'compose', 'build'])
        result = subprocess.run(['docker', 'run', 'tiborrr/docspell-addon-example', 'John'], capture_output=True, text=True)
        
        # Check if the output from the container is as expected
        self.assertEqual(result.stderr.strip(), 'Hello John')

if __name__ == '__main__':
    unittest.main()