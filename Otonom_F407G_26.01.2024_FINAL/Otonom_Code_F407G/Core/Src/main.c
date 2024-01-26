/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2023 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */


/**
 ***************************************************************************************
 *Merhaba arkadaşlar Otonom AKS son kodu aşağıda görüldüğü gibidir lütfen kodlar üstünde (2023-2024)
 *Oynama yapılmamalıdır
 *Berkay Aşık
 *Samet Aygün
 *Kaan Avcı
 *Esma Arhan
 *Emirhan Akdemir tarafından hazırlanmıştır.
 *Everything for my everything
 *
 ***************************************************************************************
 */

/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "usb_host.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "../../modules/wheels/wheel.h"
#include "../../modules/break/break.h"
#include "../../modules/bldc/bldc.h"
#include "../../modules/modbus/modbus.h"
#include "../../modules/role/role.h"
#include "../../modules/manuel/manuel.h"
#include "lwgps/lwgps.h"
#include "usbh_hid.h"


wheel_adjust_t wheelParameters = {0} ;
switchBreak_adjust_t breakParameters = {0};
role_State_Adjust_t roleParameters = {0};
manuel_mode_t manuelParameters = {0};
int16_t back_Encoder = 0;
uint16_t wantedWheelDegree = 0;
int16_t wantedSpeed=0;
int16_t resetBackEncoder =0;
uint8_t setAdc  = 6;
uint8_t setSpeed = 10;
uint8_t pActiveCount = 0;
int16_t isReset=0;
char key;

lwgps_t gps;
uint8_t rx_data = 0;
uint8_t rx_buffer[128];
uint8_t rx_index = 0;

modbusRegister_t ModbusRegister[MODBUS_REGISTER_NUMBER];

#define wheel_offset 0 // Eğer ki offset (0 noktasında encoderın değeri) 0 değil ise değeri -4 ile çarp, +4 ekle ve  wheel_offsetin şuanki durumu ile topla (Direksiyon İçin)



/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
ADC_HandleTypeDef hadc1;

TIM_HandleTypeDef htim1;
TIM_HandleTypeDef htim2;
TIM_HandleTypeDef htim10;
TIM_HandleTypeDef htim12;
TIM_HandleTypeDef htim14;

UART_HandleTypeDef huart1;
UART_HandleTypeDef huart2;
UART_HandleTypeDef huart3;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_TIM1_Init(void);
static void MX_TIM2_Init(void);
static void MX_TIM12_Init(void);
static void MX_TIM14_Init(void);
static void MX_USART1_UART_Init(void);
static void MX_USART2_UART_Init(void);
static void MX_TIM10_Init(void);
static void MX_ADC1_Init(void);
static void MX_USART3_UART_Init(void);
void MX_USB_HOST_Process(void);

/* USER CODE BEGIN PFP */


/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */


void USBH_HID_EventCallback(USBH_HandleTypeDef *phost){


	if (USBH_HID_GetDeviceType(phost)==HID_KEYBOARD){

		HID_KEYBD_Info_TypeDef *keyboardInfo;

		keyboardInfo = USBH_HID_GetKeybdInfo(phost);
		key  =  USBH_HID_GetASCIICode(keyboardInfo);

	}


}


void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
	if(huart == &huart3) {
		if(rx_data != '\n' && rx_index < sizeof(rx_buffer)) {
			rx_buffer[rx_index++] = rx_data;
		} else {
			lwgps_process(&gps, rx_buffer, rx_index+1);
			rx_index = 0;
			rx_data = 0;
		}
	}
	HAL_UART_Receive_IT(&huart3, &rx_data, 1); // Bu if bloğunun içinde olduğundan herhalde data göndermiyor olabilir ama bilmiyorum

}



