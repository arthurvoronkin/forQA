import hashlib
import sys
from os import walk


def md5sum(file_name, block_size=65536):                            # Below functions to detect a checksum
    the_hash = hashlib.md5()
    with open(file_name, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            the_hash.update(block)
    return the_hash.hexdigest()


def sha1sum(file_name, block_size=65536):
    the_hash = hashlib.sha1()
    with open(file_name, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            the_hash.update(block)
    return the_hash.hexdigest()


def sha256sum(file_name, block_size=65536):
    the_hash = hashlib.sha256()
    with open(file_name, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            the_hash.update(block)
    return the_hash.hexdigest()


source_argument_file = sys.argv[1]       # Input file with parameters and directory with files
target_directory = sys.argv[2]           # It should be with \ or / at the end for the path i.e. /home/user/Documents/


with open(source_argument_file, 'r') as source_file:  # Reading lines of the source file
    file_arguments = source_file.readlines()

_, _, list_of_target_files = next(walk(target_directory))  # Getting names of target directory's files

for arguments in file_arguments:                          # Iterate through parameters
    devided_string = str(arguments).rstrip('\n').split()  # Splitting the parameters string by ' ' and cutting \n
    checksum_of_input_file = devided_string[-1].lower().strip()  # The checksum should be after the last ' '
    checksum_algorithm = devided_string[-2].lower().strip()  # Checksum algorithm should be before checksum + cut ' '

    filename = arguments[: arguments.rfind(' ')].strip()    # File should be at lease after 2 empty spaces from the end

    filename = filename[: filename.rfind(' ')].strip()      # So we are doing it twice + cutting unwanted spaces

    if filename in list_of_target_files:                    # Checking if file exists in the target directory
        checksum_calculation = None
        file_path = target_directory + filename             # Constructing the file path with a filename
        if checksum_algorithm == 'md5':                     # Checking the algorithm and running it
            checksum_calculation = md5sum(file_path)
        elif checksum_algorithm == 'sha1':
            checksum_calculation = sha1sum(file_path)
        elif checksum_algorithm == 'sha256':
            checksum_calculation = sha256sum(file_path)
        if checksum_calculation == checksum_of_input_file:
            print(filename, 'OK')                           # If filename exists on the target and checksum match -> OK
        else:
            print(filename, 'FAIL')                    # If filename exists on the target and checksum mismatch -> FAIL
    else:
        print(filename, 'NOT FOUND')                    # If filename doesn't exists on the target -> NOT FOUND
