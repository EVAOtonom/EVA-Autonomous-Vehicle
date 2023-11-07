################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../modules/break/break.c 

OBJS += \
./modules/break/break.o 

C_DEPS += \
./modules/break/break.d 


# Each subdirectory must supply rules for building sources it contributes
modules/break/%.o modules/break/%.su: ../modules/break/%.c modules/break/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F302x8 -c -I../Core/Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F3xx/Include -I../Drivers/CMSIS/Include -I"C:/Users/EVA Otonom/Desktop/Otonom_Code/modules" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-modules-2f-break

clean-modules-2f-break:
	-$(RM) ./modules/break/break.d ./modules/break/break.o ./modules/break/break.su

.PHONY: clean-modules-2f-break

