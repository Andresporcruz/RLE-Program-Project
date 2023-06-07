#Andres Portillo
#COP3502
#3/10/2023


# import the ConsoleGfx class
from console_gfx import ConsoleGfx



def to_hex_string(data):

    # initialize an empty string to store hex values
    hex = ""

    # create a map of decimal to hex values
    decimal_hex_map = {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "A",
        11: "B",
        12: "C",
        13: "D",
        14: "E",
        15: "F",
    }

    # loop through each item in the list and convert it to a hex value
    for item in data:
        hex += decimal_hex_map[item]

    # return the hex string in lowercase
    return hex.lower()



def count_runs(flat_data):
    # if the list is empty, return an empty list
    if not flat_data:
        return []

    # initialize the run counter to 1 and create a dictionary to store the current run
    run_counter = 1
    current_run = {"length": 1, "value": flat_data[0]}

    # loop through each pixel in the flat image
    for pixel in flat_data[1:]:
        # if the pixel is the same as the current run, increase the run length
        if pixel == current_run["value"]:
            # if the run length is already at the maximum (15), start a new run
            if current_run["length"] == 15:
                run_counter += 1
                current_run = {"length": 1, "value": pixel}
            else:
                current_run["length"] += 1
        # if the pixel is different from the current run, start a new run
        else:
            run_counter += 1
            current_run = {"length": 1, "value": pixel}

    # return the run counter
    return run_counter

def encode_rle(flat_data):
    if not flat_data:
        return []   # If there is no data, return an empty list.

    rle_data = []   # Create an empty list to store the RLE data.
    current_run = {"value": flat_data[0], "length": 1}   # Initialize a dictionary to keep track of the current run.

    for pixel in flat_data[1:]:
        if pixel == current_run["value"]:
            if current_run["length"] == 15:
                # If the current run is at the maximum length of 15, append the current run to the RLE data and start a new run.
                rle_data.extend([current_run["length"], current_run["value"]])
                current_run = {"value": pixel, "length": 1}
            else:
                # If the current run is not at the maximum length, increment the length of the run.
                current_run["length"] += 1
        else:
            # If the next pixel is different from the current pixel, append the current run to the RLE data and start a new run.
            rle_data.extend([current_run["length"], current_run["value"]])
            current_run = {"value": pixel, "length": 1}

    # Append the final run to the RLE data.
    rle_data.extend([current_run["length"], current_run["value"]])
    return rle_data


def get_decoded_length(rle_data):
    length = 0
    for i in range(len(rle_data)):
        if i % 2 == 0:
            # The even-indexed elements in the RLE data are the lengths of the runs.
            length += rle_data[i]
    return length


def decode_rle(rle_data):
    raw_data = []
    for i in range(0, len(rle_data), 2):
        encoded_length = rle_data[i]
        encoded_data = rle_data[i + 1]
        # Repeat the encoded data by the encoded length to get the raw data.
        raw_data += [encoded_data] * encoded_length
    return raw_data


def string_to_data(data_string):
    return [hex_char_to_decimal(hex_char) for hex_char in data_string]


def to_rle_string(rle_data):
    return ''.join(str(rle_data[i]) + decimal_to_hex(int(rle_data[i+1])).lower() + ':' for i in range(0, len(rle_data), 2))[:-1]




def string_to_rle(rle_string):
    rle_data = []

    chunks = rle_string.split(":")
    for chunk in chunks:
        hex_encoded_data = chunk[-1]
        decimal_length = chunk[:-1]

        rle_data.append(int(decimal_length))
        rle_data.append(hex_char_to_decimal(hex_encoded_data))

    return rle_data


def decimal_to_hex(number):
    if number == 0:
        return "0"

    hex_chars = []
    while number != 0:
        remainder = number % 16

        if remainder < 10:
            hex_chars.append(str(remainder))
        else:
            hex_chars.append(chr(remainder + 55))

        number //= 16

    return "".join(hex_chars[::-1])


def hex_char_to_decimal(hex_char):
    hex_decimal_map = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "A": 10,
        "B": 11,
        "C": 12,
        "D": 13,
        "E": 14,
        "F": 15,
    }

    return hex_decimal_map[hex_char.upper()]

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

    # make sure the input is valid and if its not, it should crash
    if user_input < 0 or user_input > 9:
        error(f"invalid menu input! GOT: {user_input}")

    return user_input


