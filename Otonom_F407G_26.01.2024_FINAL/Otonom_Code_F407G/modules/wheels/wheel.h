/*
 * wheel.h
 *
 *  Created on: Oct 25, 2023
 *      Author: hp
 */

#ifndef SRC_WHEEL_H_
#define SRC_WHEEL_H_
#include "main.h"

#define WheelREnable HAL_GPIO_WritePin(DireksiyonEn_R_GPIO_Port, DireksiyonEn_R_Pin, GPIO_PIN_SET)
#define WheelRDisable HAL_GPIO_WritePin(DireksiyonEn_R_GPIO_Port, DireksiyonEn_R_Pin, GPIO_PIN_RESET)
#define WheelLEnable HAL_GPIO_WritePin(DireksiyonEn_L_GPIO_Port, DireksiyonEn_L_Pin, GPIO_PIN_SET)
#define WheelLDisable HAL_GPIO_WritePin(DireksiyonEn_L_GPIO_Port, DireksiyonEn_L_Pin, GPIO_PIN_RESET)
#define turningSpeed 50
#define WheelPWMLeft  TIM_CHANNEL_1
#define WheelPWMRight  TIM_CHANNEL_2
extern TIM_HandleTypeDef htim12;

void wheelInit();
void wheelStop();
void wheelTurnLeft();
void wheelTurnRight();





#endif /* SRC_WHEEL_H_ */
