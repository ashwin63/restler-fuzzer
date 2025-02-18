import typing
import random
import time
import string
import itertools
import subprocess
import re
import os, json, random
import base64  
import utils.logger as logger
random_seed=time.time()
#print(f"Value generator random seed: {random_seed}")
random.seed(random_seed)
EXAMPLE_ARG = "req"

def get_next_val(fuzzable_integer):
    #return subprocess.run('echo "ashwin"',capture_output= True)
    #return subprocess.run(['"ashwin" |radamsa'], capture_output=True)
    while True:
        command = 'echo ' + fuzzable_integer + ' | radamsa'
        result = subprocess.run(command, shell=True, capture_output=True)
        
        #mutated_output = result.stdout.decode('utf-8', errors='ignore')
        try:
            mutated_output = int(result.stdout.strip())
        except ValueError:
            mutated_output = fuzzable_integer 
        return mutated_output
        # Filter to include only lowercase alphabetic characters
        #filtered_output = ''.join(filter(str.isalpha, mutated_output)).lower()
        
        #if filtered_output:
        #    return filtered_output.strip()
        
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
            print(fuzzable_number)
            print(mutated_output)
            return mutated_output
        else:
            print(fuzzable_number+" dud nit change")
            return fuzzable_number

def get_value_from_json(sequence_id, request_id, idx):
    filename = os.path.join(logger.DYNAMIC_VALUES_DIR, "sequence_info")

    # Check if file exists
    if not os.path.isfile(filename):
        return 99

    # Read data from the file
    with open(filename, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in sequence_info file.")

    # Check if sequence_id exists
    if sequence_id not in data:
        return 99

    # Check if request_id exists within the sequence
    if request_id not in data[sequence_id]:
        return 99#raise KeyError(f"Request ID '{request_id}' not found in sequence '{sequence_id}'.")

    # Check if idx exists within the request
    if str(idx) not in data[sequence_id][request_id]:
        return 99#raise KeyError(f"Index '{idx}' not found in request '{request_id}' under sequence '{sequence_id}'.")

    # Return the value
    return data[sequence_id][request_id][str(idx)]

def gen_restler_fuzzable_int(**kwargs):
    val = get_value_from_json(kwargs[EXAMPLE_ARG].temp_sequence_hex,kwargs[EXAMPLE_ARG].method_endpoint_hex_definition,kwargs[EXAMPLE_ARG].generator_value_idx)
    yield get_next_number(str(val) if str(val).isnumeric()else str(99))
    #print(kwargs["examples"].hex_definition)
    #filename = os.path.join(logger.DYNAMIC_VALUES_DIR,kwargs[EXAMPLE_ARG].hex_definition)
    # if os.path.isfile(filename):
    #     with open(filename, 'r') as file:
    #         data = json.load(file)
    #         length = len(data)
    #         next_index = random.randrange(length)
    #     while True:
    #        yield get_next_val(data[next_index][str(kwargs[EXAMPLE_ARG].idx)])
    # else:
    #yield get_next_val("11")

def gen_restler_fuzzable_string(**kwargs):
    #print(kwargs["examples"].hex_definition)
    filename = os.path.join(logger.DYNAMIC_VALUES_DIR,kwargs[EXAMPLE_ARG].hex_definition)
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            length = len(data)
            next_index = random.randrange(length)
        while True:
            yield get_next_string(data[next_index][str(kwargs[EXAMPLE_ARG].idx)])
    else:
        yield get_next_string("hello")

def gen_restler_fuzzable_string_unquoted(**kwargs):
    #print(kwargs["examples"].hex_definition)
    filename = os.path.join(logger.DYNAMIC_VALUES_DIR,kwargs[EXAMPLE_ARG].hex_definition)
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            length = len(data)
            next_index = random.randrange(length)
        while True:
            yield get_next_unquoted_string(data[next_index][str(kwargs[EXAMPLE_ARG].idx)])
    else:
        yield get_next_unquoted_string("hello")

def gen_restler_fuzzable_number(**kwargs):
    #print(kwargs["examples"].hex_definition)
    filename = os.path.join(logger.DYNAMIC_VALUES_DIR,kwargs[EXAMPLE_ARG].hex_definition)
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            length = len(data)
            next_index = random.randrange(length)
        while True:
            yield get_next_number(data[next_index][str(kwargs[EXAMPLE_ARG].idx)])
    else:
        yield get_next_number("hello")
    

value_generators = {
    "restler_fuzzable_int": gen_restler_fuzzable_int,
    #"restler_fuzzable_number": gen_restler_fuzzable_number,
    #"restler_fuzzable_string": gen_restler_fuzzable_string
   # "restler_fuzzable_string_unquoted": gen_restler_fuzzable_string_unquoted
}
#print(get_next_val("sample_file_name_not_used"))
