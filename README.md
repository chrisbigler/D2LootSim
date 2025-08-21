# D2LootSim - Edge of Fate Leveling & Tiers Rework
A Monte Carlo simulation system for Destiny 2's **Edge of Fate Leveling & Tiers Rework** - modeling tier-based progression (T1-T5), Guardian Rank/Conquests unlocks, and the new activity reward structures that prioritize time respect and generous loot distribution.

![CleanShot 2025-08-21 at 15 41 21](https://github.com/user-attachments/assets/119b85d0-965c-40cb-b16b-72a241edbcc2)


## How to run on your Machine
1. Download the repo
2. Open downloaded file folder in your preferred IDE (VS Code, Cursor, etc.)
3. Run `python app.py` to start the web interface on http://localhost:5002

## Core Concepts

### New Progression Philosophy

The **Edge of Fate** system introduces fundamental changes to how players progress:

**Goals of System Tweaks:**
- **Power Level** is no longer the sole focus for progression, but a driving force to access difficulty and loot tiers
- **Power comes from gear tiers and builds**, not raw level increases
- **Guardian Rank Objectives + Conquests** unlock new difficulty and gear tiers
- **Respect Time**: Make loot chase generous at lower tiers (T1-T3)
- **T4 gear** should be directly chaseable 
- **T5 gear** feels rare and reserved for highest end activities only (Raids, Trials, Competitive)

### Gear Tier System (T1-T5)

The new system uses **5 distinct gear tiers** instead of simple power level progression:

- **T1-T3**: Generous drop rates, accessible through regular play
- **T4**: Directly chaseable through focused activities and conquests
- **T5**: Rare drops reserved for pinnacle endgame content (RaDs, Trials, Competitive)

**Crucible Integration**: Crucible drops respect the level band associated tier for drops (LL 300 = T3 w/ 33% chance for T4, LL 400 = T4 w/ 25% chance for T5)

### Guardian Rank & Conquests

**Conquests** serve as milestone progression achievements that unlock new heights:
- Beating a Conquest unlocks new parts of the game with **new gear tiers and difficulty levels**
- Connected to Guardian Rank to reflect achievement progression
- Designed to feel like major progression milestones rather than incremental upgrades
