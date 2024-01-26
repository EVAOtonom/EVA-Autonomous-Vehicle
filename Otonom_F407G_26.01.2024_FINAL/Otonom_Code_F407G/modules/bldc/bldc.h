/*
 * bldc.h
 *
 *  Created on: Oct 14, 2023
 *      Author: EVA Otonom
 */

#ifndef BLDC_BLDC_H_
#define BLDC_BLDC_H_
#include "main.h"

typedef enum {
    EngineFront,  // Motor öne gidiyor
    EngineBack   // Motor geriye gidiyor
} BldcState;

extern TIM_HandleTypeDef htim14;
extern uint8_t setSpeed;

void bldcInit();
void stopBldc();
void adjustBldc(unsigned int speedValue);


#endif /* BLDC_BLDC_H_ */
