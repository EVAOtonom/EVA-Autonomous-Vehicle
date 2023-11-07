/*
 * modbus.c
 *
 *  Created on: 20 Eki 2023
 *      Author: hp
 */


#include "modbus.h"
#include <string.h>
#include "modbus_crc.h"
#include <stdbool.h>
modbusControl_t modbus;

void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *huart, uint16_t Size)
{
  /* Prevent unused argument(s) compilation warning */
	modbus.reciveDataLength = Size;
	HAL_UARTEx_ReceiveToIdle_IT(&huart1, modbus.reciveBuffer, sizeof(modbus.reciveBuffer));
	modbusReciveEnable;
	modbus.status = ModbusData_Avaliable;


  /* NOTE : This function should not be modified, when the callback is needed,
            the HAL_UARTEx_RxEventCallback can be implemented in the user file.
   */
}

void modbus_Init(modbusRegister_t *ModbusRegisters){
	modbusReciveEnable;
	modbus.modbusRegisters = ModbusRegisters;
	modbus.slaveID = MODBUS_SLAVE_ID;
	HAL_UARTEx_ReceiveToIdle_IT(&huart1, modbus.reciveBuffer, sizeof(modbus.reciveBuffer));
}
//Clear Recive Buffer
static void modbusClearReciveBuffer(){
	modbus.status = ModbusData_NotAvaliable;
	memset(modbus.reciveBuffer,0,sizeof(modbus.reciveBuffer));
}
static void modbusClearSendBuffer(){
	memset(modbus.reciveBuffer,0,sizeof(modbus.sendBuffer));
}
static bool modbusCheckRecivedCRC(){
	uint8_t reciveCrcH = 0;
	uint8_t reciveCrcL = 0;
	uint16_t reciveCrc  = 0;
	reciveCrcH = modbus.reciveBuffer[modbus.reciveDataLength-1];
	reciveCrcL = modbus.reciveBuffer[modbus.reciveDataLength-2];
	reciveCrc  = ((reciveCrcH & 0xFF) << 8) | (reciveCrcL & 0xFF);
	modbus.crc_Recive.crc16 = crc16(modbus.reciveBuffer, modbus.reciveDataLength-2);
	if(modbus.crc_Recive.crc16 == reciveCrc){
		return true;
	}
	else
	{
		return false;
	}
}
static void modbusCalculateSendedCRC(uint16_t Length){
	modbus.crc_Send.crc16 = crc16(modbus.sendBuffer, Length);
}
static void modbusReadHoldingRegisterFunction(){
	uint8_t  counter          = 0;
	uint16_t byteCount        = 0;
	uint16_t reciveDataLength = 0;

	uint32_t wantedRegisterAdress     = 0;
	uint32_t wantedRegisterQuantity   = 0;
	reciveDataLength = modbus.reciveDataLength;
	// Find the number of byte to send for response
	byteCount = ((modbus.reciveBuffer[reciveDataLength-4] &0xFF) << 8) | ((modbus.reciveBuffer[reciveDataLength-3] &0xFF));
	// Find WantedRegisterAdress
	wantedRegisterAdress = (modbus.reciveBuffer[2] & 0xFF << 8) | (modbus.reciveBuffer[3] & 0xFF);
	// Find WantedRegisterQuantity
	wantedRegisterQuantity = (modbus.reciveBuffer[4] & 0xFF << 8) | (modbus.reciveBuffer[5] & 0xFF);
	modbus.sendBuffer[counter++] = modbus.slaveID;
	modbus.sendBuffer[counter++] = modbusFunctionReadHoldinRegister;
	modbus.sendBuffer[counter++] = ((byteCount)& 0xFF) * 2;
	for (int i = 0; i < wantedRegisterQuantity; ++i) {
		if(modbus.modbusRegisters[i].modbusregister == 0)
		{
			modbus.sendBuffer[counter++] = 0;
			modbus.sendBuffer[counter++] = 0;
		}
		else
		{
			modbus.sendBuffer[counter++] = ((*modbus.modbusRegisters[wantedRegisterAdress + i].modbusregister) >> 8) & 0xFF;
			modbus.sendBuffer[counter++] = ((*modbus.modbusRegisters[wantedRegisterAdress + i].modbusregister) & 0xFF);
		}
	}
	modbusCalculateSendedCRC(counter);
	modbus.sendBuffer[counter++] = modbus.crc_Send.bytes.LSB;
	modbus.sendBuffer[counter++] = modbus.crc_Send.bytes.MSB;
	modbusSendEnable;
	HAL_UART_Transmit(&huart1, modbus.sendBuffer, counter, HAL_MAX_DELAY);
	modbusReciveEnable;
	modbusClearSendBuffer();
}
static void modbusWriteMultipleRegisterFunction(){
	uint8_t  counter          = 0;
	//uint16_t byteCount        = 0;
	//uint16_t reciveDataLength = 0;
	//reciveDataLength = modbus.reciveDataLength;
	uint32_t wantedRegisterAdress     = 0;
	uint32_t wantedRegisterQuantity   = 0;

	// Find WantedRegisterAdress
	wantedRegisterAdress = (modbus.reciveBuffer[2] & 0xFF << 8) | (modbus.reciveBuffer[3] & 0xFF);
	// Find WantedRegisterQuantity
	wantedRegisterQuantity = (modbus.reciveBuffer[4] & 0xFF << 8) | (modbus.reciveBuffer[5] & 0xFF);
	for (int i = 0; i < wantedRegisterQuantity; ++i) {
		*modbus.modbusRegisters[i+wantedRegisterAdress].modbusregister = (modbus.reciveBuffer[7+(i*2)] & 0xFF) << 8 | (modbus.reciveBuffer[7+(i*2)+1] & 0xFF);

	}
	modbus.sendBuffer[counter++] = modbus.slaveID ;
	modbus.sendBuffer[counter++] = modbusFunctionWriteMultipleRegister;
	modbus.sendBuffer[counter++] = (wantedRegisterAdress >> 8) & 0xFF;
	modbus.sendBuffer[counter++] = (wantedRegisterAdress & 0xFF);
	modbus.sendBuffer[counter++] = (wantedRegisterQuantity >> 8) & 0xFF;
	modbus.sendBuffer[counter++] = (wantedRegisterQuantity & 0xFF);
	modbusCalculateSendedCRC(counter);
	modbus.sendBuffer[counter++] = modbus.crc_Send.bytes.LSB;
	modbus.sendBuffer[counter++] = modbus.crc_Send.bytes.MSB;
	modbusSendEnable;
	HAL_UART_Transmit(&huart1, modbus.sendBuffer, counter, HAL_MAX_DELAY);
	modbusReciveEnable;
}
static void modbusWriteSingleRegisterFunction(){
	uint32_t wantedRegisterAdress = 0;
	// Find WantedRegisterAdress
	wantedRegisterAdress = (modbus.reciveBuffer[2] & 0xFF << 8) | (modbus.reciveBuffer[3] & 0xFF);
	// Find WantedRegisterValue
	*modbus.modbusRegisters[wantedRegisterAdress].modbusregister = ((modbus.reciveBuffer[4] & 0xFF) << 8) | ((modbus.reciveBuffer[5] & 0xFF) );
	// Send Same Frame That We get
	modbusSendEnable;
	HAL_UART_Transmit(&huart1, modbus.reciveBuffer, modbus.reciveDataLength, HAL_MAX_DELAY);
	modbusReciveEnable;
}
void modbus_Loop(){
	if(modbus.status == ModbusData_Avaliable){
		//Check Incoming Slave Adres
		if(modbus.reciveBuffer[0] == modbus.slaveID)
		{
			if(modbusCheckRecivedCRC())
			{

			// Check Function Code
				switch (modbus.reciveBuffer[1]) {
					case modbusFunctionReadHoldinRegister:
						modbusReadHoldingRegisterFunction();
						break;
					case modbusFunctionWriteMultipleRegister:
						modbusWriteMultipleRegisterFunction();
						break;
					case modbusFunctionWriteSingleRegister:
						modbusWriteSingleRegisterFunction();
						break;
				}
			}
			else
			{
				//Send CRC is wrong error Code if needed
			}
			modbusClearReciveBuffer();
		}
		else
		{
			modbusClearReciveBuffer();
		}
	}
}
