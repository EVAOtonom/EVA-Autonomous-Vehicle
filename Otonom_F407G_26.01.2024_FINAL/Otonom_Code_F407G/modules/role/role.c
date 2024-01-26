/*
 * role.c
 *
 *  Created on: Oct 27, 2023
 *      Author: kaana
 */


#include "role.h"


void signalInit(){

	BLDCRPassive;
	LeftSignalPassive;
	RightSignalPassive;
	StopSignalPassive;
};




void bldcReverseSignal(role_State_Adjust_t* role_state_adjust_t){

	BLDCRActive;
	role_state_adjust_t->bldcSignal=REVERSE;


}
void bldcForwardSignal(role_State_Adjust_t* role_state_adjust_t){
	BLDCRPassive;
	role_state_adjust_t->bldcSignal=FORWARD;

}
void rightSignalOpen(role_State_Adjust_t* role_state_adjust_t){

	role_state_adjust_t->rightSignal = SIGNAL_ACTIVE_r;

	RightSignalActive;

}
void rightSignalClose(role_State_Adjust_t* role_state_adjust_t){
	RightSignalPassive;
	role_state_adjust_t->rightSignal = SIGNAL_PASSIVE_r;
}


void leftSignalOpen(role_State_Adjust_t* role_state_adjust_t){
	LeftSignalActive;
	role_state_adjust_t->leftSignal = SIGNAL_ACTIVE_l;
}
void leftSignalClose(role_State_Adjust_t* role_state_adjust_t){
	LeftSignalPassive;
	role_state_adjust_t->leftSignal = SIGNAL_PASSIVE_l;
}

void stopSignalOpen(role_State_Adjust_t* role_state_adjust_t){
	StopSignalActive;
	role_state_adjust_t->stopSignal = SIGNAL_ACTIVE_s;
}
void stopSignalClose(role_State_Adjust_t* role_state_adjust_t){
	StopSignalPassive;
	role_state_adjust_t->stopSignal = SIGNAL_PASSIVE_s;


}
void emergencySignalClose(role_State_Adjust_t* role_state_adjust_t){
	EmergencyPassive;
	role_state_adjust_t->emergencySignal = SIGNAL_PASSIVE_e;


}
void emergencySignalOpen(role_State_Adjust_t* role_state_adjust_t){
	EmergencyActive;
	role_state_adjust_t->emergencySignal = SIGNAL_ACTIVE_e;


}

void frontSignalOpen(role_State_Adjust_t *role_state_adjust_t){

	FrontLambActive;
	role_state_adjust_t->frontSignal=SIGNAL_ACTIVE_f;


};
void frontSignalClose(role_State_Adjust_t *role_state_adjust_t){

	FrontLambPassive;
	role_state_adjust_t->frontSignal=SIGNAL_PASSIVE_f;

};

void signalDispose(){

	    BLDCRPassive;
		LeftSignalPassive;
		RightSignalPassive;
		StopSignalPassive;
}



void switchAdjust(role_State_Adjust_t* role_state_adjust_t){



	if(role_state_adjust_t->bldc_signal_i){

		bldcReverseSignal(role_state_adjust_t);

	} else if(!role_state_adjust_t->bldc_signal_i){
		bldcForwardSignal(role_state_adjust_t);
	}

	///////////////
	if(role_state_adjust_t->left_signal_i){

		leftSignalOpen(role_state_adjust_t);
		delay_ms(2000);
		leftSignalClose(role_state_adjust_t);
		delay_ms(2000);
		leftSignalOpen(role_state_adjust_t);
		delay_ms(2000);
		leftSignalClose(role_state_adjust_t);
		delay_ms(2000);
		leftSignalOpen(role_state_adjust_t);
		delay_ms(2000);
		leftSignalClose(role_state_adjust_t);
		delay_ms(2000);
		leftSignalOpen(role_state_adjust_t);
		delay_ms(2000);
		leftSignalClose(role_state_adjust_t);

		role_state_adjust_t->left_signal_i = 0;

	}
	else if(!role_state_adjust_t->left_signal_i){

		leftSignalClose(role_state_adjust_t);

	}
	//////////
	if(role_state_adjust_t->right_signal_i){

		rightSignalOpen(role_state_adjust_t);
		delay_ms(2000);
		rightSignalClose(role_state_adjust_t);
		delay_ms(2000);
		rightSignalOpen(role_state_adjust_t);
		delay_ms(2000);
		rightSignalClose(role_state_adjust_t);
		delay_ms(2000);
		rightSignalOpen(role_state_adjust_t);
		delay_ms(2000);
		rightSignalClose(role_state_adjust_t);
		delay_ms(2000);
		rightSignalOpen(role_state_adjust_t);
		delay_ms(2000);
		rightSignalClose(role_state_adjust_t);

		role_state_adjust_t->right_signal_i =0;

	}
	else if(!role_state_adjust_t->right_signal_i){

		rightSignalClose(role_state_adjust_t);

	}

	//////////
	if(role_state_adjust_t->stop_signal_i){

		stopSignalOpen(role_state_adjust_t);

	}
	else if(!role_state_adjust_t->stop_signal_i){

		stopSignalClose(role_state_adjust_t);


	}


	////////////
	if(role_state_adjust_t->emergency_signal_i){

			emergencySignalOpen(role_state_adjust_t);

		}
		else if(!role_state_adjust_t->emergency_signal_i){

			emergencySignalClose(role_state_adjust_t);

		}

	if(role_state_adjust_t->front_signal_i){

			frontSignalOpen(role_state_adjust_t);

		}
		else if(!role_state_adjust_t->front_signal_i){

			frontSignalClose(role_state_adjust_t);
		}
};






void delay_ms(int16_t k) {

					int16_t i, j;

					for(i=0; i<k; i++)

						for (j=0; j<3000; j++ ) {

						}
}







