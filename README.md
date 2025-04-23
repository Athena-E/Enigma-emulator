# Enigma Machine Emulator (Enigma M3 with UKW-B Reflector)

This is a Pygame-based emulator of the Enigma M3 series, a variant of the famous Enigma cipher machine used extensively by the German Navy (Kriegsmarine) during World War II. This particular emulator accurately models the M3's three-rotor system (chosen from a set of five) and incorporates the UKW-B reflector.

## Key Features

* **Accurate Enigma M3 Simulation:** Faithfully recreates the electromechanical operation of the Enigma M3 machine.
* **Three Rotors (Selectable from Five):** Implements a set of five distinct rotors, allowing the user to choose any three and set their initial positions and ring settings, mirroring the real M3.
* **UKW-B Reflector:** Includes the "Umkehrwalze B" (Reflector B), a crucial component for the Enigma's reciprocal encryption.
* **Plugboard (Steckerbrett):** Fully functional plugboard allowing users to define pairs of letters to be swapped before and after the rotor scrambling process.
* **Monthly Keysheet Integration:** Designed to utilize monthly keysheets for realistic setup. Users can input or load configurations based on historical keysheets (like the provided [monthly keysheet](https://artsandculture.google.com/asset/enigma-setting-sheet/EAGejYOkpCao8Q?hl=en)).
* **Pygame Interface:** Provides a user-friendly graphical interface for interacting with the virtual Enigma machine. This likely includes:
    * A visual representation of the rotors and their current positions.
    * A virtual keyboard for input and output.
    * Clear indication of the plugboard settings.
* **Step-by-Step Operation Visualization (Optional Enhancement):** [Consider adding this if implemented] Visual feedback on how each rotor steps during encryption/decryption.

## Main Components

The Enigma machine's security stemmed from the intricate interplay of its components:

* **Rotors (Walzen):** These are the heart of the Enigma.
    * **Wiring:** Each rotor internally substitutes one letter of the alphabet for another according to a fixed, complex wiring.
    * **Stepping Mechanism:** After each keypress (or encryption/decryption of a letter), the rightmost rotor advances one position. The other rotors also step, but less frequently, driven by notches on the rotors and a pawl mechanism.
    * **Ring Settings (Ringstellung):** The alphabet ring on each rotor can be rotated independently of the internal wiring, effectively adding another layer of complexity to the substitution.
    * **Rotor Order (Walzenlage):** The order in which the chosen three rotors are placed in the machine significantly affects the encryption. The M3 allowed for any permutation of the selected three rotors.
    * **Rotor Set:** The M3 used by the Kriegsmarine had a set of **five** rotors (typically numbered I to V), from which three were chosen for operation.
* **Reflector (Umkehrwalze - UKW):** Located at the left end of the rotor assembly, the reflector does not rotate.
    * **Wiring:** It connects pairs of letters. When a signal passes through the rotors, it reaches the reflector, which reverses the signal back through the rotors along a different path.
    * **UKW-B:** The UKW-B had a specific, fixed wiring. The fact that the reflector paired letters meant that a letter could never be encrypted to itself.
* **Plugboard (Steckerbrett):** Situated at the front of the machine, the plugboard allowed for up to ten pairs of letters to be swapped before the signal entered the rotors and after it exited.
    * **Effect:** This seemingly simple component drastically increased the number of possible encryption configurations.

## Usage

1.  **Installation:**
    ```bash
    pip install pygame # If you don't have Pygame installed
    git clone https://github.com/Athena-E/Enigma-emulator.git
    cd Enigma-emulator
    python enigma_sim.py # Or the name of your main script
    ```
2.  **Configuration:**
    * **Rotor Selection:** The application should allow you to choose three rotors from the set of five (I, II, III, IV, V) and specify their order.
    * **Initial Rotor Positions (Grundstellung):** Set the starting letter for each of the three rotors.
    * **Ring Settings (Ringstellung):** Configure the ring setting for each of the three rotors (typically a number from 01 to 26, corresponding to letters A to Z).
    * **Plugboard Settings (Steckerverbindungen):** Define the pairs of letters to be connected on the plugboard (e.g., AB CD EF).
    * **Reflector:** The emulator is fixed to the UKW-B reflector.
3.  **Encryption/Decryption:**
    * Type the message using the virtual keyboard.
    * The emulator will display the encrypted (or decrypted) output in real-time.
  
## Potential Future Enhancements

* **M4 Emulator:** Extend the emulator to include the fourth rotor functionality of the Enigma M4.
* **Different Reflectors:** Allow the user to select other Enigma reflectors (e.g., UKW-C).
* **Keysheet Loading:** Implement functionality to load and parse Enigma keysheet files.
* **Visual Stepping Animation:** Animate the rotor movements during encryption/decryption.
* **Saving/Loading Configurations:** Allow users to save and load their Enigma machine configurations.
* **More Detailed Documentation:** Add comments to the code and more in-depth explanations of the Enigma's operation.
