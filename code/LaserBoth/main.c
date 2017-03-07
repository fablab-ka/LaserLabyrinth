
#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include "../adc_tx5.h"
#include "../timer_tx5.h"

#include "../usi_uart.h"

// TODO: 100k für mehr sensitiviät


#define PULSE_PRESCALE 256
// Frequency / timer prescaler / pwm_width
#define PULSE_DURATION F_CPU / PULSE_PRESCALE / 128
#define  ADC_PREC 10
#define AMBI_SAMPLES 20
#define AMBI_MAX_DIFF 5
#define AMBI_SAMPLE_PAUSE 100

#define BTN_PIN PB3

volatile byte counter = 0;

unsigned long millis();


uint ambient_light() {

    uint samples = 0, val = 0, last = 0, sum = 0, extras = 0;
    // take some initial samples
    while (samples < AMBI_SAMPLES + extras) {
        adc_start();
        adc_waitForConversionComplete();
        val = adc_valuesInRange(ADC_VALUE_16_BIT, ADC_PREC);
        samples++;

        // if there are are big difference, sample again
        if (abs(last - val) > AMBI_MAX_DIFF)
            extras++;

        sum += val;
        last = val;
        delay(AMBI_SAMPLE_PAUSE);
    }

    uint ambi = sum / samples;
    return ambi;
}

int main(void) {

    setAsInputBBit(BTN_PIN);
    //setAsOutputBBit(4);
    // pullup
    portB_setBit(BTN_PIN);

    enableInterrupts();
    usiserial_init();
    usiserial_sendBytes("Booted PulseLed...\n", 18);


// should be between 50kHz and 200kHz
#define ADC_TAKT F_CPU / 200000
#define PWM_START 240
#pragma message STR(ADC_TAKT)

    adc_prescaler64();
    adc_setReferenceVCC();
    adc_useADC_1();
    adc_enable();

    timer0_pwmPhaseCorrect();
    timer0_setAsOutput_A();
    timer0_setOnCompMatch_A();
    timer0_setCompareValue_A(PWM_START);
    timer0_setPrescaler64();


    timer1_enablePWM_B();
    timer1_setAsOutput_B();
    timer1_setOnCompMatch_B();
    timer1_setCompareValue_B(PWM_START);
    // to circumvent timer bug!!
    timer1_setOnCompMatch_A();
    timer1_enablePWM_A();
    timer1_setAsOutput_A();
    timer1_setCompareValue_A(PWM_START);

    timer1_setPrescaler64();
    timer1_enableOverflowInterrupt();


    // measure ambient liegt
    const uint AMBI = ambient_light();
    usiserial_sendBytes("Ambi: ", 6);
    usiserial_byteToHexAscii(AMBI);
    usiserial_newline();


    uint adc_val = 0;
    unsigned long last = 0, now = 0;
    bool isLow = true;
    uint changes = 0;
    uint diff = 0;

    const uint  ADC_THRESHOLD = AMBI + 30;// TODO: value??
    while (1) {


        // is button pressed
        if (!pinB_isSet(BTN_PIN)) {
            timer1_setCompareValue_B(0);
        } else {
            timer1_setCompareValue_B(200);
        }



        // read from the adc
        adc_start();
        adc_waitForConversionComplete();
        adc_val = adc_valuesInRange(ADC_VALUE_16_BIT, ADC_PREC);

        if (adc_val <= ADC_THRESHOLD && !isLow) {
            changes++;
            isLow = true;
        } else if (adc_val > ADC_THRESHOLD && isLow) {
            changes++;
            isLow = false;
        }

        now = millis();
        diff = (uint) (now - last);
        if (diff >= 1000) {
            usiserial_sendBytes("ADC2: ", 5);
            usiserial_byteToHexAscii(adc_val);
            usiserial_newline();

            usiserial_sendBytes("Changes: ", 8);
            usiserial_byteToHexAscii(changes);
            usiserial_newline();

            changes = 0;
            last = now;
        }

    }


    //setAsOutputDBit(7);
    //portD_setBit(6);

    timer0_pwmPhaseCorrect();
    timer0_enableOverflowInterrupt();
    timer0_normalMode();
    //set prescaler =>  enable the timer
    timer0_setPrescaler256();

    // timer1 is a bit different
    timer1_enablePWM_A();
    //timer1_clearOC0AOnCompMatch_A();
    //timer1_clearOC0BOnCompMatch_B();

    //enable the output pins
    timer1_setAsOutput_A();
    timer1_setPrescaler256();
    timer1_setCompareValue_B(128);



    //do one dummy readout
    adc_start();
    adc_waitForConversionComplete();
#if UART
    uart_init_simple();
    uart_puts("booted...\n");
#endif
    unsigned long int adc = 0;
    adc_start();
    byte lower = 0, higher = 0;


    while (1) {


        adc_start();
        adc_waitForConversionComplete();

        adc = ADC_VALUE_16_BIT;
        if (adc <= 25 && !isLow) {
            changes++;
            isLow = true;
        } else if (adc > 25 && isLow) {
            changes++;
            isLow = false;
        }


        now = millis();
        diff = (now - last);
        if (diff >= 500) {
#if UART
            uart_puts("ADC: ");
            uart_uintToAscii(adc);
            uart_newline();
            uart_puts("F: ");
            uart_uintToAscii(changes);
            uart_newline();
#endif
            changes = 0;
            last = now;
        }

    }
}


// COPIED FROM ARDUINO millis()

#define clockCyclesPerMicrosecond() ( F_CPU / 1000000L )
#define clockCyclesToMicroseconds(a) ( (a) / clockCyclesPerMicrosecond() )
// the prescaler is set so that timer0 ticks every 64 clock cycles, and the
// the overflow handler is called every 256 ticks.
#define MICROSECONDS_PER_TIMER0_OVERFLOW (clockCyclesToMicroseconds(64 * 256))

// the whole number of milliseconds per timer0 overflow
#define MILLIS_INC (MICROSECONDS_PER_TIMER0_OVERFLOW / 1000)

// the fractional number of milliseconds per timer0 overflow. we shift right
// by three to fit these numbers into a byte. (for the clock speeds we care
// about - 8 and 16 MHz - this doesn't lose precision.)
#define FRACT_INC ((MICROSECONDS_PER_TIMER0_OVERFLOW % 1000) >> 3)
#define FRACT_MAX (1000 >> 3)

volatile unsigned long timer0_overflow_count = 0;
volatile unsigned long timer0_millis = 0;
static unsigned char timer0_fract = 0;


SIGNAL(TIMER1_OVF_vect) {
    // copy these to local variables so they can be stored in registers
    // (volatile variables must be read from memory on every access)
    unsigned long m = timer0_millis;
    unsigned char f = timer0_fract;

    m += MILLIS_INC;
    f += FRACT_INC;
    if (f >= FRACT_MAX) {
        f -= FRACT_MAX;
        m += 1;
    }

    timer0_fract = f;
    timer0_millis = m;
    timer0_overflow_count++;
}

unsigned long millis() {
    unsigned long m;
    uint8_t oldSREG = SREG;

    // disable interrupts while we read timer0_millis or we might get an
    // inconsistent value (e.g. in the middle of a write to timer0_millis)
    cli();
    m = timer0_millis;
    SREG = oldSREG;

    return m;
}