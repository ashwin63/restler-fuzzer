import typing
import random
import time
import string
import itertools
import subprocess
import re
import base64  
random_seed=time.time()
#print(f"Value generator random seed: {random_seed}")
random.seed(random_seed)
EXAMPLE_ARG = "examples"

def get_next_val(fuzzable_integer):
    #return subprocess.run('echo "ashwin"',capture_output= True)
    #return subprocess.run(['"ashwin" |radamsa'], capture_output=True)
    while True:
        command = 'echo ' + fuzzable_integer + ' | radamsa'
        result = subprocess.run(command, shell=True, capture_output=True)
        
        mutated_output = result.stdout.decode('utf-8', errors='ignore')
        
        # Filter to include only lowercase alphabetic characters
        filtered_output = ''.join(filter(str.isalpha, mutated_output)).lower()
        
        if filtered_output:
            return filtered_output.strip()
        
def get_next_string(fuzzable_string: str) -> str:
    """
    Generate a mutated string using Radamsa.
    
    Args:
    - filename (str): The name of the file to write the value to.
    
    Returns:
    - str: The generated string.
    """
    command = 'echo '+ fuzzable_string +' | radamsa'
    result = subprocess.run(command, shell=True, capture_output=True)
    
    # Handle the output as bytes
    mutated_output = result.stdout
    
    try:
        # Attempt to decode the output as UTF-8
        decoded_output = mutated_output.decode('utf-8')
        return decoded_output.strip()
    except UnicodeDecodeError:
        # Handle non-decodable bytes (optional)
        # Example: return base64 encoded output
        return base64.b64encode(mutated_output).decode('utf-8')
    
def get_next_unquoted_string(fuzzable_unquoted_string: str) -> str:
    """
    Generate a mutated string using Radamsa and ensure it is unquoted.
    
    Args:
    - filename (str): The name of the file to write the value to.
    
    Returns:
    - str: The generated unquoted string.
    """
    while True:
        string_val = get_next_string(fuzzable_unquoted_string)
        unquoted_string = string_val.strip('"')
        return unquoted_string
    
def get_next_number(fuzzable_number):
    while True:
        command = 'echo ' + fuzzable_number +' | radamsa --mutations num'  # Using a simple base number for mutations
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        mutated_output = result.stdout.strip()
        # Filter the output to ensure it's a positive number
        if re.match(r'^\-?\d+$', mutated_output):  # Match integers (possibly negative)
            return mutated_output

def gen_restler_fuzzable_int(**kwargs):
    #print(kwargs["examples"].request_block)
    if kwargs["examples"].request_block[0] == "restler_fuzzable_int":
        while True:
            yield get_next_val(kwargs["examples"].request_block[1])

def gen_restler_fuzzable_string(**kwargs):
    #print(kwargs["examples"].request_block)
    if kwargs["examples"].request_block[0] == "restler_fuzzable_string":
        while True:
            yield get_next_string(kwargs["examples"].request_block[1])

def gen_restler_fuzzable_string_unquoted(**kwargs):
    #print(kwargs["examples"].request_block)
    if kwargs["examples"].request_block[0] == "restler_fuzzable_unquoted":
        while True:
            yield get_next_unquoted_string(kwargs["examples"].request_block[1])

def gen_restler_fuzzable_number(**kwargs):
    #print(kwargs["examples"].request_block)
    if kwargs["examples"].request_block[0] == "restler_fuzzable_number":
        while True:
            yield get_next_number(kwargs["examples"].request_block[1])
    

value_generators = {
    "restler_fuzzable_int": gen_restler_fuzzable_int,
    "restler_fuzzable_number": gen_restler_fuzzable_number,
    "restler_fuzzable_string": gen_restler_fuzzable_string
   # "restler_fuzzable_string_unquoted": gen_restler_fuzzable_string_unquoted
}
#print(get_next_val("sample_file_name_not_used"))
