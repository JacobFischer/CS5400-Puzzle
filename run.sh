# HW2: solves puzzle 1-4 via A* GS

# default arguments
algorithm="astar_gs"
puzzles="puzzles/puzzle1.txt puzzles/puzzle2.txt puzzles/puzzle3.txt puzzles/puzzle4.txt"

# command line arg overrides
if [ -n "$1" ]; then
    algorithm="$1"
fi

if [ -n "$2" ]; then
    puzzles="${@:2}"
fi

echo "Algorithm: $algorithm"
echo "Puzzles: $puzzles"
echo "====================================================================="

for puzzle in $puzzles; do
    echo "---------------------------------------------------------------------"
    echo "Running program with algorithm '$algorithm' for puzzle '$puzzle'"
    echo ""
    python3 ./src/main.py $algorithm $puzzle
done
