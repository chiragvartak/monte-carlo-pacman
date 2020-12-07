#!/bin/bash -x

{

time python -u pacman.py -c --timeout 30 -p MinimaxAgent -l testClassic -a depth=3,evalFn=better -q -n 10
time python -u pacman.py -c --timeout 30 -p AlphaBetaAgent -l testClassic -a depth=3,evalFn=better -q -n 10
time python -u pacman.py -c --timeout 30 -p ExpectimaxAgent -l testClassic -a depth=3,evalFn=better -q -n 10
time python -u pacman.py -c --timeout 30 -p MCTSAgent -l testClassic -q -n 10

time python -u pacman.py -c --timeout 30 -p MinimaxAgent -l small -a depth=3,evalFn=better -q -n 10
time python -u pacman.py -c --timeout 30 -p AlphaBetaAgent -l small -a depth=3,evalFn=better -q -n 10
time python -u pacman.py -c --timeout 30 -p ExpectimaxAgent -l small -a depth=3,evalFn=better -q -n 10
time python -u pacman.py -c --timeout 30 -p MCTSAgent -l small -q -n 10

time python -u pacman.py -c --timeout 30 -p MinimaxAgent -l medium -a depth=3,evalFn=better -q -n 10
time python -u pacman.py -c --timeout 30 -p AlphaBetaAgent -l medium -a depth=3,evalFn=better -q -n 10
time python -u pacman.py -c --timeout 30 -p ExpectimaxAgent -l medium -a depth=3,evalFn=better -q -n 10
time python -u pacman.py -c --timeout 30 -p MCTSAgent -l medium -q -n 10

# No point - they all time out
time python -u pacman.py -c --timeout 30 -p MinimaxAgent -l bigClassic -a depth=2 -q -n 1
time python -u pacman.py -c --timeout 30 -p AlphaBetaAgent -l bigClassic -a depth=2 -q -n 1
time python -u pacman.py -c --timeout 30 -p ExpectimaxAgent -l bigClassic -a depth=2 -q -n 1
time python -u pacman.py -c --timeout 30 -p MCTSAgent -l bigClassic -q -n 10



} >test.log 2>&1