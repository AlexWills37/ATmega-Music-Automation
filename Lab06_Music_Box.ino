/**
 * Lab06 Hal 9000 Sings the Blues
 * The goal of this lab is to program the circuit with a piezo buzzer to play a song
 * 
 * CODE
 * Uses Timer 0 to count milliseconds and Timer 1 to generate freqeuncy for notes.
 * Timer 1 continuously outputs a frequency matching a musical note.
 * Timer 0 generates an interrupt every millisecond, changing the frequency of Timer 1 to the next note after the current
 * note has played its entire duration.
 * 
 * 
 * CIRCUIT
 * Piezo buzzer wired from Pin OC1A (PB1 / IO9) to ground. An optional in-series resistor can be added to lower the Piezo's volume
 * 
 * Extra Functionality
 * This program comes with MusicTranslator.py, a python program to (relatively) easily generate the arrays for global memory for different songs
 * 
 * @author Alex Wills
 * @date 28 September 2021
 */

// Arrays for notes and timings
// For each index i in the arrays, notes[i] is the Compare Match value to generate the correct note
// and timing_ms[i] is the number of ms to hold the note for
// Arrays can be made with MusicTranslator.py


#include <stdint.h>

const uint16_t notes[] = {15289, 18181, 22907, 30577, 27242, 24269, 22907, 27242, 22907, 30577, 27242, 17161, 18181, 22907, 27242, 24269, 22907, 20408, 18181, 20408, 18181, 17161, 18181, 20408, 15289, 18181, 20408, 22907, 20408, 18181, 22907, 27242, 22907, 27242, 30577, 30577, 22907, 18181, 20408, 0, 22907, 18181, 20408, 18181, 17161, 15289, 18181, 22907, 20408, 30577};
const int timing_ms[] = {1324, 1324, 1324, 1324, 441, 441, 441, 882, 441, 2647, 1324, 1324, 1324, 1324, 441, 441, 441, 882, 441, 2206, 441, 441, 441, 441, 882, 441, 441, 1765, 441, 882, 441, 882, 441, 441, 1765, 441, 882, 441, 441, 882, 882, 441, 441, 441, 441, 441, 441, 441, 882, 441};
int last_note = 50;


int note = 0;               // Index variable to track the current note
int duration = 0;           // To keep track of duration for each note
int end_pause = 15;        // The duration to cut off each note

/**
 * ISR to count milliseconds with timer 0.
 * Disables Timer 1's output mode at the end of each note to distinguish notes, then progresses the song
 * to the next note once the note's duration is over.
 */
ISR(TIMER0_COMPA_vect){
  // Progress as ms in the song
  duration += 1;

  // Cut off notes early
  if(duration >= timing_ms[note] - end_pause){
    TCCR1A &= ~(1 << 6);

    // At end of note, progress the song
    if(duration >= timing_ms[note]){
      note += 1;

      // Loop song at end
      if(note >= last_note){
        note = 0;
      }

      // For rests, do not turn the sound back on
      if(notes[note] != 0){
        OCR1A = notes[note] - 1;
        TCCR1A |= (1 << 6);
      }

      duration = 0;
    } // If(end of note)
    
  } // If(almost end of note)
  
}

/**
 * Main function to configure registers and infinitely loop, waiting for interrupts
 */
int main(){

  DDRB |= (1 << 1);

  // Setup Timer 1 to generate sounds
  TCCR1A = 0b01000000;  // Set WGM1 bits for CTC [1:0] = 00. Set OC1A (PB1, IO9 for toggle. Do &= ~(1 << 6) to disable toggle, do |= (1 << 6) to enable toggle
  OCR1A = notes[note] - 1;  // Set the compare match to the first note

  // Setup Timer 0 to count milliseconds
  TCCR0A = 0b00000010;  // Set WGM0 bits for CTC [1:0] = 10
  TIMSK0 = 0b00000010;  // Enable interrupts for COMP1A
  OCR0A = 250;          // Set COMP1A. Occurs every millisecond with prescale of 64

  // Enable interrupts and start the counters
  SREG |= (1<<7);       // Enable global interrupts
  TCCR1B = 0b00001001;  // Set WGM1 bits for CTC [3:2] = 01. Set clock prescale to 1
  TCCR0B = 0b00000011;  // Set WGM0 bits for CTC [2] = 0. Set clock prescale to 64


  while(true){
    
  }

  return 0;
}
