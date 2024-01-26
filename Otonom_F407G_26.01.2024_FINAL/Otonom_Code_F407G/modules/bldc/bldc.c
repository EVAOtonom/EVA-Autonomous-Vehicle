/*
 * bldc.c
 *
 *  Created on: Oct 14, 2023
 *      Author: EVA Otonom
 */


#include "bldc.h"
#include "../role/role.h"


void bldcInit(){

	HAL_TIM_PWM_Start(&htim14,TIM_CHANNEL_1);
}
void stopBldc(){

	__HAL_TIM_SET_COMPARE(&htim14,TIM_CHANNEL_1,0);


}
void adjustBldc(unsigned int speedValue){

	if(speedValue<=setSpeed && speedValue>=0){
		__HAL_TIM_SET_COMPARE(&htim14,TIM_CHANNEL_1,speedValue);
						}

			else if(speedValue>setSpeed){

				speedValue  = setSpeed;
				__HAL_TIM_SET_COMPARE(&htim14,TIM_CHANNEL_1,speedValue);

			}


}


