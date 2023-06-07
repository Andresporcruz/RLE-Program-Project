


# import the ConsoleGfx class
from console_gfx import ConsoleGfx



def to_hex_string(data):
    # TODO is there a difference between RLE or raw?
    # TODO can I assume that every item in data is <=15?
    hex = ""

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

    # map over every item, converting the decimal to hex
    for item in data:
        hex += decimal_hex_map[item]

    # example wants lowercase so that is what we return
    return hex.lower()



def count_runs(flat_data):
    if len(flat_data) == 0:
        return []

    # first run is created with the first pixel's value
    current_run = {"length": 1, "value": flat_data[0]}
    run_counter = 0

    for pixel in flat_data[1:]:
        # if this pixel is part of the current run OR this is the first iteration
        if pixel == current_run["value"]:
            # is the run full?
            if current_run["length"] == 15:
                # if so, increment run counter
                run_counter += 1
                # initilize new run with pixel
                current_run = {"length": 1, "value": pixel}
            else:
                # if not, then we can just
                # increase the length of the run
                current_run["length"] += 1
        # pixel marks the end of the current run
        else:
            # increment run counter
            run_counter += 1
            # initilize new run with pixel
            current_run = {"length": 1, "value": pixel}

    # the last run is not counted so I increment the run_counter here
    # to compensate
    run_counter += 1

    return run_counter


def encode_rle(flat_data):
    # if flat_data is empty, return an empty list
    if len(flat_data) == 0:
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


def get_decoded_length(rle_data):
    return sum(rle_data[::2])


def decode_rle(rle_data):
    raw_data = []


    for encoded_length_index in range(0, len(rle_data), 2):
        encoded_length = rle_data[encoded_length_index]
        encoded_data = rle_data[encoded_length_index + 1]


        for _ in range(encoded_length):
            raw_data.append(encoded_data)

    return raw_data


def string_to_data(data_string):
    raw_data = []
    for hex_char in data_string:
        raw_data.append(hex_char_to_decimal(hex_char))

    return raw_data


def to_rle_string(rle_data):
    readable_str = ""

    for i in range(0, len(rle_data), 2):
        run_length = rle_data[i]
        encoded_data = rle_data[i + 1]


        readable_str += str(run_length)


        readable_str += decimal_to_hex(int(encoded_data)).lower()


        readable_str += ":"


    return readable_str[:-1]



def string_to_rle(rle_string):
    rle_data = []


    for chunk in rle_string.split(":"):
        hex_encoded_data = chunk[-1]
        decimal_length = chunk[:-1]

        # append the length
        rle_data.append(int(decimal_length))


        rle_data.append(hex_char_to_decimal(hex_encoded_data))

    return rle_data



def decimal_to_hex(number):

    if number == 0: return "0"

    hex = ""

    while number != 0:
        remainder = number % 16

        if remainder < 10:

            hex += chr(remainder + 48)
        else:

            hex += chr(remainder + 55)

        number //= 16

    return hex[::-1]


def hex_char_to_decimal(hex_char):
    if len(hex_char) != 1:
        error(f"hex char should only have length 1, got {hex_char}")

    hex_char = hex_char.upper()

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

    # asssumes that the hex_char is valid
    return hex_decimal_map[hex_char]


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
        # TODO should this loop?
        user_selection = menu_input()

        # 0. Exit
        if user_selection == 0:
            return

        # 1. Load File 
        elif user_selection == 1:
            # get the filename from the user
            filename = input("Enter name of file to load: ")

            # load the file
            current_image = ConsoleGfx.load_file(filename)

        # 2. Load Test Image 
        elif user_selection == 2:
            current_image = ConsoleGfx.test_image
            current_image_is_test_image = True
            print("Test image data loaded.")

        # 3. Read RLE String
        elif user_selection == 3:
            user_input = input("Enter an RLE string to be decoded: ")

            # list of numbers [length, encoded, length, encoded, etc.]
            rle_data = string_to_rle(user_input)


            flat_data = decode_rle(rle_data)

            # store as image
            current_image = flat_data

        # 4. Read RLE Hex String
        elif user_selection == 4:
            user_input = input("Enter the hex string holding RLE data: ")

            # list of numbers [length, encoded, length, encoded, etc.]
            rle_data = string_to_data(user_input)


            flat_data = decode_rle(rle_data)

            # store as image
            current_image = flat_data

        # 5. Read Data Hex String
        elif user_selection == 5:
            user_input = input("Enter the hex string holding flat data: ")

            flat_data = string_to_data(user_input)

            # store as image
            current_image = flat_data

        # 6. Display Image 
        elif user_selection == 6:

            if current_image_is_test_image:
                print("Displaying image...")

            ConsoleGfx.display_image(current_image)

        # 7. Display RLE String
        elif user_selection == 7:
            rle_data = encode_rle(current_image)

            rle_representation = to_rle_string(rle_data)

            print(f"RLE representation: {rle_representation}")

        # 8. Display Hex RLE Data
        elif user_selection == 8:
            # list of numbers [length, encoded, etc.]
            rle_data = encode_rle(current_image)

            rle_representation = to_hex_string(rle_data)

            print(f"RLE hex values: {rle_representation}")

        # 9. Display Hex Flat Data
        elif user_selection == 9:
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

    # tests from me!
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
