.. _battleship-tut:

Battleship example CCS
=========================================

At larger complexities, it is better to seperate the core logic from the Platform interaction.

Core logic
=================================

This plays a game based on Battleship, where you fire cannons at squares on a grid and get hits.
If you sink a ship (by hitting all it's squares) you get more points.

In this game, players are competing against eachother to kill an "AI" which randomally placed it's ships and does not sink.

The goal is to make this modular. All-caps constants define the ships and weapons (the base game only has one kind of weapon, but it's fun to have more):

.. code-block:: Python
    SHIPS = {'kayak':[1,1], 'Viking-boat':[2,1],'scout':[3,1], 'battleship':[4,1]} #...
    WEAPONS = {'cannon':[1,1], 'missle':[3,1], 'depth-charge':[3,3]}
    WEAPONCOUNTS = {'cannon':65536, 'missle':6, 'depth-charge':2}

There are two objects created: The BattleGame recieves attacks and generates scores and reports. The Player class sends attacks and has limited weapons.

Platform interaction
================================

Button pressed drive actions, and messages report things. The Canvas is a personal scoreboard.

The high-level game control flow is here as well. Such as restarting the game or initalizing the game.

Users press a button to (re)start a game. If there is a game running, they have other buttons (one for each weapon) and can press a button which opens a box to dial in the coords of the attack.

All the Platform features here are also found in the simpler Buttons, Group chat, and Menu Canvas tutorials.