void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{

	if(htim->Instance == TIM10)
	{

		switchAdjust(&roleParameters);  //Röle ayarlama kodu
		getMode(&manuelParameters);    // Mod ayarlama kodu

//****AUTO RESET CODE BEGIN****//

		if (!HAL_GPIO_ReadPin(AUTO_RESET_GPIO_Port, AUTO_RESET_Pin)) {

					isReset = 1;
				}

//****AUTO RESET CODE END****//


//****JOYSTICK CODE AUTOMODE BEGIN****//

		if(manuelParameters.mod == AUTOMODE){

			adjustBldc(wantedSpeed); // Hız ayarlama kodu

		}

//****JOYSTICK CODE AUTOMODE END****//


//****JOYSTICK CODE BEGIN****//


if(manuelParameters.mod==MANUELMODE || manuelParameters.mod==PRIVATMODE ){

		readAdc_speed(&manuelParameters);


   if(!HAL_GPIO_ReadPin(JOYSTICK_REVERSE_GPIO_Port, JOYSTICK_REVERSE_Pin)){

	   	roleParameters.bldc_signal_i=1;
		delay_ms(100);
		wantedSpeed=0;
		adjustBldc(wantedSpeed);
		delay_ms(100);


		if (manuelParameters.adc_Speed <= 6) {
		wantedSpeed = manuelParameters.adc_Speed;
		adjustBldc(wantedSpeed);
		}
		else if (manuelParameters.adc_Speed > 6 ) {
			wantedSpeed = 6;
			adjustBldc(wantedSpeed);
		}
	}


	if(!HAL_GPIO_ReadPin(JOYSTICK_PRESS_BREAK_GPIO_Port,JOYSTICK_PRESS_BREAK_Pin)){

		wantedSpeed=0;
		adjustBldc(wantedSpeed);
		delay_ms(100);
		breakParameters.pressing_break=1;
		breakAdjust(&breakParameters,&roleParameters);
		breakCheckSwitchStatus(&breakParameters);



	}

	if(!HAL_GPIO_ReadPin(JOYSTICK_RELEASE_BREAK_GPIO_Port,JOYSTICK_RELEASE_BREAK_Pin)){

		wantedSpeed=0;
		adjustBldc(wantedSpeed);
		delay_ms(100);
		breakParameters.pressing_break=0;
		breakAdjust(&breakParameters,&roleParameters);
		breakCheckSwitchStatus(&breakParameters);


	}

//**MANUELMODE CODE BEGIN**//

if(manuelParameters.mod==MANUELMODE){

if(!HAL_GPIO_ReadPin(JOYSTICK_FORWARD_GPIO_Port, JOYSTICK_FORWARD_Pin)){

		roleParameters.bldc_signal_i=0;
		delay_ms(100);
		wantedSpeed=0;
		adjustBldc(wantedSpeed);
		delay_ms(100);

		wantedSpeed = manuelParameters.adc_Speed;
		adjustBldc(wantedSpeed);


	}
}

//**MANUELMODE CODE END**//

//**PRIVATMODE CODE BEGIN**//


if(manuelParameters.mod==PRIVATMODE){

	if(!HAL_GPIO_ReadPin(JOYSTICK_FORWARD_GPIO_Port, JOYSTICK_FORWARD_Pin)){

			roleParameters.bldc_signal_i=0;
			delay_ms(100);
			wantedSpeed=0;
			adjustBldc(wantedSpeed);
			delay_ms(100);

			wantedSpeed = manuelParameters.adc_Speed;
			adjustBldc(wantedSpeed);


		}
	}

//**PRIVATMODE CODE END**//

	}

//****JOYSTICK CODE END****//


//****REMOTECONTROLMODE CODE BEGIN****//

	if(key== 'w' ||key=='W'){

		roleParameters.bldc_signal_i =0;
		adjustBldc(0);
		wantedSpeed = 6;
		adjustBldc(wantedSpeed);

	}

	if(key== 'a' ||key=='A'){


	wheelParameters.wantedDegreeTemp=wheelParameters.wantedDegreeTemp+-1;

	}

	if(key== 'd' ||key=='D'){


			wheelParameters.wantedDegreeTemp=wheelParameters.wantedDegreeTemp+1;

	}

	if(key== 's' ||key=='S'){

		roleParameters.bldc_signal_i =1;
		adjustBldc(0);
		wantedSpeed = 6;
		adjustBldc(wantedSpeed);


	}

	if(key== 'z' ||key=='Z'){

		wantedSpeed = 0;
		adjustBldc(wantedSpeed);
		breakParameters.pressing_break =0;

				}

	if(key== 'x' ||key=='X'){

		wantedSpeed = 0;
		adjustBldc(wantedSpeed);
		breakParameters.pressing_break =1;

			}

	if(key== 'e' ||key=='E'){

		roleParameters.emergency_signal_i=1;

				}

	if(key== 'q' ||key=='Q'){

			isReset=1;

	}





//****REMOTECONTROLMODE END****//


		breakCheckSwitchStatus(&breakParameters);   // BREAK SWITCH CONTROL
		breakAdjust(&breakParameters,&roleParameters);  // BREAK PRESS CONTROL



//****WHEEL CODE BEGIN****//

		//wheel_degree = (GPIOB->IDR >> 4)&0x1FF;
		if(HAL_GPIO_ReadPin(B1_GPIO_Port, B1_Pin)){
			__HAL_TIM_SET_COUNTER(&htim1,0);
			wheelParameters.wantedDegree = 0;
		}

		wheelParameters.wheel_manuel = (((int16_t)__HAL_TIM_GET_COUNTER(&htim1) >> 6)* (-1) );

		 wheelParameters.currrentDegreeTemp = (((GPIOC->IDR) >> 1) & 0x1FF);
		 wheelParameters.currrentDegreeTemp += wheel_offset;
		 if(wheelParameters.currrentDegreeTemp > 180) {
			 wheelParameters.currrentDegreeTemp -= 360;
		 }
		 wheelParameters.currrentDegreeTemp = wheelParameters.currrentDegreeTemp >> 2;
		 wheelParameters.currrentDegree = wheelParameters.currrentDegreeTemp;


		 back_Encoder = ((int16_t)__HAL_TIM_GET_COUNTER(&htim2) / 2.25) ;  // Arka encoder okuma

		if (wheelParameters.wantedDegreeTemp > 40 && (manuelParameters.mod == AUTOMODE || manuelParameters.mod==REMOTECONTROLMODE )){
			wheelParameters.wantedDegreeTemp=40;
			wheelParameters.wantedDegree = 40;
		}
		else if (wheelParameters.wantedDegreeTemp < -40  && (manuelParameters.mod == AUTOMODE || manuelParameters.mod==REMOTECONTROLMODE)){
			wheelParameters.wantedDegreeTemp= -40;

			wheelParameters.wantedDegree = -40;
		}
		else if (manuelParameters.mod == AUTOMODE) {
			wheelParameters.wantedDegree= wheelParameters.wantedDegreeTemp;
		}
		else if (wheelParameters.wheel_manuel > 40 && (manuelParameters.mod == MANUELMODE ||  manuelParameters.mod == PRIVATMODE)) {
			wheelParameters.wantedDegree = 40;

		}
		else if (wheelParameters.wheel_manuel < -40  && (manuelParameters.mod == MANUELMODE ||  manuelParameters.mod == PRIVATMODE)) {
					wheelParameters.wantedDegree = -40;
		}

		else {
			wheelParameters.wantedDegree = wheelParameters.wheel_manuel;

		}
		if(wheelParameters.wantedDegree > wheelParameters.currrentDegree)
		{

			if(wheelParameters.status != TurningRight)
			{
				//Turn Wheel Right
				//Call Function that turn wheel Right
				wheelParameters.status = TurningRight;
				wheelTurnRight(&wheelParameters);
			}
		}
		else if(wheelParameters.wantedDegree < wheelParameters.currrentDegree)
		{

			if(wheelParameters.status != TurningLeft)
			{
				//Turn Wheel Left
				//Call Function that turn wheels Left
				wheelParameters.status = TurningLeft;
				wheelTurnLeft(&wheelParameters);
			}
		}
		else
		{
			//Stop Turn Right Command And Left Command
			if(wheelParameters.status != NoTurning)
			{
				//Stop Wheel
				//Call Function Stop wheels
				wheelParameters.status = NoTurning;
				wheelStop(&wheelParameters);
			}
		}



	}

}

