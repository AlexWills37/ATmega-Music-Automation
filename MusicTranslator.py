# Alex Wills
# 26 September 2021
# 
# MusicTranslator.py
#
# Allows user to input musical information (note, duration) to translate into the arrays needed for
# to load into system memory for the Embedded Systems Lab06 Hal 9000 Sings the Blues
#
# Made with the goal of easily playing other songs using the metro mini, without needing
# to store a complex translator in the system's memory
#
# Future project idea: Write this translator in C++ to better interface with the metro mini
#
# Credits:
#   Intermediate Python projects 
#   https://www.geeksforgeeks.org/writing-to-file-in-python/
#   


def main():
    # music = open("song_arrays.txt", 'w')
    # make_compare_dictionary(1)
    
    song_file = "Tetris.txt"
    array_file = song_file[0:(song_file.find("."))] + "_arrays2.txt"

    inFile = open(song_file, 'r')
    outFile = open(array_file, "w")
    build_music_by_file(inFile, outFile)
    inFile.close()
    outFile.close()
    
    
    '''for key in note_to_frequency:
        print(note_to_frequency[key], end=", ")
    print()
    print(note_to_frequency)
    '''

    


prescale = 1
clock = 16000000


# Compare Match values for clock prescale of 1
note_to_compare = {
    "REST" : 0, "X" : 0,   
    "B2" : 64793,
    "C3" : 61157, "C#3" : 57724, "D3" : 54484, "D#3" : 51427, "E3" : 48534, "F3" : 45816, "F#3" : 43243, "G3" : 40816, "G#3" : 38526, "A3" : 36363, "A#3" : 34322, "B3" : 32396,
    "C4" : 30577, "C#4" : 28862, "D4" : 27242, "D#4" : 25712, "E4" : 24269, "F4" : 22907, "F#4" : 21622, "G4" : 20408, "G#4" : 19263, "A4" : 18181, "A#4" : 17161, "B4" : 16198,
    "C5" : 15289, "C#5" : 14430, "D5" : 13620, "D#5" : 12856, "E5" : 12134, "F5" : 11453, "F#5" : 10810, "G5" : 10204, "G#5" : 9631, "A5" : 9090, "A#5" : 8580, "B5" : 8099,
    "C6" : 7644, "C#6" : 7215, "D6" : 6810, "D#6" : 6428, "E6" : 6067, "F6" : 5726, "F#6" : 5405, "G6" : 5102, "G#6" : 4815, "A6" : 4545, "A#6" : 4290, "B6" : 4049,
    "C7" : 3822, "C#7" : 3607, "D7" : 3405, "D#7" : 3214, "E7" : 3033, "F7" : 2863, "F#7" : 2702, "G7" : 2551, "G#7" : 2407, "A7" : 2272, "A#7" : 2145, "B7" : 2024,
    "C8" : 1911, "C#8" : 1803, "D8" : 1702, "D#8" : 1607, "E8" : 1516, "F8" : 1431, "F#8" : 1351, "G8" : 1275, "G#8" : 1203, "A8" : 1136, "A#8" : 1072, "B8" : 1012,
}








def note_time(bpm, beats):
    ''' returns the amount of time the note should be held (excluding the pause at the end) (ms)
    bpm - int - the bpm of the song
    beats - float - the number of beats for the note
    
    return - time (ms) for the note '''
    
    return (60000 * beats) / (bpm)


def build_music_by_file(inFile, outFile):
    ''' Uses a file to build the arrays for notes and delays.\n
    First line of the file should have the BPM\n
    The file should have a different note on each line.\n
    Each line should contain the note, octave, and number of beats\n
    \te.g. C#5 1.5\n
    Octaves can only go from 0 to 8, and only sharps and naturals should be used\n
    For flats, use the sharp above it'''

    comp_array = []
    time_array = []

    line = inFile.readline()
    bpm = float(line.strip())

    for line in inFile:
        line = line.strip()

        # Skip empty lines and lines that begin with '/' (comments)
        if not (line == "" or line[0] == "/"):

            # note[0] is the note, note[1] is the number of beats
            note = line.capitalize().replace("s", "#").split(" ")


            
            # TODO: add code to trasnlate a flat to a sharp

            # Add note to lists
            comp_array.append(note_to_compare[note[0]])
            time_array.append(  int(note_time(bpm, float(note[1])) + 0.5))


    # Now print arrays to text file

    # Build the array in string format
    outString = "const uint16_t notes[] = {"
    for compare in comp_array:
        outString = outString + str(compare) + ", "
    outString = outString[0:-2] + "};\n"
    outFile.write(outString)

    outString = "const int timing_ms[] = {"
    for time in time_array:
        outString += str(time) + ", "
    outString = outString[0:-2] + "};\n"
    outFile.write(outString)

    outFile.write("int last_note = " + str(len(comp_array)) + ";")








