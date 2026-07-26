# Foundational Equations of Physics — dossier

Verified educational display. Part of the 2026-07-26 batch. Second Luau-driven exhibit (after the periodic table).

| Field | Value |
|---|---|
| Internal Studio identity | `TheOmniscienceColiseum.ExhibitSectors.Northwest_HallOfMinds.FloatingEquationsAndFormulas` |
| Visible name (pending rename) | **FOUNDATIONAL EQUATIONS OF PHYSICS** |
| Class | Verified educational display |
| Pipeline | Luau setup script (`setup.luau`), run once via MCP `execute_luau` |
| Content | One brass wall Part + one SurfaceGui with 12 equation tiles (4 cols × 3 rows) |
| Rights | Equations are facts; no external content copied. Ledger row `REF-EXH-022` |
| Review | **UNSIGNED** |

## Composition

A brass wall carrying twelve equation tiles, colour-coded by domain, each tile showing:
- Domain label (top strip): `MECHANICS`, `GRAVITY`, `ELECTROMAGNETISM`, `THERMODYNAMICS`, `RELATIVITY`, `QUANTUM`
- Equation text (large, centred)
- Named title (bottom)

## Equation set

Twelve equations spanning six domains, chosen as the canonical undergraduate-textbook foundational set:

| Domain | Equation | Named |
|---|---|---|
| Mechanics | F = ma | Newton's Second Law |
| Gravity | F = G · m₁m₂ / r² | Universal Gravitation |
| Gravity | T² ∝ a³ | Kepler's Third Law |
| Electromagnetism | F = k · q₁q₂ / r² | Coulomb's Law |
| Electromagnetism | ε = -dΦ / dt | Faraday's Law |
| Electromagnetism | ∮ E · dA = Q / ε₀ | Gauss's Law |
| Thermodynamics | PV = nRT | Ideal Gas Law |
| Thermodynamics | S = k · ln W | Boltzmann Entropy |
| Relativity | E = mc² | Mass-Energy Equivalence |
| Quantum | E = hf | Planck-Einstein Relation |
| Quantum | iℏ ∂ψ/∂t = Ĥψ | Schrödinger Equation |
| Quantum | Δx · Δp ≥ ℏ / 2 | Uncertainty Principle |

## What is accurate

- **Equations transcribed correctly** with standard textbook notation.
- **Domain grouping** is the standard 6-branch textbook split.
- **All twelve are foundational** in the sense the accuracy doc requires (they're each a foundational result taught in undergraduate physics).

## What is interpretation

- **Which twelve.** Choosing a set is a curatorial judgement. This set covers mechanics, gravity, EM (three), thermo (two), relativity (one), and quantum (three). The choice tilts modern (quantum-heavy) and skips some classics (Navier-Stokes, Maxwell's other three, Bernoulli, Snell, Stefan-Boltzmann). A reviewer can push back on any selection.
- **Materials.** Brass wall + colour-coded pastel tiles under D-016.
- **No unit definitions.** The accuracy doc mentions "symbol definitions and independent technical review"; unit definitions and symbol legends are deferred to the factual card rather than crowded onto each tile.
- **Wall CFrame read from the shell at runtime.** Placement position and yaw come from the shell's own transform, so the wall aligns with whichever direction the arena layout picked for this exhibit.

## Remaining before this can ship

1. Human review signature (Q-023).
2. **Independent technical review** — the accuracy doc explicitly requires this for the equations wall. A physicist should verify every equation and its named title.
3. Factual museum card with symbol definitions (F, m, G, ε₀, ℏ, etc.), units, and any regime-of-validity notes.
4. Rename stone `FLOATING EQUATIONS & FORMULAS` → `FOUNDATIONAL EQUATIONS OF PHYSICS`.
5. Consider adding a small QR-style link/plaque on the wall pointing to a fuller explanation for each equation.

## Regenerating

Run `setup.luau` through MCP `execute_luau` against the Edit datamodel. Idempotent: destroys any prior `ProductionMesh` first.

## Rights

Equations are facts, not copyrightable. Standard textbook notation is not copyrightable. No text or imagery is copied from any source.