def main():
    current_image = None
    current_image_is_test_image = False

    welcome()
    print("")

    print("Displaying Spectrum Image:")
    ConsoleGfx.display_image(ConsoleGfx.test_rainbow)
    print("")

    while True:
        # Display the menu
        menu()

        # Prompt for input
        user_selection = menu_input()

        # Handle user input
        if user_selection == 0:
            # 0. Exit
            return
        elif user_selection == 1:
            # 1. Load File
            filename = input("Enter name of file to load: ")
            current_image = ConsoleGfx.load_file(filename)
        elif user_selection == 2:
            # 2. Load Test Image
            current_image = ConsoleGfx.test_image
            current_image_is_test_image = True
            print("Test image data loaded.")
        elif user_selection == 3:
            # 3. Read RLE String
            user_input = input("Enter an RLE string to be decoded: ")
            rle_data = string_to_rle(user_input)
            flat_data = decode_rle(rle_data)
            current_image = flat_data
        elif user_selection == 4:
            # 4. Read RLE Hex String
            user_input = input("Enter the hex string holding RLE data: ")
            rle_data = string_to_data(user_input)
            flat_data = decode_rle(rle_data)
            current_image = flat_data
        elif user_selection == 5:
            # 5. Read Data Hex String
            user_input = input("Enter the hex string holding flat data: ")
            flat_data = string_to_data(user_input)
            current_image = flat_data
        elif user_selection == 6:
            # 6. Display Image
            if current_image_is_test_image:
                print("Displaying image...")
            ConsoleGfx.display_image(current_image)
        elif user_selection == 7:
            # 7. Display RLE String
            rle_data = encode_rle(current_image)
            rle_representation = to_rle_string(rle_data)
            print(f"RLE representation: {rle_representation}")
        elif user_selection == 8:
            # 8. Display Hex RLE Data
            rle_data = encode_rle(current_image)
            rle_representation = to_hex_string(rle_data)
            print(f"RLE hex values: {rle_representation}")
        elif user_selection == 9:
            # 9. Display Hex Flat Data
            print(f"Flat hex values: {to_hex_string(current_image)}")



def tests():
    # tests from the comments provided in the pdf
    assert to_hex_string([3, 15, 6, 4]) == "3f64"
    assert count_runs([15, 15, 15, 4, 4, 4, 4, 4, 4]) == 2
    assert encode_rle([15, 15, 15, 4, 4, 4, 4, 4, 4]) == [3, 15, 6, 4]
    assert get_decoded_length([3, 15, 6, 4]) == 9
    assert get_decoded_length([7, 15, 7, 4]) == 14
    assert decode_rle([3, 15, 6, 4]) == [15, 15, 15, 4, 4, 4, 4, 4, 4]
    assert string_to_data("3f64") == [3, 15, 6, 4]
    assert to_rle_string([15, 15, 6, 4]) == "15f:64"
    assert string_to_rle("15f:64") == [15, 15, 6, 4]

    # tests from zybooks
    assert count_runs([1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]) == 25
    assert count_runs(
        [4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         8, 7]) == 6

    assert encode_rle(
        [4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         8, 7]) == [2, 4, 15, 1, 15, 1, 5, 1, 1, 8, 1, 7]
    assert encode_rle([1, 2, 3, 4, 1, 2, 3, 4]) == [1, 1, 1, 2, 1, 3, 1, 4, 1, 1, 1, 2, 1, 3, 1, 4]
    assert encode_rle(
        [4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1]) == [2, 4, 15, 1, 15, 1, 5, 1]
    assert encode_rle(
        [4, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1]) == [1, 4, 1, 5, 15, 1, 15, 1, 5, 1]

    assert decode_rle([2, 4, 15, 1, 15, 1, 5, 1, 1, 8, 1, 7]) == [4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                                                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                                                  1, 8, 7]


    assert decimal_to_hex(0) == "0"
    assert decimal_to_hex(1) == "1"
    assert decimal_to_hex(2) == "2"
    assert decimal_to_hex(3) == "3"
    assert decimal_to_hex(4) == "4"
    assert decimal_to_hex(5) == "5"
    assert decimal_to_hex(6) == "6"
    assert decimal_to_hex(7) == "7"
    assert decimal_to_hex(8) == "8"
    assert decimal_to_hex(9) == "9"
    assert decimal_to_hex(10) == "A"
    assert decimal_to_hex(11) == "B"
    assert decimal_to_hex(12) == "C"
    assert decimal_to_hex(13) == "D"
    assert decimal_to_hex(14) == "E"
    assert decimal_to_hex(15) == "F"
    assert decimal_to_hex(16) == "10"
    assert decimal_to_hex(17) == "11"
    assert decimal_to_hex(18) == "12"
    assert decimal_to_hex(19) == "13"
    assert decimal_to_hex(20) == "14"


if __name__ == "__main__":
    # tests()
    main()
