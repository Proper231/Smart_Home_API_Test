import concurrent.futures
import subprocess

def run_python_file(file_path):
    # Call the Python interpreter with the given file path
    subprocess.run(['python', file_path])

if __name__ == "__main__":
    # List the paths of the three Python files to be executed
    file_paths = [
#        'test2ConvoS.py',
#        'test2ConvoC',
        'STText.py',
        'LLM_final.py',
        'coqui.py'

    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_python_file , file_paths )
