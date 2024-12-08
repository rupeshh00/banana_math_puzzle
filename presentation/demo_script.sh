#!/bin/bash

# macOS Screen Recording Script for Banana Math Puzzle Demo

# Set up variables
DEMO_OUTPUT_DIR="$HOME/CascadeProjects/banana_math_puzzle/presentation/demo_output"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
VIDEO_OUTPUT="${DEMO_OUTPUT_DIR}/banana_math_puzzle_demo_${TIMESTAMP}.mp4"
GAME_PATH="$HOME/CascadeProjects/banana_math_puzzle/main.py"

# Create output directory if it doesn't exist
mkdir -p "$DEMO_OUTPUT_DIR"

# Screen Recording Setup
# Use built-in macOS screen recording with ffmpeg
DISPLAY_ID=$(system_profiler SPDisplaysDataType | grep -B 3 "Main Display" | grep "Resolution" | awk '{print $1}')
SCREEN_WIDTH=$(system_profiler SPDisplaysDataType | grep -B 3 "Main Display" | grep "Resolution" | awk -F'x' '{print $1}')
SCREEN_HEIGHT=$(system_profiler SPDisplaysDataType | grep -B 3 "Main Display" | grep "Resolution" | awk -F'x' '{print $2}')

echo "Starting screen recording..."
ffmpeg -f avfoundation -i "0:0" \
    -r 30 \
    -s "${SCREEN_WIDTH}x${SCREEN_HEIGHT}" \
    -vcodec libx264 \
    -preset medium \
    -crf 23 \
    -pix_fmt yuv422p \
    "$VIDEO_OUTPUT" &

FFMPEG_PID=$!

# Wait a moment for recording to start
sleep 2

# Launch Banana Math Puzzle
python3 "$GAME_PATH" &
GAME_PID=$!

# Wait for game to load
sleep 5

# Simulate user interactions using Python
python3 - << EOD
import pyautogui
import time

# Wait for game window
time.sleep(2)

# Simulate key presses
pyautogui.press('return')  # Start game
time.sleep(1)
pyautogui.press('tab')     # Navigate tutorial
time.sleep(1)
pyautogui.press('return')  # Next/Confirm
time.sleep(1)
pyautogui.press('return')  # Play game
time.sleep(20)             # Let game run for 20 seconds
EOD

# Stop the game
kill $GAME_PID

# Stop screen recording
kill $FFMPEG_PID

# Add text overlay
ffmpeg -i "$VIDEO_OUTPUT" \
    -vf "drawtext=fontfile=/Library/Fonts/Arial.ttf:text='Banana Math Puzzle Demo':fontcolor=white:fontsize=48:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=50" \
    "${DEMO_OUTPUT_DIR}/banana_math_puzzle_demo_final_${TIMESTAMP}.mp4"

echo "Demo recording complete. Output: ${VIDEO_OUTPUT}"
