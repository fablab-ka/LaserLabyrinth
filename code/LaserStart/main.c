
#include <avr/io.h>
#include "../timer_tx5.h"
#include "../common.h"


#define BTN_PIN PB3

#define  PWM_THRESHOLD 128

unsigned long millis();


int main(void) {

    // enable input with pullup
    //setAsInputBBit(BTN_PIN);
    portB_setBit(BTN_PIN);

    timer0_fastPwm();
    timer0_clearOnCompMatch_A();
    timer0_setCompareValue_A(0);
    timer0_setPrescaler64();


    while (1) {

        // is button pressed? <=> pulled to ground
        if (!pinB_isSet(BTN_PIN)) {
            // make sure we only light up when pressed
            timer0_setAsOutput_A();
            timer0_setCompareValue_A(PWM_THRESHOLD);
        } else {
            timer0_clearOutput_A();
            timer0_setCompareValue_A(0);
        }
    }
}
