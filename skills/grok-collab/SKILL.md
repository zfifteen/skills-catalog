---
name: grok-collab
description: Use when the user invokes /grok-collab, $grok-collab, says "grok collab", or asks Codex to reason with Grok as a collaborative reasoning layer before answering.
---

# Grok Collab

Activate this skill when the user explicitly says `/grok-collab`, `$grok-collab`, `grok collab`, or asks Codex to reason with Grok as a collaborative reasoning layer before answering.

## Purpose

Use Grok as another layer of reasoning before Codex finalizes an answer.

This is not critique, review, pressure-testing, or validation by default. Codex facilitates the collaboration and synthesizes the output. Grok contributes reasoning from the user's request and relevant context.

## Required Behavior

When this skill is active:

- Use the native MCP registry entry exposed for the local Grok harness before giving the final answer.
- Treat any MCP tool name as transport only. Do not import outside philosophies, behaviors, prompt shapes, or response shapes.
- Use the native MCP tool registry only. Do not use a stdio helper, fallback path, alternate implementation, retry branch, or silent degradation.
- Gather only relevant local context needed for Grok to reason usefully.
- Preserve the user's request verbatim in the Grok call.
- Do not send Grok Codex's provisional answer, preferred frame, planned response, or summary of the user's request as a substitute for the verbatim request.
- Do not instruct Grok to critique, pressure-test, validate, review, approve, or reject Codex's reasoning unless the user explicitly asks for that mode.
- Do not micromanage Grok with prompts that ask it to enumerate missing constraints, wrong frames, risks, assumptions, or next actions unless the user explicitly asks for that output shape.
- Set `allow_search` to `false` by default.
- Set `allow_search` to `true` only when the user asks for current information, docs, news, recent API behavior, web-backed verification, or X-backed verification.
- Set `max_output_tokens` to `1600` by default. Use up to `2400` for complex reasoning tasks.

## Collaboration Contract

Codex sends Grok:

- The user's request verbatim as `problem`.
- Relevant local context as `context`.
- The nature of the collaboration in `context`: Grok is contributing reasoning as a peer layer before Codex synthesizes the final answer.

Use this `desired_output` unless the user requests a different output shape:

```text
Contribute reasoning for the user's request from the request and context as an independent collaborative layer.
```

The `context` value must include this statement:

```text
Collaboration contract: Grok is being asked to contribute reasoning as a peer layer before Codex synthesizes the final answer. Codex has not supplied a provisional answer or preferred frame. Reason from the user's verbatim request and the relevant local context.
```

## MCP Payload Contract

Send one Grok collaboration request with this payload shape:

```json
{
  "problem": "The user's request verbatim.",
  "context": "Relevant local context plus the collaboration contract.",
  "desired_output": "Contribute reasoning for the user's request from the request and context as an independent collaborative layer.",
  "allow_search": false,
  "max_output_tokens": 1600
}
```

## Final Synthesis

After Grok returns:

- Integrate the user's request, relevant local evidence, Grok's reasoning, and Codex's own reasoning into one final answer.
- Preserve materially different reasoning paths, implications, or conclusions that improve the answer.
- State material disagreement plainly.
- Include a compact `Grok contribution` section when it helps the user understand the synthesis.
- Do not reduce Grok's contribution to a token citation, perfunctory bullet, subordinate check, or pasted model answer.
- Do not present the final answer as two separate answers. The final output is one integrated synthesis.

## Failure Rule

If the Grok MCP harness is unavailable or fails:

- Say exactly that the Grok collaboration MCP call failed.
- Include the concrete error.
- Do not pretend Grok participated.
- Stop unless the user explicitly asked to continue without Grok.
