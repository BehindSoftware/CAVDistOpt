#!/bin/bash

#./analyze_log.sh uart_logs/UART_Log_trip25_raw2_col7.txt

LOGFILE="$1"

if [ -z "$LOGFILE" ]; then
    echo "Usage: $0 <UART_log_file>"
    exit 1
fi

echo "=============================="
echo " ADMM LOG ANALYSIS SUMMARY"
echo "=============================="
echo "Log file: $LOGFILE"
echo

# Total iterations
TOTAL_ITER=$(grep -c "^Iteration:" "$LOGFILE")

# Solution / infeasible counts
SOLUTION_CNT=$(grep -c "\[Result\]:Solution found" "$LOGFILE")
INFEASIBLE_CNT=$(grep -c "\[Result\]:Problem is infeasible" "$LOGFILE")

# Convergence info
CONVERGENCE_CNT=$(grep -c "Convergence reached after" "$LOGFILE")

echo "Total ADMM iterations        : $TOTAL_ITER"
echo "Total solutions found        : $SOLUTION_CNT"
echo "Total infeasible problems    : $INFEASIBLE_CNT"
echo "Total convergences           : $CONVERGENCE_CNT"
echo

# echo "---- Convergence details ----"
# grep "Convergence reached after" "$LOGFILE" | \
# awk -F'after | iterations' '{print "Converged after iteration:", $2}'

# echo
# echo "---- Per-case summary ----"

# awk '
# /\*Summarize\*/ {
#     case_id++
#     iter=0
#     sol=0
#     inf=0
#     conv=-1
# }

# /^Iteration:/ { iter++ }

# /\[Result\]:Solution found/ { sol++ }

# /\[Result\]:Problem is infeasible/ { inf++ }

# /Convergence reached after/ {
#     match($0, /after ([0-9]+)/, a)
#     conv=a[1]
# }

# /^Step/ && case_id>0 {
#     printf("Case %d | Iterations: %d | Solutions: %d | Infeasible: %d | Converged: ",
#            case_id, iter, sol, inf)
#     if (conv >= 0)
#         printf("YES (%d iters)\n", conv)
#     else
#         printf("NO\n")
#     iter=0; sol=0; inf=0; conv=-1
# }
# END {
#     if (case_id > 0) {
#         printf("Case %d | Iterations: %d | Solutions: %d | Infeasible: %d | Converged: ",
#                case_id, iter, sol, inf)
#         if (conv >= 0)
#             printf("YES (%d iters)\n", conv)
#         else
#             printf("NO\n")
#     }
# }
# ' "$LOGFILE"
