/*
 * break.c
 *
 *  Created on: Oct 15, 2023
 *      Author: hp
 */

#include "break/break.h"
void breakInit()
{
	FrenREnable;
	FrenLEnable;
}

static void stop_break(switchBreak_adjust_t *breakParameters)
{
	FrenPWM_RDisable;
	FrenPWM_LDisable;
	breakParameters->motorStatus = NoMovment;

}

static void press_break(switchBreak_adjust_t *breakParameters)
{
	stop_break(breakParameters);
	if(breakParameters->switchStatus_press != SWITCH_PRESSED)
	{
		FrenPWM_LEnable;
		breakParameters->motorStatus = PressingBreak;
	}
}

static void release_break(switchBreak_adjust_t *breakParameters)
{
	stop_break(breakParameters);

	if (breakParameters->switchStatus_release != SWITCH_PRESSED ) {

		FrenPWM_REnable;
		breakParameters->motorStatus = RealasingBreak;

	}

}



void breakCheckSwitchStatus(switchBreak_adjust_t *breakParameters)
{
	if(HAL_GPIO_ReadPin(FrenSwitch_Press_GPIO_Port, FrenSwitch_Press_Pin))
	{
		breakParameters->switchStatus_press = SWITCH_RELEASED;

	}
	else
	{
		breakParameters->switchStatus_press = SWITCH_PRESSED;
	}

	if(!HAL_GPIO_ReadPin(FrenSwitch_Release_GPIO_Port, FrenSwitch_Release_Pin)) {

		breakParameters->switchStatus_release = SWITCH_RELEASED;
	}
	else
	{
		breakParameters->switchStatus_release = SWITCH_PRESSED;
	}

}

void breakAdjust(switchBreak_adjust_t *breakParameters)
{

	if(breakParameters->pressing_break)
	{
		press_break(breakParameters);
	}
	else
	{
		release_break(breakParameters);
	}
}



