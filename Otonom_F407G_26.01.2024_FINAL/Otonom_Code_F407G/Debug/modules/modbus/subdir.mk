################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../modules/modbus/modbus.c \
../modules/modbus/modbus_crc.c 

OBJS += \
./modules/modbus/modbus.o \
./modules/modbus/modbus_crc.o 

C_DEPS += \
./modules/modbus/modbus.d \
./modules/modbus/modbus_crc.d 


# Each subdirectory must supply rules for building sources it contributes
modules/modbus/%.o modules/modbus/%.su modules/modbus/%.cyclo: ../modules/modbus/%.c modules/modbus/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F407xx -c -I../Core/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -I"C:/Users/hp/STM32CubeIDE/Otonom/Otonom_Code_F407G/modules" -I/Otonom_Code_F407G -I/Otonom_Code_F407G/USB_HOST -I/Otonom_Code_F407G/modules -I/Otonom_Code_F407G/USB_HOST/App -I/Otonom_Code_F407G/USB_HOST/Target -I/Otonom_Code_F407G/Middlewares -I/Otonom_Code_F407G/usb_hid_device -I../USB_HOST/App -I../USB_HOST/Target -I../Middlewares/ST/STM32_USB_Host_Library/Core/Inc -I../Middlewares/ST/STM32_USB_Host_Library/Class/HID/Inc -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-modules-2f-modbus

clean-modules-2f-modbus:
	-$(RM) ./modules/modbus/modbus.cyclo ./modules/modbus/modbus.d ./modules/modbus/modbus.o ./modules/modbus/modbus.su ./modules/modbus/modbus_crc.cyclo ./modules/modbus/modbus_crc.d ./modules/modbus/modbus_crc.o ./modules/modbus/modbus_crc.su

.PHONY: clean-modules-2f-modbus

