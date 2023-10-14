/*
 * bldc.h
 *
 *  Created on: Oct 14, 2023
 *      Author: EVA Otonom
 */

#ifndef BLDC_BLDC_H_
#define BLDC_BLDC_H_
#include "main.h"

extern TIM_HandleTypeDef htim17;



void bldcInit();
void stopBldc();
void adjustBldc(unsigned int speedValue);


#endif /* BLDC_BLDC_H_ */
