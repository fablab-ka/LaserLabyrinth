
#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include "../adc_tx5.h"
#include "../timer_tx5.h"

#include "../usi_uart.h"

// TODO: 100k für mehr sensitiviät


#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wmissing-noreturn"
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


volatile uint adc_val = 0;
uint ADC_THRESHOLD = 0;// TODO: value??
bool isLow = true;
uint changes = 0;


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

volatile uint adcs = 0;

int main(void) {

    setAsInputBBit(BTN_PIN);
    //setAsOutputBBit(4);
    // pullup
    portB_setBit(BTN_PIN);

    enableInterrupts();
    usiserial_init();
    //usiserial_sendBytes("Booted PulseLed...\n", 18);


// should be between 50kHz and 200kHz
#define ADC_TAKT F_CPU / 200000
#define PWM_START 40
#pragma message STR(ADC_TAKT)

    adc_prescaler64();
    adc_setReferenceVCC();
    adc_useADC_1();
    adc_enable();


    timer0_pwmPhaseCorrect();
    timer0_setAsOutput_A();
    timer0_setOnCompMatch_A();
    timer0_setCompareValue_A(0);
    timer0_setPrescaler64();


    timer1_enablePWM_B();
    timer1_setAsOutput_B();
    timer1_setOnCompMatch_B();
    timer1_setCompareValue_B(PWM_START);
    // to circumvent timer bug!!
    timer1_setOnCompMatch_A();
    //timer1_enablePWM_A();
    //timer1_setAsOutput_A();
    timer1_setCompareValue_A(PWM_START);
    timer1_setPrescaler64();
    timer1_enableOverflowInterrupt();


    // measure ambient liegt
    const uint AMBI = 20;//ambient_light();
    usiserial_sendBytes("Ambi: ", 6);
    //usiserial_byteToHexAscii(AMBI);
    //usiserial_newline();

    ADC_THRESHOLD = AMBI + 30;

    // let the adc run free and trigger an interrupt
    adc_enableAutoTriggerMode();
    adc_autoTriggerFreeRunning();
    adc_enableCompleteInterrupt();
    adc_start();
    unsigned long last = 0, now = 0;

    uint diff = 0;

    while (1) {


        // is button pressed
        if (!pinB_isSet(BTN_PIN)) {
            timer1_setCompareValue_B(128);
            //usiserial_sendBytes("down\n", 5);
        } else {
            timer1_setCompareValue_B(250);
        }


        now = millis();
        diff = (uint) (now - last);
        if (diff >= 1000) {
            usiserial_sendBytes("ADC2: ", 5);
            usiserial_uintToHexAscii(adc_val);
            usiserial_newline();

            usiserial_sendBytes("cs: ", 4);
            usiserial_uintToHexAscii(adcs);
            usiserial_newline();


            usiserial_sendBytes("Changes: ", 8);
            usiserial_uintToHexAscii(changes);
            usiserial_newline();

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

SIGNAL(ADC_vect) {
    // read from the adc
    adcs++;
    adc_val = adc_valuesInRange(ADC_VALUE_16_BIT, ADC_PREC);
    if (adc_val <= ADC_THRESHOLD && !isLow) {
        changes++;
        isLow = true;
    } else if (adc_val > ADC_THRESHOLD && isLow) {
        changes++;
        isLow = false;
    }
}

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

#pragma clang diagnostic pop