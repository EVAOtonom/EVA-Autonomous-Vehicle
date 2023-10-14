/*
 * bldc.c
 *
 *  Created on: Oct 14, 2023
 *      Author: EVA Otonom
 */


#include "bldc/bldc.h"


void bldcInit(){
	HAL_TIM_PWM_Start(&htim17,TIM_CHANNEL_1);
}
void stopBldc(){
	__HAL_TIM_SET_COMPARE(&htim17,TIM_CHANNEL_1,0);


}
void adjustBldc(unsigned int speedValue){

	__HAL_TIM_SET_COMPARE(&htim17,TIM_CHANNEL_1,speedValue);
}

