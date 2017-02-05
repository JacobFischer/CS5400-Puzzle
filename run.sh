# HW2: solves puzzle 1 and 2 via ID-DFGS

# default arguments
algorithm="id_dfgs"
puzzles="puzzles/puzzle1.txt puzzles/puzzle2.txt"

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
