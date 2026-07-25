--!strict

--[[
	Universal combat tunables.

	AGENTS.md: "Keep tunable values in shared configuration modules instead of
	scattering numbers through scripts." docs/COMBAT_SYSTEM.md: "All numeric
	values belong in configuration modules." This is that module.

	Every entry carries its decision status, because the two kinds are not
	interchangeable:

	  LOCKED   approved project direction. Changing it requires a decision
	           recorded in docs/DECISION_LOG.md, not a playtest observation.
	  DEFAULT  a starting value expected to change through testing. Tune it
	           freely from playtest evidence; that is not a project pivot.

	Frozen, so a runtime write fails loudly instead of silently desynchronizing
	the server from its own configuration.
]]

local CombatConfig = {}

-- Health and damage -----------------------------------------------------------

-- DEFAULT (P-001)
CombatConfig.MAX_HEALTH = 100

-- LOCKED. The four-hit chain is approved direction, not a tuning value.
CombatConfig.M1_CHAIN_LENGTH = 4

-- DEFAULT. Total damage of one full uninterrupted chain, about 20. Per-hit
-- values are deliberately absent: the chain's shape is an M2 task, and
-- docs/COMBAT_SYSTEM.md only fixes the total.
CombatConfig.M1_CHAIN_TOTAL_DAMAGE = 20

-- DEFAULT. Seconds after a hit before the chain resets to its first attack.
CombatConfig.COMBO_RESET_SECONDS = 1.1

-- Movement --------------------------------------------------------------------

--[[
	Speed is derived from movement input, never requested (D-028). There is no
	sprint action and no auto-sprint threshold, because the engine already
	supplies one: measured 2026-07-26, a move vector of magnitude 0.5 produced
	exactly half the speed of magnitude 1.0. So a part-deflected thumbstick walks
	on its own, full deflection reaches the cap, and "automatic at full movement
	input" needs no constant to express.

	`Walk` therefore exists only because a keyboard is binary -- `W` is always
	full magnitude, so without a modifier a desktop player would have exactly one
	speed.
]]

-- DEFAULT (P-010). The normal cap. Raised from Roblox's default of 16 on
-- 2026-07-26 because 16 felt sluggish in a 759-stud arena: crossing it took
-- about 53 seconds. The arena figures in docs/OMNISCIENCE_COLISEUM.md and P-008
-- were measured at 16 and have been rescaled accordingly.
CombatConfig.SPRINT_SPEED = 24

-- DEFAULT (P-011). Half of sprint, so holding Walk reads as a deliberate choice
-- rather than a slight nudge.
CombatConfig.WALK_SPEED = 12

-- Death and respawn -----------------------------------------------------------

-- DEFAULT (P-002)
CombatConfig.RESPAWN_DELAY_SECONDS = 5

-- DEFAULT (P-003). Also ends early when the protected player starts an attack
-- or ability. Protected players cannot deal damage.
CombatConfig.SPAWN_PROTECTION_SECONDS = 2

-- Defense ---------------------------------------------------------------------

-- DEFAULT. Total frontal arc protected by block, in degrees, so a hit is
-- blocked when the angle between the defender's facing and the incoming
-- direction is at most half this value. Hits from the side or back bypass
-- block. There is no stamina or guard meter in Scope A.
CombatConfig.BLOCK_ARC_DEGREES = 120

-- DEFAULT. Cooldown on the ragdoll escape, which is separate from the normal
-- dash cooldown. docs/COMBAT_SYSTEM.md: the escape "is defensive counterplay,
-- not a second normal dash."
CombatConfig.RAGDOLL_ESCAPE_COOLDOWN_SECONDS = 20

-- Meter and attribution -------------------------------------------------------

-- DEFAULT. Discovery Meter is server-owned and clamped to [0, this].
CombatConfig.DISCOVERY_METER_MAX = 100

-- DEFAULT. How far back the server looks when attributing a KO or an assist.
CombatConfig.ASSIST_LOOKBACK_SECONDS = 10

-- DEFAULT. Fraction of MAX_HEALTH a player must have dealt within the lookback
-- window to earn an assist. Stored as a fraction rather than a flat 10 damage
-- so it tracks MAX_HEALTH if that is tuned.
CombatConfig.ASSIST_DAMAGE_FRACTION = 0.1

-- Presentation limits ---------------------------------------------------------

-- LOCKED (D-007). Final Proof is a short stylized KO effect, not an execution
-- cinematic. Presentation code may not exceed this.
CombatConfig.FINAL_PROOF_MIN_SECONDS = 1
CombatConfig.FINAL_PROOF_MAX_SECONDS = 2

-- Networking ------------------------------------------------------------------

-- DEFAULT. Ceiling on accepted action requests per player per second, used for
-- the "request rate is plausible" check in docs/TECHNICAL_ARCHITECTURE.md.
-- Sized well above human input rates so it catches automation, not fast play.
CombatConfig.MAX_ACTION_REQUESTS_PER_SECOND = 20

--[[
	Returns the assist damage threshold in health points.

	Pure and therefore unit testable, which is the point: this is exactly the
	kind of derived value that silently breaks when MAX_HEALTH is tuned.
]]
function CombatConfig.getAssistDamageThreshold(): number
	return CombatConfig.MAX_HEALTH * CombatConfig.ASSIST_DAMAGE_FRACTION
end

--[[
	Returns the `Humanoid.WalkSpeed` cap for the current hold state.

	Pure, so the rule is testable without a character. The controller applies the
	number and decides nothing.
]]
function CombatConfig.getMoveSpeed(isWalkHeld: boolean): number
	return if isWalkHeld then CombatConfig.WALK_SPEED else CombatConfig.SPRINT_SPEED
end

--[[
	Returns the maximum angle in degrees between the defender's facing direction
	and an incoming attack for that attack to count as blocked.
]]
function CombatConfig.getBlockHalfArcDegrees(): number
	return CombatConfig.BLOCK_ARC_DEGREES / 2
end

return table.freeze(CombatConfig)
