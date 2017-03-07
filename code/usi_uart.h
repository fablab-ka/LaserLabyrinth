//
// Created by me on 05.03.17.
//

#ifndef AVR_TOP_USI_UART_H
#define AVR_TOP_USI_UART_H

#include "common.h"

void usiserial_init();
void usiserial_sendByte(byte data);
void usiserial_sendBytes(byte *message, byte len);
void usiserial_byteToHexAscii(byte value);
#define usiserial_newline() usiserial_sendByte('\n')
#endif //AVR_TOP_USI_UART_H
