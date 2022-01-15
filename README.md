# ATmega-Music-Automation
Firmware for the ATmega 328p that allows you to play progammable music with a piezo buzzer

## Goal
The goal of this lab assignment was to generate music using piezo buzzers and bare-bones C++ (no arduino libraries)

## Implementation
The firmware is relatively straightforward:
- Configure a built-in 8-bit timer to count milliseconds
- Configure a built-in 16-bit timer to generate a square wave to send to the buzzer to make note frequencies
- Iterate through two arrays
  - One array holds timing information, telling the program when to move to the next array element
  - The other array holds Compare Match Values for the 16-bit timer. This array changes the note being played

To stop sound for rests, indicated by 0 in the note array, and to allow for the same note to be played multiple times in a row, the program disconnects the square wave output at the end of each note for a few milliseconds, only re-enabling the output at the next non-0 note.

## Python automation
The firmware is simple to code, but it comes with a drawback: it relies on specifically formatted arrays to load onto the microcontroller.

To overcome this issue, and make it easy to program multiple different songs, I wrote a python program that translates from an easy-to-write text file to the specific C++ arrays for the firmware. The ultimate goal was to make it easy to transcribe sheet music into this system.

### Input
First, create a .txt file.
The very first line must be an integer that specifies the BPM
Subsequent lines can be empty, contain a comment, or contain note information. Whitespace and comments make it easy to organize the text file for future reference.

Note information should be formatted like ```[Note] [Number_of_Beats]```

```[Note]``` should be a note's name, an optional sharp, and the octave

  e.g. E4, Fs3, c#5, DS4, X, REST
  
  The note is not case sensitive, and sharps can be denoted by ```'s'``` or ```'#'```
  
  ```X``` and ```REST``` denote a rest / pause in the music
  
  This program, due to the 16-bit timer, supports octaves 3 - 8
  
  
  ```[Number_of_Beats]``` should be a floating point number indicating how long to hold the note.
  
  The note and its timing should be on the same line, separated by a space.
  
  
Once you have your text file, use MusicTranslator.py
- Replace ```song_file = "Tetris.txt"``` with ```song_file = "[your_text_file]"```
- Run MusicTranslator.py
- The results will show up in a new file in the same directory. Copy the array definitions from this text file into the C++ firmware


### Output
  The translator will create a text file with C++ array and variable declarations. Copy these over the existing declarations in the firmware, then upload the firmware to the board. If the circuit for the ATmega328p is setup correctly [(see the header in the firmware)](Lab06_Music_Box.ino), the board should now be playing your song!
  

## Example translation
Input file: Tetris.txt
```
130

// Beginning of song
E5 1
B4 .5
C5 .5
D5 1
C5 .5
B4 .5

A4 1
A4 .5
C5 .5
E5 1
D5 .5
C5 .5

B4 1.5
C5 .5
D5 1
E5 1
C5 1
A4 1
A4 1
X 1
... (rest of file not shown)
```

Output file: Tetris_arrays2.txt
```
const uint16_t notes[] = {12134, 16198, 15289, 13620, 15289, 16198, 18181, 18181, 15289, 12134, 13620, 15289, 16198, 15289, 13620, 12134, 15289, 18181, 18181, 0, 0, 13620, 11453, 9090, 10204, 11453, 12134, 15289, 12134, 13620, 15289, 16198, 15289, 13620, 12134, 15289, 18181, 18181, 0, 12134, 15289, 13620, 16198, 15289, 18181, 19263, 12134, 15289, 13620, 16198, 15289, 12134, 9090, 9090, 9631};
const int timing_ms[] = {462, 231, 231, 462, 231, 231, 462, 231, 231, 462, 231, 231, 692, 231, 462, 462, 462, 462, 462, 462, 231, 462, 231, 462, 231, 231, 692, 231, 462, 231, 231, 692, 231, 462, 462, 462, 462, 462, 462, 923, 923, 923, 923, 923, 923, 1846, 923, 923, 923, 923, 462, 462, 462, 462, 1846};
int last_note = 55;
```

## Video Exmample


https://youtu.be/GVEnl32yGfY

Video of the circuit playing "Attack of the Killer Queen," a song by Toby Fox, Lena Raine, and Marcy Nabors.

This tune has 451 notes, which was only reasonable to program thanks to the python music translator.




## Limitations
The biggest drawback to this approach is the need to store every note with an integer and a 16-bit integer, which takes up a lot of space. It would probably be better to store each 16-bit value for the notes once as a constant, and use an 8-bit number to represent which note to select.
