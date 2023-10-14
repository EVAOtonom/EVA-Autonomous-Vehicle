/*
 * wheel.c
 *
 *  Created on: Oct 14, 2023
 *      Author: hp
 */


#include "wheel.h"


void wheelInit(){
	WheelLEnable;
	WheelREnable;
	HAL_TIM_PWM_Start(&htim15, WheelPWMLeft);
	HAL_TIM_PWM_Start(&htim15, WheelPWMRight);
}


void wheelTurnRight(wheel_adjust_t * wheelParameter){
	wheelStop(wheelParameter);

	__HAL_TIM_SET_COMPARE(&htim15,WheelPWMRight,turningSpeed);
}
void wheelTurnLeft(wheel_adjust_t * wheelParameter){
	wheelStop(wheelParameter);
	__HAL_TIM_SET_COMPARE(&htim15,WheelPWMLeft,turningSpeed);
}
void wheelStop(wheel_adjust_t * wheelParameter){

	__HAL_TIM_SET_COMPARE(&htim15,WheelPWMLeft,0);
	__HAL_TIM_SET_COMPARE(&htim15,WheelPWMRight,0);
}
