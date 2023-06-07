#Andres Portillo
#COP3502
#2/19/2023



from console_gfx import ConsoleGfx

def to_hex_string(data):
    decimal_hex_map = {
        0: "0", 1: "1", 2: "2", 3: "3",
        4: "4", 5: "5", 6: "6", 7: "7",
        8: "8", 9: "9", 10: "A", 11: "B",
        12: "C", 13: "D", 14: "E", 15: "F"
    }
    hex_str = "".join([decimal_hex_map[item] for item in data])
    return hex_str.lower()

def count_runs(flat_data):
    if not flat_data:
        return []
    current_run = {"length": 1, "value": flat_data[0]}
    run_counter = 0
    for pixel in flat_data[1:]:
        if pixel == current_run["value"]:
            if current_run["length"] == 15:
                run_counter += 1
                current_run = {"length": 1, "value": pixel}
            else:
                current_run["length"] += 1
        else:
            run_counter += 1
            current_run = {"length": 1, "value": pixel}
    run_counter += 1
    return run_counter

def encode_rle(flat_data):
    if not flat_data:
        return []
    rle_data = []
    current_run = {"value": flat_data[0], "length": 1}
    for pixel in flat_data[1:]:
        if pixel == current_run["value"]:
            if current_run["length"] == 15:
                rle_data.extend([current_run["length"], current_run["value"]])
                current_run = {"value": pixel, "length": 1}
            else:
                current_run["length"] += 1
        else:
            rle_data.extend([current_run["length"], current_run["value"]])
            current_run = {"value": pixel, "length": 1}
    rle_data.extend([current_run["length"], current_run["value"]])
    return rle_data

# Returns decompressed size RLE data; used to generate flat data from RLE encoding. (Counterpart to #2)
# Ex: get_decoded_length([3, 15, 6, 4]) yields integer 9.
def get_decoded_length(rle_data):
    return sum(rle_data[i] for i in range(0, len(rle_data), 2))

# Returns the decoded data set from RLE encoded data. This decompresses RLE data for use. (Inverse of #3)
# Ex: decode_rle([3, 15, 6, 4]) yields list [15, 15, 15, 4, 4, 4, 4, 4, 4].
def decode_rle(rle_data):
    raw_data = []

    # moving window which contains 2 elements in the list
    # in this list [1, 2, 3, 4, 5, 6, 7, 8], the window would be
    # [1, 2], then [3, 4], then [5, 6] etc
    for encoded_length_index in range(0, len(rle_data), 2):
        encoded_length = rle_data[encoded_length_index]
        encoded_data = rle_data[encoded_length_index+1]

        # add the encoded data to raw_data length times
        for _ in range(encoded_length):
            raw_data.append(encoded_data)

    return raw_data

# Translates a string in hexadecimal format into byte data (can be raw or RLE). (Inverse of #1)
# Ex: string_to_data ("3f64") yields list [3, 15, 6, 4].
def string_to_data(data_string):
    raw_data = []
    for hex_char in data_string:
        raw_data.append(hex_char_to_decimal(hex_char))

    return raw_data

# Translates  RLE data into  a human-readable representation.  For  each  run,  in  order,  it should  display  the  run
# length in decimal (1-2 digits); the run value in hexadecimal (1 digit); and a delimiter, ‘:’, between runs. (See
# examples in standalone section.)
# Ex: to_rle_string([15, 15, 6, 4]) yields string "15f:64".
def to_rle_string(rle_data):
    rle_string = ""
    for i in range(0, len(rle_data), 2):
        run_length = rle_data[i]
        run_value = rle_data[i+1]
        rle_string += str(run_length) + decimal_to_hex(run_value) + ":"
    return rle_string[:-1]


# Translates a string in human-readable RLE format (with delimiters) into RLE byte data. (Inverse of #7)
# Ex: string_to_rle("15f:64") yields list [15, 15, 6, 4].
def string_to_rle(rle_string):
    pass

# I copied this code from my lab4 code
# TODO delete this code?
#
# convert a decimal number to hex
# using acsii MAGIC!
#
# TYPE:
# - number is an int (positive)
# - returns a string (hex repr. of number)
def decimal_to_hex(number):
    hex_chars = "0123456789ABCDEF"
    hex = ""

    while number != 0:
        remainder = number % 16
        hex = hex_chars[remainder] + hex
        number //= 16

    if hex == "":
        hex = "0"

    return hex

