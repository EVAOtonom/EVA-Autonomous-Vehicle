/*
 * wheel.c
 *
 *  Created on: Oct 25, 2023
 *      Author: hp
 */


#include "../wheels/wheel.h"


void wheelInit(){
	WheelLEnable;
	WheelREnable;
	HAL_TIM_PWM_Start(&htim12, WheelPWMLeft);
	HAL_TIM_PWM_Start(&htim12, WheelPWMRight);

}


void wheelTurnRight(wheel_adjust_t * wheelParameter){
	wheelStop(wheelParameter);

	__HAL_TIM_SET_COMPARE(&htim12,WheelPWMLeft,turningSpeed);
}
void wheelTurnLeft(wheel_adjust_t * wheelParameter){
	wheelStop(wheelParameter);
	__HAL_TIM_SET_COMPARE(&htim12,WheelPWMRight,turningSpeed);
}
void wheelStop(wheel_adjust_t * wheelParameter){

	__HAL_TIM_SET_COMPARE(&htim12,WheelPWMLeft,0);
	__HAL_TIM_SET_COMPARE(&htim12,WheelPWMRight,0);

}
