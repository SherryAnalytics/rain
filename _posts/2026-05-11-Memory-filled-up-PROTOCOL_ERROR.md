---
layout: single
title: "When Memory Fills Up - The PROTOCOL_ERROR Nobody Talks About"
date: 2026-05-11
tags: [llm, memory, protocol-error, debugging]
---

# Long Context Is Not Infinite Memory
### Notes from a PromptOps debugging moment in VS Code + GitHub Copilot

Recently I ran into this error while working in VS Code with GitHub Copilot:

```text
Error Code: net::ERR_HTTP2_PROTOCOL_ERROR
```

I was trying to create a set of QC prompt templates and initially asked the agent to process a large amount of context all at once.

At first I thought the model itself had failed.

Then I tried a different approach: instead of asking the agent to generate everything in one giant context window, I broke the work into smaller focused steps and reviewed the prompts one at a time.

That worked.

The interesting part is that the issue was probably not “AI intelligence,” but context overload.

Since I was working inside VS Code with GitHub Copilot, the overloaded part may have been:

- the Copilot chat session
- the VS Code extension
- the service connection
- the request payload being transmitted behind the scenes
- accumulated generated artifacts and instructions

Modern AI tools can handle very large contexts, but the surrounding workflow still has to package and carry:

- chat history
- prompt templates
- instructions
- generated files
- tool outputs
- formatting metadata
- file operations

Eventually the whole thing becomes heavy and fragile.

This reminded me that:

> Long context is useful, but it is not infinite working memory.

In practice, PromptOps feels less like dumping everything into one mega-prompt, and more like orchestrating manageable stages.

For example:

1. Create policy
2. Create index - registry
3. Create reusabe snippets
4. Create template
5. Review template
6. Save template
7. Move to next template 
8. Maintain changelog/versioning

The workflow matters as much as the prompt itself.

Ironically, this feels very human too.

A clean desk and a staged checklist often outperform trying to hold the entire project in your head at once.

---

# Why This Matters

One thing I am gradually learning is that modern AI engineering is not only about model capability.

It is also about:

- orchestration
- context management
- workflow boundaries
- modular prompting
- state management
- review checkpoints
- memory strategy

Large context windows are powerful, but they are not magic infinity containers.

In many cases, smaller well-scoped prompts produce more stable and maintainable systems than one gigantic “do everything” prompt.

That realization changed how I think about PromptOps.

---

# How I Started Organizing the Prompt Templates

Another thing I learned from this exercise was that the templates themselves needed structure.

Instead of treating prompts as one large collection, I started dividing them into domains.

For now, I grouped them into two major categories:

## 1. DA (Data Analyst) Domain

Templates focused on remediation analytics work itself.

Examples include:

- EA entry writer
- population analysis support
- inclusion/exclusion waterfall logic
- data profiling helpers
- exploratory analysis assistance
- requirement interpretation
- SQL/Python/SAS generation support

These templates are designed to help produce or accelerate analytical work products.

---

## 2. QC (Quality Control) Domain

Templates focused on reviewing, validating, and grading QC check readiness.

Examples include:

- grade EA entries
- QC checklist review
- standards validation
- wording consistency checks
- documentation completeness review
- defect identification
- remediation audit support

These templates behave more like reviewers or validators rather than creators.

---

# What Became Interesting

Once I separated the templates into domains, the workflow started feeling less like “chatting with AI” and more like orchestrating specialized agents with distinct responsibilities.

For example:

```text
DA template → creates EA entry draft
QC template → reviews and grades the EA entry
Finalization template → prepares final submission artifact
```

At that point, PromptOps started resembling a lightweight operating system for analytical workflows.

Not because the prompts themselves were magical, but because:

- the templates were modular
- responsibilities were separated
- context became more manageable
- prompts became reusable
- review loops became clearer
- outputs became easier to audit

Ironically, this also reduced context overload, because each template only needed the context relevant to its own role.

That may have been one of the biggest lessons from the entire debugging experience.

---

# Related Reading

## AI Engineering / PromptOps

### AI Engineering by Chip Huyen
https://www.oreilly.com/library/view/ai-engineering/9781098166298/

### OpenAI Prompt Engineering Guide
https://platform.openai.com/docs/guides/prompt-engineering

### Anthropic Context Windows Overview
https://docs.anthropic.com/en/docs/build-with-claude/context-windows

### LangChain Memory Concepts
https://python.langchain.com/docs/concepts/memory/

### Andrej Karpathy discussion on Context Engineering
https://x.com/karpathy/status/1937902205765607626

---

# Personal Takeaway

The lesson for me was not that “AI failed.”

The lesson was that orchestration matters.

Long context should be treated as a managed asset, not an infinite container.
