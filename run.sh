#!/bin/bash

# Initialize counters
alphaBetaAIWins=0
monteCarloAIWins=0
ties=0 

# Initial seed value
seed=0

for i in {1..20}; do
  if [ $i -le 9 ]; then
    p1="alphaBetaAI"
    p2="monteCarloAI"
    player1="Player 1 ($p1)"
    player2="Player 2 ($p2)"
  else
    if [ $i -eq 9 ]; then
      seed=0
    fi
    p1="monteCarloAI"
    p2="alphaBetaAI"
    player1="Player 1 ($p1)"
    player2="Player 2 ($p2)"
  fi

  echo "Game $i: $player1 vs $player2, Seed: $seed"

  lastLine=$(python3 main.py -p1 $p1 -p2 $p2 -limit_players 1,2 -visualize False -seed $seed | tail -n 1)

  echo "Result: $lastLine"

  if echo "$lastLine" | grep -q "Player  1  has won"; then
    if [ "$p1" == "alphaBetaAI" ]; then
      ((alphaBetaAIWins++))
    else
      ((monteCarloAIWins++))
    fi
  elif echo "$lastLine" | grep -q "Player  2  has won"; then
    if [ "$p2" == "alphaBetaAI" ]; then
      ((alphaBetaAIWins++))
    else
      ((monteCarloAIWins++))
    fi
  elif echo "$lastLine" | grep -q "The game has tied"; then
    ((ties++))
  fi

  let seed=seed+1

  echo ""
done

# Print the total wins for each player and the number of ties
echo "AlphaBetaAI wins: $alphaBetaAIWins"
echo "MonteCarloAI wins: $monteCarloAIWins"
echo "Ties: $ties"
