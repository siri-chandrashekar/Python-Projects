morse_dict = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ",": "--..--",
    ".": ".-.-.-",
    "?": "..--..",
    "/": "-..-.",
    "-": "-....-",
    "(": "-.--.",
    ")": "-.--.-",
    " ": "/",
}


def text_to_morse(text):
    result = []
    for letter in text.upper():
        if letter in morse_dict:
            result.append(morse_dict[letter])
        else:
            result.append("?")
    return " ".join(result)


def main():
    while True:
        msg = input("Enter a message to be morse coded: ")
        print("Here is your morse code\n" + text_to_morse(msg))

        choice = input("Do you want to continue? (yes/no): ").lower()
        if choice == "no":
            break
        if choice == "yes":
            continue

        print("Invalid input, exiting...")
        break


if __name__ == "__main__":
    main()
