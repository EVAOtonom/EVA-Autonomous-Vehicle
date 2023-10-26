/*
 * break.h
 *
 *  Created on: Oct 15, 2023
 *      Author: hp
 */

#ifndef BREAK_BREAK_H_
#define BREAK_BREAK_H_

#include "main.h"

#define FrenREnable HAL_GPIO_WritePin(FrenEn_R_GPIO_Port, FrenEn_R_Pin, GPIO_PIN_SET)
#define FrenRDisable HAL_GPIO_WritePin(FrenEn_R_GPIO_Port, FrenEn_R_Pin, GPIO_PIN_RESET)
#define FrenLEnable HAL_GPIO_WritePin(FrenEn_L_GPIO_Port, FrenEn_L_Pin, GPIO_PIN_SET)
#define FrenLDisable HAL_GPIO_WritePin(FrenEn_L_GPIO_Port, FrenEn_L_Pin, GPIO_PIN_RESET)

#define FrenPWM_REnable HAL_GPIO_WritePin(FrenPWM_R_GPIO_Port, FrenPWM_R_Pin, GPIO_PIN_SET)
#define FrenPWM_RDisable HAL_GPIO_WritePin(FrenPWM_R_GPIO_Port, FrenPWM_R_Pin, GPIO_PIN_RESET)
#define FrenPWM_LEnable HAL_GPIO_WritePin(FrenPWM_L_GPIO_Port, FrenPWM_L_Pin, GPIO_PIN_SET)
#define FrenPWM_LDisable HAL_GPIO_WritePin(FrenPWM_L_GPIO_Port, FrenPWM_L_Pin, GPIO_PIN_RESET)


typedef enum {
    SWITCH_RELEASED,  // Switch basılmamış
    SWITCH_PRESSED   // Switch basılmış
} SwitchState;

typedef enum {
	NoMovment,
    PressingBreak,  // Switch basılmamış
    RealasingBreak   // Switch basılmış
} BreakMotorStatus;

typedef struct switchBreak_adjust_s {

	int16_t pressing_break;
    SwitchState switchStatus_press;
    SwitchState switchStatus_release;  // Enum tipini struct içinde kullanıyoruz
    BreakMotorStatus motorStatus;
} switchBreak_adjust_t;

SwitchState switch_break();


void breakInit();
void breakCheckSwitchStatus(switchBreak_adjust_t *breakParameters);
void breakAdjust(switchBreak_adjust_t *breakParameters);

#endif /* BREAK_BREAK_H_ */
