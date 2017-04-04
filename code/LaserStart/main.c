
#include <avr/io.h>
#include "../timer_tx5.h"
#include "../common.h"

#define BTN_PIN PB3

#define  PWM_THRESHOLD 128

unsigned long millis();


#define LASER_ON()  timer0_setAsOutput_A(); \
timer0_setCompareValue_A(PWM_THRESHOLD)
// make sure we only light up when pressed, so activate only when needed

#define LASER_OFF()  timer0_clearOutput_A(); \
timer0_setCompareValue_A(0)

int main(void) {

    enableInterrupts();
    // enable input with pullup
    setAsInputBBit(BTN_PIN);
    portB_setBit(BTN_PIN);

    // for laser pulsing
    timer0_fastPwm();
    timer0_clearOnCompMatch_A();
    timer0_setCompareValue_A(0);
    timer0_setPrescaler64();

    // for timing
    timer1_enablePWM_B();
    timer1_setPrescaler64();
    timer1_enableOverflowInterrupt();


    byte pressCounter = 0;
    bool wasDown = false, possible = false;
    unsigned long last = 0, now = 0;
    uint diff = 0;

    byte prescaler = 1;

    while (1) {

        // is button pressed? <=> pulled to ground
        if (!pinB_isSet(BTN_PIN)) {
            LASER_ON();
            wasDown = true;
        } else {
            LASER_OFF();

            if (wasDown) {
                pressCounter++;
                last = millis();
            }
            wasDown = false;
        }


        now = millis();
        diff = (uint) (now - last);

        if (pressCounter > 0 && diff >= 1000) {

            // on tripple click change the prescaler
            if (pressCounter > 3) {
                prescaler = ((prescaler + 1) % 5) + 1;
                // clear and set new prescaler
                timer0_no_timer();
                TCCR0B |= prescaler;

                // light up for a second
                delay(500);
                LASER_ON();
                for (byte i = 0; i < prescaler; ++i) {
                    delay(1000);
                }
                LASER_OFF();
            }

            pressCounter = 0;
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