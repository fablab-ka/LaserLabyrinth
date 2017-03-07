/*
 * common.h
 *
 *  Created on: Dec 26, 2014
 *  Author: Mark Weinreuter
 */
#ifndef UTIL_H
#define UTIL_H

#if defined(__AVR_ATmega48__) || defined(__AVR_ATmega88__) || defined(__AVR_ATmega168__) || \
    defined(__AVR_ATmega48P__) || defined(__AVR_ATmega88P__) || defined(__AVR_ATmega168P__)|| defined(__AVR_ATmega328P__) || \
    defined(__AVR_ATtiny85__) ||     defined(__AVR_ATtiny45__)


#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>


//define a byte :D
typedef uint8_t byte;

typedef unsigned int uint;

//define a pointer to register
typedef volatile uint8_t *regPtr;

// define boolean values to indicate true and false only
typedef enum bool {
    false = 0, true = 1
} bool;


#define is_digit(c)            (( (c) >='0') && ( (c) <= '9'))
#define is_lowercase(c)        (( (c) >='a') && ( (c) <= 'z'))
#define is_uppercase(c)        (( (c) >='A') && ( (c) <= 'Z'))




//some macros for bit operations
#define bit(pos)                            (1 << pos)
#define bit2(pos1, pos2)                    ( bit(pos1) | bit(pos2) )
#define bit3(pos1, pos2, pos3)              ( bit(pos1) | bit(pos2) | bit(pos3) )
#define bit4(pos1, pos2, pos3, pos4)        ( bit(pos1) | bit(pos2) | bit(pos3) | bit(pos4) )
#define bit5(pos1, pos2, pos3, pos4, pos5)  ( bit(pos1) | bit(pos2) | bit(pos3) | bit(pos4) | bit(pos5))


#define setValue(x, y)                  (x |= y)
#define setBit(x, pos)                  (x |= bit(pos))

#define clearValue(x, y)                (x &= ~y)
#define clearBit(x, pos)                (x &= ~bit(pos))

#define toggleBit(x, pos)               ((x) ^= bit(pos))
#define toggleValue(x, value)           (x ^= value)


#if !(defined(__AVR_ATtiny85__) ||     defined(__AVR_ATtiny45__))

#define setAsOutputCValue(x)            (DDRC |= (x))
#define setAsOutputCBit(pos)            (DDRC |= bit(pos))

#define setAsInputCValue(x)             (DDRC &= ~(x))
#define setAsInputCBit(pos)             (DDRC &= ~bit(pos))


#define portC_setBit(pos)               (PORTC |= bit(pos))
#define portC_clearBit(pos)             (PORTC &= ~bit(pos))

#define portC_getBit(pos)               ((PINC &bit(pos))>>pos)

#define setAsOutputDValue(x)            (DDRD |= (x))
#define setAsOutputDBit(pos)            (DDRD |= bit(pos))

#define setAsInputDValue(x)             (DDRD &= ~(x))
#define setAsInputDBit(pos)             (DDRD &= ~bit(pos))


#define portD_setBit(pos)               (PORTD |= bit(pos))
#define portD_clearBit(pos)             (PORTD &= ~bit(pos))
#define portD_getBit(pos)               ((PIND &bit(pos))>>pos)


#endif

#define setAsOutputBValue(x)            (DDRB |= (x))
#define setAsOutputBBit(pos)            (DDRB |= bit(pos))

#define setAsInputBValue(x)             (DDRB &= ~(x))
#define setAsInputBBit(pos)             (DDRB &= ~bit(pos))

#define portB_setBit(pos)               (PORTB |= bit(pos))
#define portB_clearBit(pos)             (PORTB &= ~bit(pos))
#define portB_toggleBit(pos)            (PORTB ^= bit(pos))

#define pinB_isSet(pos)                 ((PINB & bit(pos))==bit(pos))
#define portB_getBit(pos)               ((PINB &bit(pos))>>pos)

#define enableInterrupts()              sei()
#define disableInterrupts()             cli()

#define delay(ms)                       _delay_ms(ms)


#else
#error Chip is not supported!
#endif

#define _STR(x) #x
#define STR(x) _STR(x)

#endif //UTIL_H
