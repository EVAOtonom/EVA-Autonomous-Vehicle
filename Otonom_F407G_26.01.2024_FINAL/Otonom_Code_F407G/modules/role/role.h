/*
 * role.h
 *
 *  Created on: Oct 27, 2023
 *      Author: kaana
 */

#ifndef ROLE_ROLE_H_
#define ROLE_ROLE_H_
#include "main.h"


#define BLDCRActive HAL_GPIO_WritePin(BLDC_ROLE_GPIO_Port, BLDC_ROLE_Pin, GPIO_PIN_SET);
#define BLDCRPassive HAL_GPIO_WritePin(BLDC_ROLE_GPIO_Port, BLDC_ROLE_Pin, GPIO_PIN_RESET);

#define RightSignalActive HAL_GPIO_WritePin(RIGHT_SIGNAL_GPIO_Port,RIGHT_SIGNAL_Pin,GPIO_PIN_SET);
#define RightSignalPassive HAL_GPIO_WritePin(RIGHT_SIGNAL_GPIO_Port,RIGHT_SIGNAL_Pin,GPIO_PIN_RESET);

#define LeftSignalActive HAL_GPIO_WritePin(LEFT_SIGNAL_GPIO_Port,LEFT_SIGNAL_Pin,GPIO_PIN_SET);
#define LeftSignalPassive HAL_GPIO_WritePin(LEFT_SIGNAL_GPIO_Port,LEFT_SIGNAL_Pin,GPIO_PIN_RESET);

#define StopSignalActive HAL_GPIO_WritePin(STOP_SIGNAL_GPIO_Port,STOP_SIGNAL_Pin,GPIO_PIN_SET);
#define StopSignalPassive HAL_GPIO_WritePin(STOP_SIGNAL_GPIO_Port,STOP_SIGNAL_Pin,GPIO_PIN_RESET);


#define EmergencyActive HAL_GPIO_WritePin(EMERGENCY_SIGNAL_GPIO_Port,EMERGENCY_SIGNAL_Pin,GPIO_PIN_SET);
#define EmergencyPassive HAL_GPIO_WritePin(EMERGENCY_SIGNAL_GPIO_Port,EMERGENCY_SIGNAL_Pin,GPIO_PIN_RESET);

#define FrontLambActive HAL_GPIO_WritePin(FRONT_LAMB_GPIO_Port,FRONT_LAMB_Pin,GPIO_PIN_SET);
#define FrontLambPassive HAL_GPIO_WritePin(FRONT_LAMB_GPIO_Port,FRONT_LAMB_Pin,GPIO_PIN_RESET);



typedef enum {
	SIGNAL_ACTIVE_r,
	SIGNAL_PASSIVE_r
}RighSignalControl;

typedef enum {
	SIGNAL_ACTIVE_l,
	SIGNAL_PASSIVE_l,
}LeftSignalControl;

typedef enum {
	SIGNAL_ACTIVE_s,
	SIGNAL_PASSIVE_s
}StopSignalControl;

typedef enum {
	SIGNAL_ACTIVE_e,
	SIGNAL_PASSIVE_e
}EmergencySignal;
typedef enum {
	SIGNAL_ACTIVE_f,
	SIGNAL_PASSIVE_f
}FrontSignal;

typedef enum {

	REVERSE,
	FORWARD
}BldcControl;



typedef struct {

    int16_t right_signal_i; //Boolean degerleri
    int16_t left_signal_i;
    int16_t stop_signal_i;
    int16_t bldc_signal_i;
    int16_t front_signal_i;
    int16_t emergency_signal_i;
	RighSignalControl rightSignal;
	LeftSignalControl leftSignal;
	StopSignalControl stopSignal;
	BldcControl bldcSignal;
	EmergencySignal emergencySignal;
	FrontSignal frontSignal;

}role_State_Adjust_t;
//to be contiune


void signalInit();
void switchAdjust(role_State_Adjust_t* role_state_adjust_t);
void delay_ms(int16_t k);













#endif /* ROLE_ROLE_H_ */
