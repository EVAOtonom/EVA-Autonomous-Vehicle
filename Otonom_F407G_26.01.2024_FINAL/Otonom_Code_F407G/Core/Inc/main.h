/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
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
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f4xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

typedef enum status_s {
	NoTurning,
	TurningRight,
	TurningLeft

}status_t;
typedef struct wheel_adjust_s{
	int16_t wantedDegree;
	int16_t wantedDegreeTemp;
	int16_t wheel_manuel;
	int16_t currrentDegree;
	int16_t currrentDegreeTemp;
	status_t status;
}wheel_adjust_t;





/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define JOYSTICK_PRESS_BREAK_Pin GPIO_PIN_2
#define JOYSTICK_PRESS_BREAK_GPIO_Port GPIOE
#define CS_I2C_SPI_Pin GPIO_PIN_3
#define CS_I2C_SPI_GPIO_Port GPIOE
#define JOYSTICK_RELEASE_BREAK_Pin GPIO_PIN_4
#define JOYSTICK_RELEASE_BREAK_GPIO_Port GPIOE
#define PC14_OSC32_IN_Pin GPIO_PIN_14
#define PC14_OSC32_IN_GPIO_Port GPIOC
#define PC15_OSC32_OUT_Pin GPIO_PIN_15
#define PC15_OSC32_OUT_GPIO_Port GPIOC
#define PH0_OSC_IN_Pin GPIO_PIN_0
#define PH0_OSC_IN_GPIO_Port GPIOH
#define PH1_OSC_OUT_Pin GPIO_PIN_1
#define PH1_OSC_OUT_GPIO_Port GPIOH
#define OTG_FS_PowerSwitchOn_Pin GPIO_PIN_0
#define OTG_FS_PowerSwitchOn_GPIO_Port GPIOC
#define Absolute_1_Pin GPIO_PIN_1
#define Absolute_1_GPIO_Port GPIOC
#define Absolute_1_EXTI_IRQn EXTI1_IRQn
#define Absolute_2_Pin GPIO_PIN_2
#define Absolute_2_GPIO_Port GPIOC
#define Absolute_2_EXTI_IRQn EXTI2_IRQn
#define Absolute_3_Pin GPIO_PIN_3
#define Absolute_3_GPIO_Port GPIOC
#define Absolute_3_EXTI_IRQn EXTI3_IRQn
#define B1_Pin GPIO_PIN_0
#define B1_GPIO_Port GPIOA
#define Encoder2Signal2_Pin GPIO_PIN_1
#define Encoder2Signal2_GPIO_Port GPIOA
#define FrenEn_L_Pin GPIO_PIN_4
#define FrenEn_L_GPIO_Port GPIOA
#define FrenEn_R_Pin GPIO_PIN_5
#define FrenEn_R_GPIO_Port GPIOA
#define BLDC_PWM_Pin GPIO_PIN_7
#define BLDC_PWM_GPIO_Port GPIOA
#define Absolute_4_Pin GPIO_PIN_4
#define Absolute_4_GPIO_Port GPIOC
#define Absolute_4_EXTI_IRQn EXTI4_IRQn
#define Absolute_5_Pin GPIO_PIN_5
#define Absolute_5_GPIO_Port GPIOC
#define Absolute_5_EXTI_IRQn EXTI9_5_IRQn
#define BOOT1_Pin GPIO_PIN_2
#define BOOT1_GPIO_Port GPIOB
#define Encoder1Signal1_Pin GPIO_PIN_9
#define Encoder1Signal1_GPIO_Port GPIOE
#define AUTO_RESET_Pin GPIO_PIN_10
#define AUTO_RESET_GPIO_Port GPIOE
#define Encoder1Signal2_Pin GPIO_PIN_11
#define Encoder1Signal2_GPIO_Port GPIOE
#define FrenPWM_L_Pin GPIO_PIN_12
#define FrenPWM_L_GPIO_Port GPIOE
#define FrenPWM_R_Pin GPIO_PIN_13
#define FrenPWM_R_GPIO_Port GPIOE
#define FrenSwitch_Press_Pin GPIO_PIN_14
#define FrenSwitch_Press_GPIO_Port GPIOE
#define FrenSwitch_Release_Pin GPIO_PIN_15
#define FrenSwitch_Release_GPIO_Port GPIOE
#define MANUEL_SWITCH_Pin GPIO_PIN_10
#define MANUEL_SWITCH_GPIO_Port GPIOB
#define MANUEL_SWITCH2_Pin GPIO_PIN_11
#define MANUEL_SWITCH2_GPIO_Port GPIOB
#define ECO_MODE_Pin GPIO_PIN_12
#define ECO_MODE_GPIO_Port GPIOB
#define TURBO_MODE_Pin GPIO_PIN_13
#define TURBO_MODE_GPIO_Port GPIOB
#define DireksiyonPWM_L_Pin GPIO_PIN_14
#define DireksiyonPWM_L_GPIO_Port GPIOB
#define DireksiyonPWM_R_Pin GPIO_PIN_15
#define DireksiyonPWM_R_GPIO_Port GPIOB
#define DireksiyonEn_L_Pin GPIO_PIN_8
#define DireksiyonEn_L_GPIO_Port GPIOD
#define DireksiyonEn_R_Pin GPIO_PIN_9
#define DireksiyonEn_R_GPIO_Port GPIOD
#define LD4_Pin GPIO_PIN_12
#define LD4_GPIO_Port GPIOD
#define LD3_Pin GPIO_PIN_13
#define LD3_GPIO_Port GPIOD
#define LD5_Pin GPIO_PIN_14
#define LD5_GPIO_Port GPIOD
#define LD6_Pin GPIO_PIN_15
#define LD6_GPIO_Port GPIOD
#define Absolute_6_Pin GPIO_PIN_6
#define Absolute_6_GPIO_Port GPIOC
#define Absolute_6_EXTI_IRQn EXTI9_5_IRQn
#define Absolute_7_Pin GPIO_PIN_7
#define Absolute_7_GPIO_Port GPIOC
#define Absolute_7_EXTI_IRQn EXTI9_5_IRQn
#define Absolute_8_Pin GPIO_PIN_8
#define Absolute_8_GPIO_Port GPIOC
#define Absolute_8_EXTI_IRQn EXTI9_5_IRQn
#define Absolute_9_Pin GPIO_PIN_9
#define Absolute_9_GPIO_Port GPIOC
#define Absolute_9_EXTI_IRQn EXTI9_5_IRQn
#define OTG_FS_DM_Pin GPIO_PIN_11
#define OTG_FS_DM_GPIO_Port GPIOA
#define OTG_FS_DP_Pin GPIO_PIN_12
#define OTG_FS_DP_GPIO_Port GPIOA
#define SWDIO_Pin GPIO_PIN_13
#define SWDIO_GPIO_Port GPIOA
#define SWCLK_Pin GPIO_PIN_14
#define SWCLK_GPIO_Port GPIOA
#define Encoder2Signal1_Pin GPIO_PIN_15
#define Encoder2Signal1_GPIO_Port GPIOA
#define BLDC_ROLE_Pin GPIO_PIN_12
#define BLDC_ROLE_GPIO_Port GPIOC
#define LEFT_SIGNAL_Pin GPIO_PIN_0
#define LEFT_SIGNAL_GPIO_Port GPIOD
#define RIGHT_SIGNAL_Pin GPIO_PIN_1
#define RIGHT_SIGNAL_GPIO_Port GPIOD
#define EMERGENCY_SIGNAL_Pin GPIO_PIN_2
#define EMERGENCY_SIGNAL_GPIO_Port GPIOD
#define Audio_RST_Pin GPIO_PIN_4
#define Audio_RST_GPIO_Port GPIOD
#define OTG_FS_OverCurrent_Pin GPIO_PIN_5
#define OTG_FS_OverCurrent_GPIO_Port GPIOD
#define FRONT_LAMB_Pin GPIO_PIN_6
#define FRONT_LAMB_GPIO_Port GPIOD
#define STOP_SIGNAL_Pin GPIO_PIN_7
#define STOP_SIGNAL_GPIO_Port GPIOD
#define SWO_Pin GPIO_PIN_3
#define SWO_GPIO_Port GPIOB
#define RS485_Dir_Pin GPIO_PIN_5
#define RS485_Dir_GPIO_Port GPIOB
#define JOYSTICK_FORWARD_Pin GPIO_PIN_0
#define JOYSTICK_FORWARD_GPIO_Port GPIOE
#define JOYSTICK_REVERSE_Pin GPIO_PIN_1
#define JOYSTICK_REVERSE_GPIO_Port GPIOE

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