//****WHEEL CODE END****//

//****ADJUST MODBUS REGISTER BEGIN****//

void pointerWorks(){

	ModbusRegister[0].modbusregister = &wheelParameters.wantedDegreeTemp;
	ModbusRegister[1].modbusregister = &breakParameters.pressing_break;
	ModbusRegister[2].modbusregister = &wantedSpeed;
	ModbusRegister[3].modbusregister = &wheelParameters.currrentDegree;
	ModbusRegister[4].modbusregister = (int16_t *)breakParameters.switchStatus_press;
	ModbusRegister[5].modbusregister = (int16_t *)breakParameters.switchStatus_release;
	ModbusRegister[6].modbusregister = &back_Encoder;
	ModbusRegister[7].modbusregister = &roleParameters.bldc_signal_i;
	ModbusRegister[8].modbusregister = &roleParameters.left_signal_i;
	ModbusRegister[9].modbusregister = &roleParameters.right_signal_i;
	ModbusRegister[10].modbusregister = &roleParameters.emergency_signal_i;
	ModbusRegister[11].modbusregister = &roleParameters.front_signal_i;
	ModbusRegister[12].modbusregister = (int16_t *)&manuelParameters.mod;
	ModbusRegister[13].modbusregister = &resetBackEncoder;
	ModbusRegister[14].modbusregister = (int16_t *)&gps.latitude;
	ModbusRegister[15].modbusregister = (int16_t *)&gps.longitude;
	ModbusRegister[16].modbusregister = (int16_t *)&gps.speed;
	ModbusRegister[17].modbusregister = (int16_t *)&gps.altitude;
	ModbusRegister[18].modbusregister = (int16_t *)&gps.is_valid;


}
//****ADJUST MODBUS REGISTER END****//


