CMAKE_MINIMUM_REQUIRED(VERSION 3.5)
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_VERBOSE_MAKEFILE ON)

SET(VERSION_MAJOR 1)
SET(VERSION_MINOR 0)

# HACK, for wierd rdynamic error
set(CMAKE_SHARED_LIBRARY_LINK_C_FLAGS "")
set(CMAKE_SHARED_LIBRARY_LINK_CXX_FLAGS "")

# ========================== OS (user) specific configuration ==================================


SET(AVR_BIN "/usr/bin/")  # <-- Toolchain
SET(EXTENSION "")
SET(AVRDUDE avrdude)
SET(RM rm)
set(PROGRAMMER stk500)


SET(AVR_OBJCOPY ${AVR_BIN}avr-objcopy${EXTENSION})
SET(AVR_SIZE ${AVR_BIN}avr-size${EXTENSION})
SET(AVR_GCC ${AVR_BIN}avr-gcc${EXTENSION})
SET(AVR_GXX ${AVR_BIN}avr-g++${EXTENSION})
SET(AVR_STRIP ${AVR_BIN}avr-strip${EXTENSION})

#================== Helper functions ===================================================

function(flash_script pn pdir)
    MESSAGE("Generating Flash script: " ${pn})
    SET(CONTENT "${AVRDUDE} -Uflash:w:${pdir}.hex:a -v -c${PROGRAMMER} -p${CHIP} -P${PORT}")
    SET(CONTENT "#!/usr/bin/env bash\n${CONTENT}")
    FILE(WRITE ${TOP_DIR}flash_${pn}.sh ${CONTENT})
    execute_process(COMMAND chmod +x ${TOP_DIR}flash_${pn}.sh)
endfunction()

function(avr_compile pn pdir)
    ADD_CUSTOM_COMMAND(TARGET ${pn} POST_BUILD COMMAND ${AVR_STRIP} ${pdir} -o ${pdir}.elf)
    ADD_CUSTOM_COMMAND(TARGET ${pn} POST_BUILD COMMAND ${AVR_OBJCOPY} -O ihex -R.eeprom -R .fuse -R .lock -R .signature ${pdir}.elf ${pdir}.hex)
    ADD_CUSTOM_COMMAND(TARGET ${pn} POST_BUILD COMMAND ${AVR_OBJCOPY} -O ihex -j .eeprom --set-section-flags=.eeprom="alloc,load" --change-section-lma .eeprom=0 ${pdir}.elf ${pdir}.eep)
    ADD_CUSTOM_COMMAND(TARGET ${pn} POST_BUILD COMMAND ${AVR_SIZE} ${pdir} --mcu=${DEVICE} --format=avr > ${pdir}.size)
    flash_script(${pn} ${pdir})
    ADD_CUSTOM_COMMAND(TARGET ${pn} POST_BUILD COMMAND ${RM} ${pdir})
endfunction()


# ========= AVRDUDE SETTINGS  =============
SET(PORT usb)               # <-- Welcher Port
SET(CHIP m88p)

SET(CMAKE_C_FLAGS "-std=gnu99 -Wall -Os -fpack-struct -fshort-enums -ffunction-sections -fdata-sections -funsigned-char -funsigned-bitfields -Wl,--gc-sections -Wl,--relax")
SET(CMAKE_EXE_LINKER_FLAGS "-Os -Wl,--gc-sections -Wl,--relax")
SET(CMAKE_C_COMPILER_INIT ${AVR_GCC})
set(CMAKE_C_COMPILER ${AVR_GCC})
set(CMAKE_CXX_COMPILER ${AVR_GXX})
SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
#============== Top level configuration ====================

# Top project directory
SET(CMAKE_BUILD_TYPE Debug)

SET(TOP_DIR ${CMAKE_SOURCE_DIR}/)
SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/bin/")


# ================ Projects go here =================
#

add_subdirectory(LaserStart)
add_subdirectory(LaserBoth)