# Helper dictionary for the program
note_to_frequency = {
    "C0" : 16.35, "C#0" : 17.32,"D0" : 18.35, "D#0" : 19.45, "E0" : 20.60, "F0" : 21.83,             "F#0" : 23.12, "G0" : 24.50, "G#0" : 25.96, "A0" : 27.50, "A#0" : 29.14, "B0" : 30.87, 
    "C1" : 32.70, "C#1" : 34.65, "D1" : 36.71, "D#1" : 38.89, "E1" : 41.20, "F1" : 43.65,            "F#1" : 46.25, "G1" : 49.00, "G#1" : 51.91, "A1" : 55.00, "A#1" : 58.27, "B1" : 61.74, 
    "C2" : 65.41, "C#2" : 69.30, "D2" : 73.42, "D#2" : 77.78, "E2" : 82.41, "F2" : 87.31,            "F#2" : 92.50, "G2" : 98.00, "G#2" : 103.83, "A2" : 110.00, "A#2" : 116.54, "B2" : 123.47, 
    "C3" : 130.81, "C#3" : 138.59, "D3" : 146.83, "D#3" : 155.56, "E3" : 164.83, "F3" : 174.61,      "F#3" : 185.00, "G3" : 196.00, "G#3" : 207.65, "A3" : 220.00, "A#3" : 233.08, "B3" : 246.94, 
    "C4" : 261.63, "C#4" : 277.18, "D4" : 293.66, "D#4" : 311.13, "E4" : 329.63, "F4" : 349.23,      "F#4" : 369.99, "G4" : 392.00, "G#4" : 415.30, "A4" : 440.00, "A#4" : 466.16, "B4" : 493.88, 
    "C5" : 523.25, "C#5" : 554.37, "D5" : 587.33, "D#5" : 622.25, "E5" : 659.26, "F5" : 698.46,     "F#5" : 739.99, "G5" : 783.99, "G#5" : 830.61, "A5" : 880.00, "A#5" : 932.33, "B5" : 987.77, 
    "C6" : 1046.50, "C#6" : 1108.73, "D6" : 1174.66, "D#6" : 1244.51, "E6" : 1318.51, "F6" : 1396.91, "F#6" : 1479.98, "G6" : 1567.98, "G#6" : 1661.22, "A6" : 1760.00, "A#6" : 1864.66, "B6" : 1975.53, 
    "C7" : 2093.00, "C#7" : 2217.46,  "D7" : 2349.32, "D#7" : 2489.02, "E7" : 2637.02, "F7" : 2793.83, "F#7" : 2959.96, "G7" : 3135.96, "G#7" : 3322.44, "A7" : 3520.00, "A#7" : 3729.31, "B7" : 3951.07,
    "C8" : 4186.01, "C#8" : 4434.92,  "D8" : 4698.64, "D#8" : 4978.03, "E8" : 5274.04, "F8" : 5587.65, "F#8" : 5919.91, "G8" : 6271.93, "G#8" : 6644.88, "A8" : 7040.00, "A#8" : 7458.62, "B8" : 7902.13
}


# Helper functions for creating the program

def calc_comp_match(frequency, prescale):
    ''' Calculates the compare match value for a note's frequency '''
    return clock / (frequency * 2 * prescale)

def testPrescale(prescale):
    ''' Prints out all of the compare match values '''
    for key in note_to_frequency:
        print(key, calc_comp_match(note_to_frequency[key], prescale))


def make_compare_dictionary(prescale):
    ''' Formates a dictionary to copy/paste from terminal into code for compare match values '''
    i = 0
    string = ""
    for key in note_to_frequency:
        
        string += "\"{}\" : {:.0f}, ".format(key, calc_comp_match(note_to_frequency[key], prescale) + 0.5 - 1) # Round to the nearest number, and subtract 1 because COMP starts at 0
        i += 1

        if i >= 12:
            i = 0
            string += "\n"
    
    print(string)

def make_note_to_freq_dict():
    '''
    Builds the dictionary for the frequency of each note according to the formula
    f(n) = f(0) * a**(n)
    where f(n) is the note n-half-steps away from f(0),
        f(0) is a the frequency of a starting note for the dictionary,
        n is the number of half-steps away from f(0) desired, and
        a = 2**(1/12)'''
    print("Dictionary:\n")

    note_to_n = {       # Dictionary to go from letter notes to half steps away from C
        "C":0, "C#":1, "D":2,
        "D#":3, "E":4, "F":5,
        "F#":6, "G":7, "G#":8,
        "A":9, "A#":10, "B":11
    }

    key = ""    # Key for the note name for the final dictionary
    value = 0   # Value for the frequency of the note

    for octave in range(8):
        for note in note_to_n:
            key = "{0}{1}".format(note, octave)
            n = (12 * octave) + note_to_n[note] # half steps away from c0
            #b8 = 107 half steps away from c0
            n = n - 107 # half steps below b8
            value = 7902.13 * (2**(n/12))
            
            pair = "\"{}\" : {:.2f},".format(key, value)
            print(pair)



if __name__ == "__main__":
    main()