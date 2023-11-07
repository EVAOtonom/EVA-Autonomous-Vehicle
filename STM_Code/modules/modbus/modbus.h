/*
 * modbus.h
 *
 *  Created on: 20 Eki 2023
 *      Author: hp
 */

#ifndef MODBUS_MODBUS_H_
#define MODBUS_MODBUS_H_

#include "main.h"

#define modbusSendEnable HAL_GPIO_WritePin(RS485_Dir_GPIO_Port, RS485_Dir_Pin, GPIO_PIN_SET);
#define modbusReciveEnable HAL_GPIO_WritePin(RS485_Dir_GPIO_Port, RS485_Dir_Pin, GPIO_PIN_RESET);
#define MODBUS_SLAVE_ID 1
#define MODBUS_REGISTER_NUMBER 30
extern UART_HandleTypeDef huart1;

typedef enum modbusStatus_s{
	ModbusData_NotAvaliable,
	ModbusData_Avaliable
}modbusStatus_e;
typedef enum modbusFunction_s{
	modbusFunctionReadHoldinRegister = 3,
	modbusFunctionWriteSingleRegister = 6,
	modbusFunctionWriteMultipleRegister = 16
}modbusFunction_t;
typedef struct{
	uint8_t LSB;
	uint8_t MSB;
}byte_t;


typedef struct modbusRegister_s{
	int16_t * modbusregister;
}modbusRegister_t;

typedef struct modbusControl_s{
	uint8_t slaveID;
	modbusRegister_t *modbusRegisters;
	uint8_t reciveBuffer[256];
	uint8_t sendBuffer[256];
	uint16_t reciveDataLength;
	modbusStatus_e status;
	union {
		uint16_t crc16;
		byte_t bytes;
	}crc_Recive;
	union {
		uint16_t crc16;
		byte_t bytes;
	}crc_Send;

}modbusControl_t;

void modbus_Init(modbusRegister_t *ModbusRegisters);
void modbus_Loop();

#endif /* MODBUS_MODBUS_H_ */
