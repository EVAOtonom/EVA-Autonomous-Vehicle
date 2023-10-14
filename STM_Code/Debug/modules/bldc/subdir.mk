################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../modules/bldc/bldc.c 

OBJS += \
./modules/bldc/bldc.o 

C_DEPS += \
./modules/bldc/bldc.d 


# Each subdirectory must supply rules for building sources it contributes
modules/bldc/%.o modules/bldc/%.su modules/bldc/%.cyclo: ../modules/bldc/%.c modules/bldc/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F302x8 -c -I../Core/Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F3xx/Include -I../Drivers/CMSIS/Include -I"C:/Users/EVA Otonom/STM32CubeIDE/workspace_1.13.2/Otonom_Code/modules" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-modules-2f-bldc

clean-modules-2f-bldc:
	-$(RM) ./modules/bldc/bldc.cyclo ./modules/bldc/bldc.d ./modules/bldc/bldc.o ./modules/bldc/bldc.su

.PHONY: clean-modules-2f-bldc