/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_TIM1_Init();
  MX_TIM2_Init();
  MX_TIM12_Init();
  MX_TIM14_Init();
  MX_USART1_UART_Init();
  MX_USART2_UART_Init();
  MX_USB_HOST_Init();
  MX_TIM10_Init();
  MX_ADC1_Init();
  MX_USART3_UART_Init();
  /* USER CODE BEGIN 2 */
  HAL_TIM_Encoder_Start_IT(&htim1, TIM_CHANNEL_ALL);
  HAL_TIM_Encoder_Start_IT(&htim2, TIM_CHANNEL_ALL);
  HAL_TIM_Base_Start_IT(&htim10);
  wheelInit();
  bldcInit();
  breakInit();
  pointerWorks();
  modbus_Init(ModbusRegister);
  HAL_ADC_Init(&hadc1);
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_0, GPIO_PIN_RESET);
  lwgps_init(&gps);
  HAL_UART_Receive_IT(&huart3, &rx_data, 1);


  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
	    MX_USB_HOST_Process();

	    modbus_Loop();   //MODBUS COMMUNACATION BEGIN

	     if(isReset ==1){

	    			wheelParameters.wantedDegreeTemp=0;
	    			breakParameters.pressing_break=0;
	    			__HAL_TIM_SET_COUNTER(&htim2,0);
	    			isReset=0;

	    		}
	    		if(resetBackEncoder==1){
	    			__HAL_TIM_SET_COUNTER(&htim2,0);
	    			roleParameters.bldc_signal_i=0;
	    			resetBackEncoder=0;
	    		}


    /* USER CODE END WHILE */
    MX_USB_HOST_Process();

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_BYPASS;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 8;
  RCC_OscInitStruct.PLL.PLLN = 336;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 7;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief ADC1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_ADC1_Init(void)
{

  /* USER CODE BEGIN ADC1_Init 0 */

  /* USER CODE END ADC1_Init 0 */

  ADC_ChannelConfTypeDef sConfig = {0};

  /* USER CODE BEGIN ADC1_Init 1 */

  /* USER CODE END ADC1_Init 1 */

  /** Configure the global features of the ADC (Clock, Resolution, Data Alignment and number of conversion)
  */
  hadc1.Instance = ADC1;
  hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
  hadc1.Init.Resolution = ADC_RESOLUTION_8B;
  hadc1.Init.ScanConvMode = DISABLE;
  hadc1.Init.ContinuousConvMode = ENABLE;
  hadc1.Init.DiscontinuousConvMode = DISABLE;
  hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
  hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
  hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  hadc1.Init.NbrOfConversion = 1;
  hadc1.Init.DMAContinuousRequests = DISABLE;
  hadc1.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
  if (HAL_ADC_Init(&hadc1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time.
  */
  sConfig.Channel = ADC_CHANNEL_6;
  sConfig.Rank = 1;
  sConfig.SamplingTime = ADC_SAMPLETIME_3CYCLES;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN ADC1_Init 2 */

  /* USER CODE END ADC1_Init 2 */

}

/**
  * @brief TIM1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM1_Init(void)
{

  /* USER CODE BEGIN TIM1_Init 0 */

  /* USER CODE END TIM1_Init 0 */

  TIM_Encoder_InitTypeDef sConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM1_Init 1 */

  /* USER CODE END TIM1_Init 1 */
  htim1.Instance = TIM1;
  htim1.Init.Prescaler = 0;
  htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim1.Init.Period = 65535;
  htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim1.Init.RepetitionCounter = 0;
  htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  sConfig.EncoderMode = TIM_ENCODERMODE_TI12;
  sConfig.IC1Polarity = TIM_ICPOLARITY_RISING;
  sConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;
  sConfig.IC1Prescaler = TIM_ICPSC_DIV1;
  sConfig.IC1Filter = 0;
  sConfig.IC2Polarity = TIM_ICPOLARITY_RISING;
  sConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;
  sConfig.IC2Prescaler = TIM_ICPSC_DIV1;
  sConfig.IC2Filter = 0;
  if (HAL_TIM_Encoder_Init(&htim1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM1_Init 2 */

  /* USER CODE END TIM1_Init 2 */

}

/**
  * @brief TIM2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM2_Init(void)
{

  /* USER CODE BEGIN TIM2_Init 0 */

  /* USER CODE END TIM2_Init 0 */

  TIM_Encoder_InitTypeDef sConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM2_Init 1 */

  /* USER CODE END TIM2_Init 1 */
  htim2.Instance = TIM2;
  htim2.Init.Prescaler = 0;
  htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim2.Init.Period = 4294967295;
  htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  sConfig.EncoderMode = TIM_ENCODERMODE_TI1;
  sConfig.IC1Polarity = TIM_ICPOLARITY_RISING;
  sConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;
  sConfig.IC1Prescaler = TIM_ICPSC_DIV1;
  sConfig.IC1Filter = 0;
  sConfig.IC2Polarity = TIM_ICPOLARITY_RISING;
  sConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;
  sConfig.IC2Prescaler = TIM_ICPSC_DIV1;
  sConfig.IC2Filter = 0;
  if (HAL_TIM_Encoder_Init(&htim2, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim2, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM2_Init 2 */

  /* USER CODE END TIM2_Init 2 */

}

/**
  * @brief TIM10 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM10_Init(void)
{

  /* USER CODE BEGIN TIM10_Init 0 */

  /* USER CODE END TIM10_Init 0 */

  /* USER CODE BEGIN TIM10_Init 1 */

  /* USER CODE END TIM10_Init 1 */
  htim10.Instance = TIM10;
  htim10.Init.Prescaler = 336-1;
  htim10.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim10.Init.Period = 100-1;
  htim10.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim10.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim10) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM10_Init 2 */

  /* USER CODE END TIM10_Init 2 */

}

/**
  * @brief TIM12 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM12_Init(void)
{

  /* USER CODE BEGIN TIM12_Init 0 */

  /* USER CODE END TIM12_Init 0 */

  TIM_OC_InitTypeDef sConfigOC = {0};

  /* USER CODE BEGIN TIM12_Init 1 */

  /* USER CODE END TIM12_Init 1 */
  htim12.Instance = TIM12;
  htim12.Init.Prescaler = 336-1;
  htim12.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim12.Init.Period = 100-1;
  htim12.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim12.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_PWM_Init(&htim12) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 0;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  if (HAL_TIM_PWM_ConfigChannel(&htim12, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_ConfigChannel(&htim12, &sConfigOC, TIM_CHANNEL_2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM12_Init 2 */

  /* USER CODE END TIM12_Init 2 */
  HAL_TIM_MspPostInit(&htim12);

}

/**
  * @brief TIM14 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM14_Init(void)
{

  /* USER CODE BEGIN TIM14_Init 0 */

  /* USER CODE END TIM14_Init 0 */

  TIM_OC_InitTypeDef sConfigOC = {0};

  /* USER CODE BEGIN TIM14_Init 1 */

  /* USER CODE END TIM14_Init 1 */
  htim14.Instance = TIM14;
  htim14.Init.Prescaler = 840-1;
  htim14.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim14.Init.Period = 100-1;
  htim14.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim14.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim14) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_PWM_Init(&htim14) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 0;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  if (HAL_TIM_PWM_ConfigChannel(&htim14, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM14_Init 2 */

  /* USER CODE END TIM14_Init 2 */
  HAL_TIM_MspPostInit(&htim14);

}

/**
  * @brief USART1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART1_UART_Init(void)
{

  /* USER CODE BEGIN USART1_Init 0 */

  /* USER CODE END USART1_Init 0 */

  /* USER CODE BEGIN USART1_Init 1 */

  /* USER CODE END USART1_Init 1 */
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 38400;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART1_Init 2 */

  /* USER CODE END USART1_Init 2 */

}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * @brief USART3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART3_UART_Init(void)
{

  /* USER CODE BEGIN USART3_Init 0 */

  /* USER CODE END USART3_Init 0 */

  /* USER CODE BEGIN USART3_Init 1 */

  /* USER CODE END USART3_Init 1 */
  huart3.Instance = USART3;
  huart3.Init.BaudRate = 9600;
  huart3.Init.WordLength = UART_WORDLENGTH_8B;
  huart3.Init.StopBits = UART_STOPBITS_1;
  huart3.Init.Parity = UART_PARITY_NONE;
  huart3.Init.Mode = UART_MODE_TX_RX;
  huart3.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart3.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart3) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART3_Init 2 */

  /* USER CODE END USART3_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOE_CLK_ENABLE();
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOE, CS_I2C_SPI_Pin|FrenPWM_L_Pin|FrenPWM_R_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(OTG_FS_PowerSwitchOn_GPIO_Port, OTG_FS_PowerSwitchOn_Pin, GPIO_PIN_SET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, FrenEn_L_Pin|FrenEn_R_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOD, DireksiyonEn_L_Pin|DireksiyonEn_R_Pin|LD4_Pin|LD3_Pin
                          |LD5_Pin|LD6_Pin|LEFT_SIGNAL_Pin|RIGHT_SIGNAL_Pin
                          |EMERGENCY_SIGNAL_Pin|Audio_RST_Pin|FRONT_LAMB_Pin|STOP_SIGNAL_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(BLDC_ROLE_GPIO_Port, BLDC_ROLE_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(RS485_Dir_GPIO_Port, RS485_Dir_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pins : JOYSTICK_PRESS_BREAK_Pin JOYSTICK_RELEASE_BREAK_Pin AUTO_RESET_Pin FrenSwitch_Press_Pin
                           FrenSwitch_Release_Pin JOYSTICK_FORWARD_Pin JOYSTICK_REVERSE_Pin */
  GPIO_InitStruct.Pin = JOYSTICK_PRESS_BREAK_Pin|JOYSTICK_RELEASE_BREAK_Pin|AUTO_RESET_Pin|FrenSwitch_Press_Pin
                          |FrenSwitch_Release_Pin|JOYSTICK_FORWARD_Pin|JOYSTICK_REVERSE_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GPIOE, &GPIO_InitStruct);

  /*Configure GPIO pins : CS_I2C_SPI_Pin FrenPWM_L_Pin FrenPWM_R_Pin */
  GPIO_InitStruct.Pin = CS_I2C_SPI_Pin|FrenPWM_L_Pin|FrenPWM_R_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOE, &GPIO_InitStruct);

  /*Configure GPIO pin : OTG_FS_PowerSwitchOn_Pin */
  GPIO_InitStruct.Pin = OTG_FS_PowerSwitchOn_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(OTG_FS_PowerSwitchOn_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : Absolute_1_Pin Absolute_2_Pin Absolute_3_Pin Absolute_4_Pin
                           Absolute_5_Pin Absolute_6_Pin Absolute_7_Pin Absolute_8_Pin
                           Absolute_9_Pin */
  GPIO_InitStruct.Pin = Absolute_1_Pin|Absolute_2_Pin|Absolute_3_Pin|Absolute_4_Pin
                          |Absolute_5_Pin|Absolute_6_Pin|Absolute_7_Pin|Absolute_8_Pin
                          |Absolute_9_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_EVT_RISING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : FrenEn_L_Pin FrenEn_R_Pin */
  GPIO_InitStruct.Pin = FrenEn_L_Pin|FrenEn_R_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : BOOT1_Pin */
  GPIO_InitStruct.Pin = BOOT1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(BOOT1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : MANUEL_SWITCH_Pin MANUEL_SWITCH2_Pin ECO_MODE_Pin TURBO_MODE_Pin */
  GPIO_InitStruct.Pin = MANUEL_SWITCH_Pin|MANUEL_SWITCH2_Pin|ECO_MODE_Pin|TURBO_MODE_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pins : DireksiyonEn_L_Pin DireksiyonEn_R_Pin LD4_Pin LD3_Pin
                           LD5_Pin LD6_Pin Audio_RST_Pin */
  GPIO_InitStruct.Pin = DireksiyonEn_L_Pin|DireksiyonEn_R_Pin|LD4_Pin|LD3_Pin
                          |LD5_Pin|LD6_Pin|Audio_RST_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

  /*Configure GPIO pin : BLDC_ROLE_Pin */
  GPIO_InitStruct.Pin = BLDC_ROLE_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(BLDC_ROLE_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : LEFT_SIGNAL_Pin RIGHT_SIGNAL_Pin FRONT_LAMB_Pin STOP_SIGNAL_Pin */
  GPIO_InitStruct.Pin = LEFT_SIGNAL_Pin|RIGHT_SIGNAL_Pin|FRONT_LAMB_Pin|STOP_SIGNAL_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLDOWN;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

  /*Configure GPIO pin : EMERGENCY_SIGNAL_Pin */
  GPIO_InitStruct.Pin = EMERGENCY_SIGNAL_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(EMERGENCY_SIGNAL_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : OTG_FS_OverCurrent_Pin */
  GPIO_InitStruct.Pin = OTG_FS_OverCurrent_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(OTG_FS_OverCurrent_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : RS485_Dir_Pin */
  GPIO_InitStruct.Pin = RS485_Dir_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(RS485_Dir_GPIO_Port, &GPIO_InitStruct);

  /* EXTI interrupt init*/
  HAL_NVIC_SetPriority(EXTI1_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(EXTI1_IRQn);

  HAL_NVIC_SetPriority(EXTI2_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(EXTI2_IRQn);

  HAL_NVIC_SetPriority(EXTI3_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(EXTI3_IRQn);

  HAL_NVIC_SetPriority(EXTI4_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(EXTI4_IRQn);

  HAL_NVIC_SetPriority(EXTI9_5_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(EXTI9_5_IRQn);

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{


}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
