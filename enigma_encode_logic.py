"""
Settings:
rotor order 
ring setting 
rotor starting positions 
plugboard connections

Process:
key switch -> plugboard -> rotors -> plugboard -> light
"""

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


rotor_wirings = {
    1: "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    2: "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    3: "BDFHJLCPRTXVZNYEIWGAKMUSQO",
    4: "ESOVPZJAYQUIRHXLNFTGKDCMWB",
    5: "VZBRGITYUPSDNHLXAWMJQOFECK"
}


rotor_notches = {1: "Q", 2: "E", 3: "V", 4: "J", 5: "Z"}


UKW_B_wiring = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
UKW_C_wiring = "FVPJIAOYEDRZXWGCTKUQSBNMHL"

# plugboard settings
plugboard_dict = {}
plugboard_settings =[
    "KT", "AJ", "IV", "UR", "NY", 
    "HZ", "GD", "XF", "PB", "CQ"
] 

for letter_pair in plugboard_settings:
    letter1 = letter_pair[0]
    letter2 = letter_pair[1]
    plugboard_dict[letter1] = letter2
    plugboard_dict[letter2] = letter1


class Keyboard:
    
    def get_letter_pos(self, letter):
        letter_pos = alphabet.find(letter)
        return letter_pos


class Reflector:

    def __init__(self, wiring):
        self.wiring = wiring

    def switch_letter(self, letter):
        new_letter = self.wiring[alphabet.find(letter)]
        return new_letter


class Rotor:

    def __init__(self, start_pos, ring_setting, wiring):
        self.offset = start_pos
        self.ring_setting = ring_setting
        self.wiring = wiring
        if start_pos != ring_setting:
            self.new_wiring = self.get_new_wiring()
        else:
            self.new_wiring = wiring

    def update(self):
        asc_pos = ord(self.offset)+1
        if asc_pos > 90:
            diff = asc_pos-90
            asc_pos = 64+diff
        self.offset = chr(asc_pos)
        self.new_wiring = self.get_new_wiring()

    def letters_forwards(self, places):
        # moves each letter forwards
        shifted_letters = ""
        for i in range(26):
            asc_pos = ord(self.wiring[i]) + places
            if asc_pos > 90:
                diff = asc_pos - 90
                asc_pos = 64+diff
            shifted_letters += chr(asc_pos)
        
        return shifted_letters
            
    def alphabet_forwards(self, shifted_letters, places):
        # shifts whole alphabet forwards
        split_1 = shifted_letters[:26-places]
        split_2 = shifted_letters[26-places:]
        shifted_alphabet = split_2+split_1

        return shifted_alphabet

    def get_new_wiring(self):
        # generates substitution alphabet accoridng to ring setting and start position
        offset_asc = ord(self.offset)
        ring_setting_asc = ord(self.ring_setting)
        if ring_setting_asc > offset_asc:
            places = ring_setting_asc-offset_asc
        else:
            places = 26 - (offset_asc-ring_setting_asc)

        shifted_letters = self.letters_forwards(places)
        new_wiring = self.alphabet_forwards(shifted_letters, places)
        
        return new_wiring

    def map_letter_forwards(self, plain_letter):
        # maps letter in alphabet to letter in subsitution alphabet
        pos = alphabet.find(plain_letter)
        encrypted_letter = self.new_wiring[pos]

        return encrypted_letter

    def map_letter_backwards(self, input_letter):
        # maps letter in substitution alphabet to letter in alphabet
        pos = self.new_wiring.find(input_letter)
        encrypted_letter = alphabet[pos]

        return encrypted_letter


def check_plugboard(plugboard_dict, input_letter):
    if input_letter in plugboard_dict:
        output_letter = plugboard_dict[input_letter]
    else:
        output_letter = input_letter
    
    return output_letter



def rotor_encrypt(r1, r2, r3, reflector, input_letter, plugboard_dict):
    # full encryption plugboard -> rotors -> reflector -> rotors -> plugboard
    output_letter = check_plugboard(plugboard_dict, input_letter)
    output_letter = r3.map_letter_forwards(output_letter)
    output_letter = r2.map_letter_forwards(output_letter)
    output_letter = r1.map_letter_forwards(output_letter)

    output_letter = reflector.switch_letter(output_letter)

    output_letter = r1.map_letter_backwards(output_letter)
    output_letter = r2.map_letter_backwards(output_letter)
    output_letter = r3.map_letter_backwards(output_letter)

    output_letter = check_plugboard(plugboard_dict, output_letter)

    return output_letter

# rotors turnover and then encrypt
def turn_rotors(rotor_order, rotor_notches, r3, r2, r1):
    if r3.offset == rotor_notches[rotor_order[2]]:
        # if rotor 3 and rotor 2 turnover reached, turn rotor 1 first then turn rotor 2
        if r2.offset == rotor_notches[rotor_order[1]]:
            r1.update()
        r2.update()


# rotor order settings
rotor_order = [3,2,1]

# rotor starting position and ring setting
r3 = Rotor("Q", "A", rotor_wirings[rotor_order[2]])
r2 = Rotor("A", "A", rotor_wirings[rotor_order[1]])
r1 = Rotor("A", "A", rotor_wirings[rotor_order[0]])
reflector = Reflector(UKW_B_wiring)


# loop input letters one at a time

if __name__ == "__main__":
    while True:
        input_letter = input("Enter letter: ")

        if input_letter != "": 
            turn_rotors(rotor_order, rotor_notches, r3, r2, r1)
            r3.update()
            output_letter = rotor_encrypt(r1, r2, r3, reflector, input_letter, plugboard_dict)
            print(output_letter)
        else:
            break




