#ifndef TIMER_tX5_H
#define TIMER_tX5_H

/*
 *
 *  NOTE THERE IS A HARDWARE BUG ON OC1B:
 *
 *  Timer Counter 1 PWM output generation on OC1B – XOC1B does not work correctly
 *  Timer Counter1 PWM output OC1B-XOC1B does not work correctly. Only in the case when the control bits,
 *  COM1B1 and COM1B0 are in the same mode as COM1A1 and COM1A0, respectively, the OC1B-XOC1B output
 *  works correctly.
 *  Problem Fix/Work around:
 *  The only workaround is to use same control setting on COM1A[1:0] an

 *
 */
#include <avr/io.h>

#if  defined(__AVR_ATtiny25__) || defined(__AVR_ATtiny45__) || defined(__AVR_ATtiny85__)


#define TIM0_VALUE                                 TCNT0
#define TIM0_CTRL_A                                TCCR0A
#define TIM0_CTRL_B                                TCCR0B

#define TIM0_COMP_A                                OCR0A
#define TIM0_COMP_B                                OCR0B

#define TIM0_OCR0A_PIN                            PB0
#define TIM0_OCR0B_PIN                            PB1
#define TIM0_OCRA_PORT                            PORTB
#define TIM0_INTERRUPT_REG                        TIMSK



/**
 * Set the OC0A as ouptput.
 */
#define timer0_setAsOutput_A()                DDRB |= bit(TIM0_OCR0A_PIN)
#define timer0_clearOutput_A()                DDRB &= ~bit(TIM0_OCR0A_PIN)

/**
 * Set the OC0B=PD5 as output.
 */
#define timer0_setAsOutput_B()                DDRB |= bit(TIM0_OCR0B_PIN)


//timer 1
#define TIM1_VALUE                              TCNT1

#define TIM1_COMP_A                             OCR1A
#define TIM1_COMP_B                             OCR1B
#define TIM1_
#define TIM1_CTRL                               TCCR1


// Timer one has an inverted ouptut alongside the regular output!!
#define TIM1_OC1B_PIN                           PB4
#define TIM1_OC1A_PIN                           PB1
// Inverted
#define TIM1_OC1B_PIN_1                         PB3
#define TIM1_OC1A_PIN_1                         PB0


#define TIM1_OCRA                               OCR1A
#define TIM1_OCRB                               OCR1B

#define timer1_setAsOutput_A()                  DDRB |= (1 << TIM1_OC1A_PIN)
#define timer1_setAsOutput_B()                  DDRB |= (1 << TIM1_OC1B_PIN)
#define timer1_setAsOutput_A_1()                DDRB |= (1 << TIM1_OC1A_PIN_1)
#define timer1_setAsOutput_B_1()                DDRB |= (1 << TIM1_OC1B_PIN_1)


#define TIM1_INTERRUPT_REG                      TIMSK

#define TIMER_1_OVERFLOW_INTERRUPT_FLAG         TOIE1
#define TIMER_1_A_COMPARE_INTERRUPT_FLAG        OCIE1A
#define TIMER_1_B_COMPARE_INTERRUPT_FLAG        OCIE1B
#define TIMER_1_INPUT_CAPTURE_INTERRUPT_FLAG    ICF1
//timer 2


/*		TIMER 0			*/

//the different prescaler modes
#define TIMER_0_PRESCALER_MASK              (~((1 << CS00) | (1 << CS01) | (1 << CS02)))
#define timer0_no_timer()                   (TCCR0B) &= TIMER_0_PRESCALER_MASK
#define timer0_setPrescaler1()              (TCCR0B) |= (1 << CS00                         )
#define timer0_setPrescaler8()              (TCCR0B) |= (            1 << CS01             )
#define timer0_setPrescaler64()             (TCCR0B) |= (1 << CS00 | 1 << CS01             )
#define timer0_setPrescaler256()            (TCCR0B) |= (                        1 << CS02 )
#define timer0_setPrescaler1024()           (TCCR0B) |= (1 << CS00 |             1 << CS02 )
#define timer0_setPrescalerExtFalling()     (TCCR0B) |= (            1 << CS01 | 1 << CS02 )
#define timer0_setPrescalerExtRising()      (TCCR0B) |= (1 << CS00 | 1 << CS01 | 1 << CS02 )

/*			WAVE GENERATION MODES			*/
#define timer0_normalMode()                 TIM0_CTRL_A &= ~(1 << WGM00 | 1 << WGM01 );  (TIM0_CTRL_B &= ~(1 << WGM02))
#define timer0_pwmPhaseCorrect()            TIM0_CTRL_A |= (1 << WGM00)
#define timer0_ctcOCRAMode()                TIM0_CTRL_A |=              (1 << WGM01)
#define timer0_fastPwm()                    TIM0_CTRL_A |= (1 << WGM00 | 1 << WGM01)
#define timer0_pwmPhaseCorrectOCRA()        TIM0_CTRL_A |= (1 << WGM00              ); TIM0_CTRL_B |= (1 << WGM02)
#define timer0_fastPwmOCRA()                TIM0_CTRL_A |= (1 << WGM00 | 1 << WGM01 ); TIM0_CTRL_B |= (1 << WGM02)

/**		COMPARE OUTPUT MODES
 * the behaviour depends on the pwm mode selected. Consult datasheet!
 */
