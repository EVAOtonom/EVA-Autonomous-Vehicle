/*
 * manuel.h
 *
 *  Created on: Jan 2, 2024
 *      Author: kaana
 */

#ifndef MANUEL_MANUEL_H_
#define MANUEL_MANUEL_H_


#include "main.h"
#include "../../modules/role/role.h"
#include "../../modules/bldc/bldc.h"


extern ADC_HandleTypeDef hadc1;
extern int16_t wantedSpeed ;

typedef enum {

	DEFAULTMODE=0,
	AUTOMODE=1,
	MANUELMODE=2,
	REMOTECONTROLMODE=3,
	PRIVATMODE=4


}MODE_DEFINITON;

typedef struct {

	MODE_DEFINITON mod;
	uint16_t adc_Speed;

}manuel_mode_t;


extern uint8_t setAdc  ;
extern uint8_t setSpeed ;
extern uint8_t pActiveCount;


void getMode (manuel_mode_t *manuelParameters);
void readAdc_speed(manuel_mode_t *manuelParameters);




#endif /* MANUEL_MANUEL_H_ */
