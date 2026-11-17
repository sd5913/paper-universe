# Secret World — Development Process

**Module C | Paper Universe**

## 1. Concept and Interaction Design

Secret World is a surreal paper-cut exploration module, intentionally distinct from Weather World and Biology World in both visual language and interaction verbs.

**Visual language:** aged parchment, torn newspaper edges, cyanotype (blueprint) style, glow-in-the-dark mineral ink paper-cuts.

**Interaction verbs:** drag-overlap (Overlap), tear (Tear), flip (Flip), hold-and-charge (Hold & Charge).

**Feedback mechanisms:** instant colour inversion, geometric fragmentation, hidden-layer reveal, and transformation of everyday objects into surreal symbols.

The design goal is discovery through experimentation — players are not given instructions, they explore the canvas and uncover secrets by interacting with the four core elements.

## 2. Four Core Elements

| Element | Name | Visual | Interaction |
|---------|------|--------|-------------|
| A | Shift Door (错位之门) | Paper-cut archway on the canvas | Drag the door handle to shift it |
| B | Glow Crystal (发光水晶) | Semi-transparent geometric mineral with etchings | Click to awaken glow, drag near other objects, hold to charge |
| C | Stellar Compass (星图罗盘) | Gear and paper-pointer celestial compass | Rotate the pointer to specific angles |
| D | Void Envelope (黑洞信封) | Open black envelope with torn edges | Drag objects into it to devour/transform |

## 3. Combination Reactions

1. **Spatial Fold** (Door + Crystal): Drag the crystal near the door. The scene inverts to negative colours, the door opens to reveal a miniature starry sky.
2. **Dimension Devour** (Any object + Envelope): Drag the crystal into the envelope. The object is swallowed, crumpled, and the envelope spits out a completely different mutated paper-cut (origami wings, glowing jellyfish, paper butterfly, or star fragment).
3. **Symbol Awaken** (Compass + Hidden Layer): Rotate the compass pointer to 45° or 180°. Hidden ancient glyphs and geometric mazes fade in on the parchment background.

## 4. Final Climax — Secret Mandala

After triggering 2 or more combination reactions, the entire canvas explodes into confetti triangles. The pieces then reassemble into a large, rotating "Secret Mandala" (秘密曼陀罗). The player can move the mouse to blow and disperse the mandala pieces.

## 5. Implementation

The module was developed using HTML, CSS, JavaScript, and p5.js.

Key technical features:

- **Easing functions** (AI-assisted): EaseOutCubic, EaseInOutCubic, EaseOutBack, EaseOutElastic for smooth animations.
- **Torn-paper geometry**: Vertex deformation using `noise()` and `sin()` to simulate torn edges on the void envelope.
- **Negative-space effect**: Alpha layering and colour inversion for the spatial fold reaction.
- **Hidden-layer reveal**: Alpha blending controlled by compass angle to fade in ancient glyphs.
- **Spring physics**: Crystal returns to home position with velocity-based spring physics after release.
- **Mandala state machine**: `idle → exploding → reassembling → active` with confetti particles and polar-coordinate layout.
- **Persistence**: Progress saved to `localStorage` with version key `paper_universe_secrets_v3`.
- **Secret star map**: A journal panel (press J) showing a constellation of 12 discovered secrets across 4 tiers.

## 6. Testing and Iteration

During development, the following were tested and refined:

- Verified that all four elements are discoverable through proximity and interaction.
- Confirmed that each combination reaction triggers correctly with appropriate visual feedback.
- Tested the mandala explosion → reassembly → dispersal sequence.
- Ensured that progress persists across page reloads via localStorage.
- Fixed an issue where clicking the crystal would discover all four primary elements at once (this is intentional — it serves as an entry point to the module).
- Confirmed the module operates independently from Weather World and Biology World (no shared state dependencies beyond CONFIG/STATE conventions).

## 7. AI Assistance and Reflection

AI tools assisted with:
- Generating easing function implementations.
- Calculating geometric vertices for the torn-paper envelope edges.
- Structuring the mandala state machine logic.
- Debugging the compass angle normalisation.

However, the overall design concept, visual direction, interaction design, element definitions, and all testing decisions were guided by my own creative vision and observation. I understand and can explain every part of the implementation.

The key lesson from this process was that complex interaction systems need careful state management — the mandala sequence in particular required a clear state machine to avoid visual glitches during transitions.

## 8. Current Status — 9 November 2026

Secret World v3 has been implemented and tested locally. The first version is being uploaded to the `秘密世界` branch in staged commits.

The module is ready for further integration testing with the other Paper Universe modules.
