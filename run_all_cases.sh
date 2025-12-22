#!/bin/bash

#./run_all_cases.sh

# Values to sweep
TRIP_ENDS=(25 50 75 100 125 150)
INTERSECTIONS=(2 3 4 5 6 7 8 9 10)

# Optional: create a log directory
LOG_DIR="uart_logs"
mkdir -p "${LOG_DIR}"

for TRIP_END in "${TRIP_ENDS[@]}"; do
    for RAW_INT in "${INTERSECTIONS[@]}"; do
        for COL_INT in "${INTERSECTIONS[@]}"; do

            LOG_FILE="${LOG_DIR}/UART_Log_trip${TRIP_END}_raw${RAW_INT}_col${COL_INT}.txt"

            echo "===================================================="
            echo "Running case:"
            echo "  trip-end = ${TRIP_END}"
            echo "  raw-int  = ${RAW_INT}"
            echo "  col-int  = ${COL_INT}"
            echo "  log      = ${LOG_FILE}"
            echo "===================================================="

            python3 main.py ... | tee "${LOG_FILE}" || echo "FAILED case: trip=${TRIP_END}, raw=${RAW_INT}, col=${COL_INT}"


        done
    done
done
