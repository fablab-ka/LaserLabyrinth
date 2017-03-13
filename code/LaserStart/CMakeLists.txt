#==================== PROJECT CONFIGURATION ===========================================
PROJECT(LaserStart)

set(FILE_NAME ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${PROJECT_NAME})

# ========= CHIP AND FREQUENY ==============

SET(DEVICE "attiny45")
SET(FREQ "8000000")

# Tell the compiler about these setttings
SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mmcu=${DEVICE} -DF_CPU=${FREQ}UL")

#=========================== AVRDUDE LOCAL CONFIG =========================================

set(CHIP t45)
set(PORT usb)

#========================= SOURCE FILES IN HERE  ===========================================
SET(SOURCE_FILES
        ../usi_uart.c
        ../LaserBoth/main.c)

#======================= COMPILING AND STUFF ===================================================

MESSAGE("Compiling Project: ${PROJECT_NAME}")
ADD_EXECUTABLE(${PROJECT_NAME} ${SOURCE_FILES})

avr_compile(${PROJECT_NAME} ${FILE_NAME})