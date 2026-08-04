# Templates

Read only the template you need. Each one is a skeleton for the generated prompt — the thing the user pastes into their tool — not instructions for you.

---

## Template J — Image reference editing

Use when the user has an existing image and wants it modified. Tell the user to attach the reference image to the tool first, then build the prompt around the delta only.

```
Using the attached reference image, change ONLY the following:
- [change 1 — be specific about the object, region, and target state]
- [change 2]

Keep unchanged: [subject identity, pose, framing, lighting, color grade, background — list everything that must survive the edit]

Style match: preserve the original [lighting direction / lens character / color palette / grain] exactly.
Output: [aspect ratio], [resolution], single image, no text overlay.
```

Rules for building it:
- The "keep unchanged" list is the load-bearing half — a reference edit fails by drifting on what nobody protected.
- Never restate the whole scene. If the prompt describes the image, the model regenerates instead of editing.
- One delta per prompt when the changes are unrelated. Two deltas that touch the same region can share a prompt.

---

## Template K — ComfyUI

Node-based workflow, not a single prompt box. Ask which checkpoint is loaded before writing — SDXL, Flux, Pony and SD1.5 take different syntax and weights. Always output two separate blocks; never merge them.

```
POSITIVE PROMPT
[subject], [key features], [action or pose], [environment],
[lighting], [composition and shot type], [art style or medium],
[quality tags appropriate to the checkpoint]
```

```
NEGATIVE PROMPT
[failure modes for this subject], [anatomy issues if figures are present],
[unwanted styles], [text, watermark, signature], [compression and blur artifacts]
```

Add below the blocks, only when the user needs them:
- Checkpoint / VAE / LoRA the prompt assumes, with weights: `<lora:name:0.7>`
- Sampler, steps, CFG — state the range, not one value: drafts 20–30 steps, finals 40–50
- Resolution matching the checkpoint's native training size

Weight syntax is `(word:1.2)` to strengthen and `(word:0.8)` to weaken. Keep weights between 0.5 and 1.5 — outside that range the token distorts the whole image.

---

## Template L — Prompt decompiler

Use when the user pastes an existing prompt and wants it broken down, adapted to another tool, simplified, or split. This is a different task from building from scratch: the source prompt is the spec.

Work in this order and output only step 5 unless the user asked to see the analysis:

1. **Extract the intent** — what the original prompt is actually trying to produce, stated in one sentence. Ignore how it is phrased.
2. **Inventory what is load-bearing** — the constraints, format locks, and scope limits that change the output if removed. Everything else is padding.
3. **Name the failure modes** — what in the original invites drift: vague verbs, missing output contract, fabricated techniques, CoT on a reasoning-native model, no stop conditions.
4. **Re-target** — apply the destination tool's rules from the Tool Routing section of `SKILL.md`. A prompt built for Claude does not transfer to o3 by copying; the scaffolding that helps one hurts the other.
5. **Output the rebuilt prompt** in the standard output format.

When the request is to *split* rather than adapt: cut at the point where the second task stops depending on the first's output shape. Deliver Prompt 1 and add `➡️ Run this first, then ask for Prompt 2` below it.

When the request is to *simplify*: delete in this order — restated instructions, hedges and politeness, explanations of why, examples beyond the second, role assignment if the task is mechanical. Stop when the next deletion would change the output.
