# Clash of clans clone
This is a terminal-based clash of clans clone built using python

## Gameplay
The player controls the king, moving him and attacking any buildings in his vicinity.
In addition, players can spawn troops in one of three predefined locations (marked by numbers 1, 2, 3 on the map).

The aim is to destroy the townhall and all huts on the map. 
Beware of the 2 cannons that fire when the king or troop is within their firing radius. 
To help defend against these attacks, you can use the healing spell to boost the king and troops' health by 50%.

The game ends when
- player wins by destroying the townhall and all huts
- player loses when the king and troops are killed before they are able to destroy all buildings.

## Game objects
- King: main object controlled by the player, marked by `K` on the map.
- Barbarians: troops spawned by the player in one of three predefined locations. 
Move towards the nearest building and try to destroy it. Marked by `B`.
- Townhall: The central building in the middle of the map, marked by `T`.
- Hut: Multiple huts are distributed across the map to be destroyed by the player. Marked by `H`.
- Cannon: There are 2 cannons on the map that attack the king and barbarians when they get too close. Marked by `C`.
- Walls: There are walls blocking some of the cells on the map. These must be destroyed in order to access those cells. Marked by `*`.
- Spawning points: There are spawning points on the map marked by `1`, `2` and `3`. Troops can be spawned here by pressing the number keys 1, 2, or 3 respectively.

## Game controls
- `w`: move king up
- `s`: move kind down
- `a`: move king left
- `d`: move king right
- `space`: king attacks all buildings in a 5 block radius.
- `h`: use the healing spell. Boost health by 50% or current value.
- `q`: quit

