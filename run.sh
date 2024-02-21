#!/bin/bash

# Initialize counters
alphaBetaAIWins=0
monteCarloAIWins=0
ties=0 # Counter for ties

# Initial seed value
seed=1

for i in {1..20}; do
  # For the first 10 iterations
  if [ $i -le 10 ]; then
    p1="alphaBetaAI"
    p2="monteCarloAI"
    player1="Player 1 ($p1)"
    player2="Player 2 ($p2)"
  else
    # Switch players after 10 iterations and reset seed
    if [ $i -eq 11 ]; then
      seed=1
    fi
    p1="monteCarloAI"
    p2="alphaBetaAI"
    player1="Player 1 ($p1)"
    player2="Player 2 ($p2)"
  fi

  # Echo current game setup including player and seed
  echo "Game $i: $player1 vs $player2, Seed: $seed"

  # Execute and capture the game output, then extract the last line
  lastLine=$(python3 main.py -p1 $p1 -p2 $p2 -limit_players 1,2 -visualize False -seed $seed | tail -n 1)

  # Echo the last line for terminal visibility
  echo "Result: $lastLine"

  # Check for the winner and increment the appropriate counter based on the last line
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
  elif echo "$lastLine" | grep -q "The game has tied"; then # Check for a tie
    ((ties++)) # Increment the tie counter
  fi

  # Increment the seed for the next iteration
  let seed=seed+1

  # Add a newline for better readability between games
  echo ""
done

# Print the total wins for each player and the number of ties
echo "AlphaBetaAI wins: $alphaBetaAIWins"
echo "MonteCarloAI wins: $monteCarloAIWins"
echo "Ties: $ties"
