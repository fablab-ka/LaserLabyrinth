/*
 * adc.h
 *
 *  Created on: Mar 2, 2017
 *      Author: Mark Weinreuter
 */

#ifndef ADC_ADC_H_
#define ADC_ADC_H_

#include <avr/io.h>
#include "common.h"

#if  defined (__AVR_ATtiny25__) || defined (__AVR_ATtiny45__) || defined (__AVR_ATtiny85__)

/**
 * Turn on power reduction. ADC must be disabled!
 * NOTE: cannot use ACD MUX as AC input.
 */
#define adc_power_reduction_off()           PRR &= ~bit(PRADC)
#define adc_power_reduction_on()            PRR |= bit(PRADC)

#define ADC_VALUE_LOW                        ADCL
#define ADC_VALUE_HIGH                        ADCH
#define ADC_VALUE_16_BIT                    ADCW/* 10bits are used*/
#define ADC_COMPLETE_INTERRUPT_FLAG            ADIF

#define AREF_PIN                            PB0

#define ADC_MUX_0_PIN                       PC0
#define ADC_MUX_1_PIN                       PC1
#define ADC_MUX_2_PIN                       PC2
#define ADC_MUX_3_PIN                       PC3
/** Note: this is also the I2c-SDA-pin */
#define ADC_MUX_4_PIN                       PC4
/** Note: this is also the I2c-SCL-pin */
#define ADC_MUX_5_PIN                       PC5

#define adc_clearReferenceBits()                ADMUX &= ~bit3(REFS0, REFS1, REFS2)
#define adc_setReferenceVCC()                    adc_clearReferenceBits()
#define adc_setReferenceAREF()                    adc_clearReferenceBits(); ADMUX |= bit(REFS0)
#define adc_setReferenceInternal_1_1V()            adc_clearReferenceBits(); ADMUX |= bit2(       REFS1)
#define adc_setReferenceInternal_2_56V()        adc_clearReferenceBits(); ADMUX |= bit2(       REFS1, REFS2)
#define adc_setReferenceInternal_2_56V_Cap()                              ADMUX |= bit3(REFS0, REFS1, REFS2)

/**
 * Uses the bits 0,1 of ADCH and all of ADCL.
 */
#define adc_useRightAlignedData()            ADMUX &= ~bit(ADLAR)

/**
 * Uses all bits ADCH and 7,6 of ADCL.
 */
#define adc_useLeftAlignedData()            ADMUX |= bit(ADLAR)

/**
 * Ensures, that the values are clamped to 2^range possible values)
 */
#define adc_valuesInRange(adcValue, range)            (adcValue >> (10 -range))

//specifies which of the 0-7 pins to use for the adc input
#define adc_clearMuxBits()                    ADMUX &= ~bit4(MUX3, MUX2,  MUX1, MUX0)
#define adc_useADC_0()                        adc_clearMuxBits()
#define adc_useADC_1()                        adc_clearMuxBits(); ADMUX |= bit(MUX0)
#define adc_useADC_2()                        adc_clearMuxBits(); ADMUX |=        bit(MUX1)
#define adc_useADC_3()                        adc_clearMuxBits(); ADMUX |= bit2(MUX0, MUX1)
/*
 * TODO:
#define adc_useADC_6()						adc_clearMuxBits(); ADMUX |= bit2(MUX1, MUX2)
#define adc_useADC_7()						adc_clearMuxBits(); ADMUX |= bit3(MUX0, MUX1, MUX2)
#define adc_use_1_1V()						adc_clearMuxBits(); ADMUX |= bit3(MUX1, MUX2, MUX3)
#define adc_useGND()						adc_clearMuxBits(); ADMUX |= bit4(MUX0, MUX1, MUX2, MUX3)

*/


/**
 * Enables the adc.
 */
#define adc_enable()                        ADCSRA |= bit(ADEN)
/**
 * Disables the adc and terminates a pending conversion.
 */
#define adc_disable()                        ADCSRA &= ~bit(ADEN)

/**
 * Start a conversion.
 */
#define adc_start()                            ADCSRA |= bit(ADSC)

//wait till the bit is cleared
#define adc_waitForConversionComplete()        while(ADCSRA & bit(ADSC))

#define adc_enableAutoTriggerMode()            ADCSRA |= bit(ADATE)

#define adc_enableCompleteInterrupt()        ADCSRA |= bit(ADIE)

//first clears the unused bits and sets the required ones => enables easy switching
#define adc_clearPrescalerBits()            ADCSRA = (ADCSRA & ~bit3(ADPS0, ADPS1, ADPS2))
#define adc_prescalerOff()                    adc_clearPrescalerBits();
#define adc_prescaler2()                    adc_clearPrescalerBits();        ADCSRA |= bit(ADPS0)
#define adc_prescaler4()                    adc_clearPrescalerBits();        ADCSRA |= bit(ADPS1)
#define adc_prescaler8()                    adc_clearPrescalerBits();        ADCSRA |= bit2(ADPS0, ADPS1)
#define adc_prescaler16()                    adc_clearPrescalerBits();        ADCSRA |= bit(ADPS2)
#define adc_prescaler32()                    adc_clearPrescalerBits();        ADCSRA |= bit2(ADPS0, ADPS2)
#define adc_prescaler64()                    adc_clearPrescalerBits();        ADCSRA |= bit2(ADPS1, ADPS2)
#define adc_prescaler128()                                                     ADCSRA |= bit3(ADPS0, ADPS1, ADPS2)

//disables the specified adc, should be used to reduce power consumption
//if an analog signal is applied at ADC0...5
#define adc_disableADC_0()                    DIDR0 |= bit(ADC0D)
#define adc_disableADC_1()                    DIDR0 |= bit(ADC1D)
#define adc_disableADC_2()                    DIDR0 |= bit(ADC2D)
#define adc_disableADC_3()                    DIDR0 |= bit(ADC3D)

//if ADATE is set, these select the trigger source for an ADC conversion
//see the data sheet for some more information about interupts and switching modes
#define adc_autoTriggerFreeRunning()                ADCSRB = (ADCSRB & ~(1 << ADTS0 | 1 <<  ADTS1 | 1 << ADTS2))
#define adc_autoTriggerAnalogComp()                ADCSRB = (ADCSRB & ~(              1 <<  ADTS1 | 1 << ADTS2)) | (1 << ADTS0)
#define adc_autoTriggerExtInterrupt0()            ADCSRB = (ADCSRB & ~(1 << ADTS0              | 1 << ADTS2)) | (             1 << ADTS1)
// TODO: add more!


#else
#error "Chip not yet supported."
#endif


extern unsigned int adc_getSampleBlocking(byte samples);

#endif /* ADC_ADC_H_ */
