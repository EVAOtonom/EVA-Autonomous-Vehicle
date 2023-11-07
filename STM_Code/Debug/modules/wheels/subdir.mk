################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../modules/wheels/wheel.c 

OBJS += \
./modules/wheels/wheel.o 

C_DEPS += \
./modules/wheels/wheel.d 


# Each subdirectory must supply rules for building sources it contributes
modules/wheels/%.o modules/wheels/%.su: ../modules/wheels/%.c modules/wheels/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F302x8 -c -I../Core/Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F3xx/Include -I../Drivers/CMSIS/Include -I"C:/Users/EVA Otonom/Desktop/Otonom_Code/modules" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-modules-2f-wheels

clean-modules-2f-wheels:
	-$(RM) ./modules/wheels/wheel.d ./modules/wheels/wheel.o ./modules/wheels/wheel.su

.PHONY: clean-modules-2f-wheels