# take in a single hex char and return its decimal representation
def hex_char_to_decimal(hex_char):
    # make sure the char has length 1
    if len(hex_char) != 1:
        error(f"hex char should only have length 1, got {hex_char}")

    # make sure that it is uppercase
    hex_char = hex_char.upper()

    # convert the hex char to a decimal value
    if hex_char.isdigit():
        return int(hex_char)
    else:
        return ord(hex_char) - 55


# easy error messages
def error(msg):
    raise Exception(msg)

# print the welcome message
def welcome():
    print("Welcome to the RLE image encoder!")

def menu():
    print("")
    print("RLE Menu")
    print("--------")
    print("0. Exit")
    print("1. Load File")
    print("2. Load Test Image")
    print("3. Read RLE String")
    print("4. Read RLE Hex String")
    print("5. Read Data Hex String")
    print("6. Display Image")
    print("7. Display RLE String")
    print("8. Display Hex RLE Data")
    print("9. Display Hex Flat Data")
    print("")

def menu_input():
    user_input = int(input("Select a Menu Option: "))

    # make sure the input is valid and if its not,
    # crash
    if user_input < 0 or user_input > 9:
        error(f"invalid menu input! GOT: {user_input}")

    return user_input

def main():
    current_image = None

    welcome()
    print("")

    print("Displaying Spectrum Image:")
    ConsoleGfx.display_image(ConsoleGfx.test_rainbow)
    print("")

    menu_options = {
        0: exit_program,
        1: load_file,
        2: load_test_image,
        3: read_rle_string,
        4: read_rle_hex_string,
        5: read_data_hex_string,
        6: display_image,
        7: display_rle_string,
        8: display_hex_rle_data,
        9: display_hex_flat_data,
    }

    while True:
        menu()
        user_selection = menu_input()

        if user_selection in menu_options:
            current_image = menu_options[user_selection](current_image)
        else:
            print("Invalid selection. Please try again.\n")


def exit_program(current_image):
    return None


def load_file(current_image):
    filename = input("Enter name of file to load: ")
    return ConsoleGfx.load_file(filename)


def load_test_image(current_image):
    print("Test image data loaded.")
    return ConsoleGfx.test_image


def read_rle_string(current_image):
    print("Reading RLE string...")
    return current_image


def read_rle_hex_string(current_image):
    print("Reading RLE hex string...")
    return current_image


def read_data_hex_string(current_image):
    print("Reading data hex string...")
    return current_image


def display_image(current_image):
    if current_image is None:
        print("No image loaded. Please load an image first.\n")
    else:
        ConsoleGfx.display_image(current_image)


def display_rle_string(current_image):
    print("Displaying RLE string...")
    return current_image


def display_hex_rle_data(current_image):
    print("Displaying hex RLE data...")
    return current_image


def display_hex_flat_data(current_image):
    print("Displaying hex flat data...")
    return current_image


# the methods I am required to implement have
# sample inputs and outputs
# this function makes sure tha the functions behave as expected
def tests():
    # tests from the comments provided in the pdf
    assert to_hex_string([3, 15, 6, 4]) == "3f64"
    assert count_runs([15, 15, 15, 4, 4, 4, 4, 4, 4]) == 2
    assert encode_rle([15, 15, 15, 4, 4, 4, 4, 4, 4]) == [3, 15, 6, 4]
    assert get_decoded_length([3, 15, 6, 4]) == 9
    assert get_decoded_length([7, 15, 7, 4]) == 14
    assert decode_rle([3, 15, 6, 4]) == [15, 15, 15, 4, 4, 4, 4, 4, 4]
    assert string_to_data ("3f64") == [3, 15, 6, 4]

    # tests from zybooks
    assert count_runs([1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5]) == 25
    assert count_runs([4,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8,7 ]) == 6

    assert encode_rle([4,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8,7]) == [2,4,15,1,15,1,5,1,1,8,1,7]
    assert encode_rle([1,2,3,4,1,2,3,4]) == [1,1,1,2,1,3,1,4,1,1,1,2,1,3,1,4]
    assert encode_rle([4,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]) == [2,4,15,1,15,1,5,1]
    assert encode_rle([4,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]) == [1,4,1,5,15,1,15,1,5,1]

    assert decode_rle([2,4,15,1,15,1,5,1,1,8,1,7]) == [4,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,8,7]

if __name__ == "__main__":
    tests()
    main()