# 📦 Container Loading System – Bin Packing Algorithm (Python)

## 🧠 Project Overview
This project implements a **container loading system** using the **First-Fit Decreasing (FFD)** heuristic of the **Bin Packing Problem**. The goal is to optimize how differently sized items (e.g., boxes) are packed into containers with limited capacity, minimizing the number of containers used.

This type of solution is highly applicable to logistics, shipping, warehouse management, and resource allocation problems.


## 🔧 Technologies Used

- **Language**: Python 3
- **Algorithm**: First-Fit Decreasing (FFD)
- **Optional Inputs**: Volume and Weight constraints


## 🚀 How It Works

1. User provides a list of item sizes (volume/weight).
2. The system sorts them in decreasing order (FFD).
3. Items are packed one-by-one into the first container where they fit.
4. The system shows:
   - Container summary (items in each bin)
   - Packing efficiency (used space vs total capacity)
   - Total bins used


## 💡 Why FFD?

- ⚡ Fast and simple to implement
- 🔍 Offers near-optimal packing (90–95% efficiency)
- 🧠 Easy to maintain and extend for multi-constraint versions (e.g., weight + volume)


## 📌 Example

**Input:**
- Items = `[4, 3, 2, 5]` (volume in m³)
- Container capacity = `10 m³`

**Output:**
-Container 1: [5, 4] (Used: 9/10 m³)
-Container 2: [3, 2] (Used: 5/10 m³)
-Packing Efficiency: 70%
-Total Containers Used: 2

## ✅ Key Features

- First-Fit Decreasing (FFD) bin packing algorithm
- Supports volume & weight constraints
- Calculates packing efficiency
- Prints detailed container breakdown

## 👨‍💻 Author
Group Project