#define timer0_resetOnCompMatch_A()             TIM0_CTRL_A &= ~(1 << COM0A0 | 1 << COM0A1)
#define timer0_toggleOnCompMatch_A()        TIM0_CTRL_A |=  (1 << COM0A0              )
#define timer0_clearOnCompMatch_A()         TIM0_CTRL_A |=  (              1 << COM0A1)
#define timer0_setOnCompMatch_A()           TIM0_CTRL_A |=  (1 << COM0A0 | 1 << COM0A1)

#define timer0_resetOnCompMatch_B()             TIM0_CTRL_A &= ~(1 << COM0B0 | 1 << COM0B1)
#define timer0_toggleOnCompMatch_B()        TIM0_CTRL_A |=  (1 << COM0B0              )
#define timer0_clearOnCompMatch_B()         TIM0_CTRL_A |=  (              1 << COM0B1)
#define timer0_setOnCompMatch_B()           TIM0_CTRL_A |=  (1 << COM0B0 | 1 << COM0B1)


#define timer0_setCompareValue_A(value)          TIM0_COMP_A = (value)
#define timer0_setCompareValue_B(value)          TIM0_COMP_B = (value)

/*		INTERRUPTS		*/
#define timer0_enableOverflowInterrupt()        TIM0_INTERRUPT_REG    |= (1 << TOIE0)
#define timer0_enableCompareInterrupt_A()       TIM0_INTERRUPT_REG    |= (1 << OCIE0A)
#define timer0_enableCompareInterrupt_B()       TIM0_INTERRUPT_REG    |= (1 << OCIE0B)



/*    =========================== TIMER 1 ===============================	 */

#define TIM1_G_CTRL                              GTCCR

// IN CTC mode use OCR1C as top

#define timer1_resetCounterOnCompMatch()        (TIM1_CTRL) |= (1 << CTC1)
#define timer1_enablePWM_A()                    (TIM1_CTRL) |= (1 << PWM1A)
#define timer1_enablePWM_B()                    (TIM1_G_CTRL) |= (1 << PWM1B)

#define timer1_nothingOnCompMatch_A()       TIM1_CTRL &= ~(1 << COM1A0 | 1 << COM1A1)
#define timer1_toggleOnCompMatch_A()        TIM1_CTRL |=  (1 << COM1A0              )
#define timer1_clearOnCompMatch_A()         TIM1_CTRL |=  (              1 << COM1A1)
#define timer1_setOnCompMatch_A()           TIM1_CTRL |=  (1 << COM1A0 | 1 << COM1A1)

#define timer1_nothingOnCompMatch_B()       TIM1_G_CTRL &= ~(1 << COM1B0 | 1 << COM1B1)
#define timer1_toggleOnCompMatch_B()        TIM1_G_CTRL |=  (1 << COM1B0              )
#define timer1_clearOnCompMatch_B()         TIM1_G_CTRL |=  (              1 << COM1B1)
#define timer1_setOnCompMatch_B()           TIM1_G_CTRL |=  (1 << COM1B0 | 1 << COM1B1)


#define timer1_setCompareValue_A(value)          TIM1_COMP_A = (value)
#define timer1_setCompareValue_B(value)          TIM1_COMP_B = (value)

#define TIMER_1_PRESCALER_MASK                  (~((1 << CS10) | (1 << CS11) | (1 << CS12) < (1 << CS13)))
#define timer1_no_timer()                       (TIM1_CTRL) &= PRESCALAR_MASK
#define timer1_setPrescaler1()                  (TIM1_CTRL) |= (1 << CS10 )
#define timer1_setPrescaler2()                  (TIM1_CTRL) |= (            1 << CS11 )
#define timer1_setPrescaler4()                  (TIM1_CTRL) |= (1 << CS10 | 1 << CS11)
#define timer1_setPrescaler8()                  (TIM1_CTRL) |= (                        1 << CS12 )
#define timer1_setPrescaler16()                 (TIM1_CTRL) |= (1 << CS10 |             1 << CS12 )
#define timer1_setPrescaler32()                 (TIM1_CTRL) |= (            1 << CS11 | 1 << CS12 )
#define timer1_setPrescaler64()                 (TIM1_CTRL) |= (1 << CS10 | 1 << CS11 | 1 << CS12 )
#define timer1_setPrescaler128()                (TIM1_CTRL) |= (                                    1 << CS13 )
#define timer1_setPrescaler256()                (TIM1_CTRL) |= (1 << CS10                         | 1 << CS13 )
#define timer1_setPrescaler512()                (TIM1_CTRL) |= (          | 1 << CS11             | 1 << CS13 )
#define timer1_setPrescaler1024()               (TIM1_CTRL) |= (1 << CS10 | 1 << CS11             | 1 << CS13 )
#define timer1_setPrescaler2048()               (TIM1_CTRL) |= (                        1 << CS12 | 1 << CS13 )
#define timer1_setPrescaler4096()               (TIM1_CTRL) |= (1 << CS10             | 1 << CS12 | 1 << CS13 )
#define timer1_setPrescaler8192()               (TIM1_CTRL) |= (          | 1 << CS11 | 1 << CS12 | 1 << CS13 )
#define timer1_setPrescaler16384()              (TIM1_CTRL) |= (1 << CS10 | 1 << CS11 | 1 << CS12 | 1 << CS13 )


#define timer1_enableOverflowInterrupt()        TIM1_INTERRUPT_REG    |= (1 << TOIE1)
#define timer1_enableCompareInterrupt_A()       TIM1_INTERRUPT_REG    |= (1 << OCIE1A)
#define timer1_enableCompareInterrupt_B()       TIM1_INTERRUPT_REG    |= (1 << OCIE1B)


#else
#error "Use only for the Attiny 25/45/85 series!"
#endif

#endif //TIMER_tX5_H
