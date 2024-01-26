/*
 * manuel.c
 *
 *  Created on: Jan 2, 2024
 *      Author: kaana
 */


#include "manuel.h"

int privatModeCounter=0;
int i0=0;
int i1=0;
int i2=0;
int i3=0;
int i4=0;
int i5=0;

void getMode (manuel_mode_t *manuelParameters) {


	/* 0-0 AUTO
	 * 1-0 MANUEL
	 * 0-1 REMOTE
	 * 1-1 PRIVATE(B,K)
	 */

	if(HAL_GPIO_ReadPin(MANUEL_SWITCH_GPIO_Port, MANUEL_SWITCH_Pin) && HAL_GPIO_ReadPin(MANUEL_SWITCH2_GPIO_Port, MANUEL_SWITCH2_Pin)){

		manuelParameters->mod = AUTOMODE;
		setSpeed = 10;
        privatModeCounter=0;
        i0=0;
        i1=0;
        i2=0;
        i3=0;
        i4=0;
        i5=0;



	}

	else if (!HAL_GPIO_ReadPin(MANUEL_SWITCH_GPIO_Port, MANUEL_SWITCH_Pin) && HAL_GPIO_ReadPin(MANUEL_SWITCH2_GPIO_Port, MANUEL_SWITCH2_Pin)) {

		manuelParameters->mod = MANUELMODE;
        privatModeCounter=0;
        i0=0;
        i1=0;
        i2=0;
        i3=0;
        i4=0;
        i5=0;


		if(!HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_12))
			{
				setSpeed=5;
				setAdc  = (64/5);
			}
			else if(!HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_13))
				{
					setSpeed=15;
					setAdc  = (64/15);
				}

			else {
				setSpeed=10;
				setAdc  = (64/10);

			}

		}

	else if (HAL_GPIO_ReadPin(MANUEL_SWITCH_GPIO_Port, MANUEL_SWITCH_Pin) && !HAL_GPIO_ReadPin(MANUEL_SWITCH2_GPIO_Port, MANUEL_SWITCH2_Pin)) {

		manuelParameters->mod = REMOTECONTROLMODE;
		setSpeed=10;
        privatModeCounter=0;
        i0=0;
        i1=0;
        i2=0;
        i3=0;
        i4=0;
        i5=0;

	}
	else if (!HAL_GPIO_ReadPin(MANUEL_SWITCH_GPIO_Port, MANUEL_SWITCH_Pin) && !HAL_GPIO_ReadPin(MANUEL_SWITCH2_GPIO_Port, MANUEL_SWITCH2_Pin)) {

		if (privatModeCounter != 20) {

		manuelParameters->mod = DEFAULTMODE;
		setSpeed  = 1;
		setAdc  = (64/1);


		if (HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_13)) {

			 if (!HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_12)) {

				 if (i0 <=1) {

				 i0 = 1;
				 delay_ms(200);
				 }

				}


			 if (HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_12) && i0 == 1 ) {

				 if (i1 <=2) {

				 i1 = 2;
				 delay_ms(200);

				}

			 }

			 if (!HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_12) && i0 == 1 && i1 == 2) {

				 if (i2 <=3) {

				 i2 = 3;
				 delay_ms(200);

				}

			 }

			 if (HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_12) && i0 == 1 && i1 == 2 && i2==3) {

				 if (i3 <=4) {

				 i3 = 4;
				 delay_ms(200);

				}

			 }

			 if (!HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_12) && i0 == 1 && i1 == 2 && i2==3 && i3==4) {

				 if (i4 <=5) {

				 i4 = 5;
				 i5 = i4;
				 delay_ms(200);

				}

			 }

			 privatModeCounter = i0 + i1 + i2 + i3 + i4 + i5;
			 }




		else if (!HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_13))
		{
			i0=0;
			i1=0;
			i2=0;
			i3=0;
			i4=0;
			i5=0;
			privatModeCounter=0;

		}
		}

			        if (privatModeCounter == 20) {

			            manuelParameters->mod = PRIVATMODE;
						setSpeed  = 20;
						setAdc  = (64/20);

			    }



	}

}



void readAdc_speed(manuel_mode_t *manuelParameters) {

		HAL_ADC_Start(&hadc1);
		HAL_ADC_PollForConversion(&hadc1, 100);
		delay_ms(100);
	    manuelParameters->adc_Speed = HAL_ADC_GetValue(&hadc1) >> 2;
	    manuelParameters->adc_Speed = manuelParameters->adc_Speed/setAdc;
	    HAL_ADC_Stop(&hadc1);
}

