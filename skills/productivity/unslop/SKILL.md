---
name: unslop
description: Cut AI tells from a piece of writing and sharpen its voice without changing what it says. Point it at a draft, a doc, or a message.
disable-model-invocation: true
---

# Unslop

Edit the text the user pointed at so it reads as written by a person, without changing what it says.

## Contract

- **Input:** the text the user points at: pasted text, a file path, or, when nothing is named, your own previous reply.
- **Output:** the rewritten text only, in the input's format. Add a change list only when the user asks for one.
- **Facts stay fixed.** Names, numbers, claims, and any structure the reader depends on survive untouched. A rule may cut a sentence; none may add a fact the source or the user did not supply.

## Process

1. **Fix the register.** Read the intended reader and voice from the text or the user's instruction. When neither says, keep the input's own register. Every later choice answers to it: a first-person post can carry opinions; a status email or a spec cannot grow any.
2. **Apply every rule.** Check the text against each numbered rule below and rewrite each hit. Most fixes are mechanical: the plain sentence a person would write, no taste required. Done when every rule has been checked and every hit rewritten.
3. **Sharpen the voice** within the register from step 1, using the next section. Done when every bullet there has been checked against the register.
4. **Reread as a stranger.** First search the result for the character-level tells: dashes, curly quotes, title-case headings, emojis. Then read it fresh. For each remaining tell, name the rule, fix it, and read again. Done when a full pass finds no hit.

## Sharpening the voice

Removing tells is half the job. Sterile, voiceless writing is just as obvious, and so is the over-correction: a chatty "definitely not AI" register swapped in for the smooth one. Both are defaults. The target is the author's own voice on a good day.

- **Sharpen stances the source already holds.** Where the author reacts to a fact, make the reaction land. Where they stay neutral, leave it neutral. Never invent an opinion.
- **Vary rhythm.** Short sentences. Then longer ones that take their time.
- **Acknowledge complexity the source holds.** "Impressive but also kind of unsettling" beats "impressive" when the author felt both.
- **First person where the register allows it.** "I" isn't unprofessional in a post or a note; it is out of place in a spec.
- **Let some mess in.** Perfect structure looks machine-made.
- **Be specific with what the source gives you.** Not "this is concerning" but the number or the event that made it concerning, when the text names one. When it doesn't, leave the sentence plain.

## Rules

Each rule leads with the target, then the tells to detect.

### Content

1. **State what happened.** Tells: puffery ("pivotal moment", "testament to", "evolving landscape", "setting the stage for", "indelible mark", "deeply rooted") and formulaic arcs ("Despite challenges... continues to thrive", "The future looks bright"). Replace with the specific facts the source holds, or cut.
2. **Name one source and say what it said, or cut the claim.** Tells: outlets or authorities cited without content. "Experts believe", "Industry reports suggest", "Some critics argue", a string of publication names.
3. **Replace a trailing -ing phrase with a fact, or delete it.** Tells: "highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering...".
4. **Describe neutrally.** Tells: promotional adjectives. "nestled", "vibrant", "breathtaking", "groundbreaking", "renowned", "stunning", "must-visit".

### Language

5. **Use the plain word.** Tells: additionally, crucial, delve, enduring, enhance, garner, interplay, intricate, landscape (abstract), tapestry (abstract), underscore, utilize, leverage, facilitate, numerous, "in the event that". Also the abstract-metaphor nouns: substrate, wedge, vector, locus, vantage, nexus, primitive (as noun), harness (as metaphor), surface (as in "API surface"), bedrock, scaffolding (as metaphor), modality, paradigm, gold-plating, ratchet (as metaphor), evacuate (for moving code), endgame, north star, flywheel. These read as technical but usually have a plainer concrete word: "substrate" is "base", "vector" is "way", "gold-plating" is "more than the job needs", "ratchet" is "a limit that only tightens", "evacuate" is "move out". A term the text defines or the project pins stays.
6. **Say "is" or "has".** Tells: "serves as", "stands as", "boasts", "features".
7. **State the point directly.** Tell: "Not just X, but Y."
8. **Use the natural number of items.** Tell: ideas forced into groups of three.
9. **Pick one name and repeat it.** Tell: synonym cycling. "protagonist", "main character", "central figure", "hero" in one paragraph.
10. **List topics directly.** Tell: false ranges, "from X to Y" where X and Y share no scale.

### Style

11. **Separate thoughts with a period or a comma.** Tells: em dashes, and the substitutes reached for in their place: en dashes, hyphens used as dashes, parentheses standing in for a dash. If a thought needs separation, end the sentence.
12. **Use a colon only before a list or an example.** Tell: a colon as a mid-sentence connector. "The fix is simple: rename the column" becomes "The fix is to rename the column." Same words, no crutch punctuation.
13. **Bold a lead-in only when it names the item and new detail follows.** "**Schema in TypeScript.** Tables live in one file." is fine. Tells: bold on every proper noun or acronym; a bold label and colon that restates the line ("**Performance:** Performance improved..."), which becomes prose.
14. **Sentence case headings.** Tell: Title Case Headings.
15. **Plain headings and bullets.** Tell: decorative emojis.
16. **Straight quotes.** Tell: curly quotes.

### Filler

17. **Say it in the fewest words.** "In order to" is "To". "Due to the fact that" is "Because". "It is important to note that" is deleted.
18. **Hedge once.** "could potentially possibly be argued that it might" is "may".

### Plain speech

19. **Name the mechanism or the number.** Tells: sentences that name a feeling. "the database stays close at hand", "SQL you can read". The fix: "`.toSQL()` returns the exact string sent to the database", "a column rename fails the build". If a sentence can't be restated as an instruction, a fact, or a number, cut it. If it could appear unchanged in another project's docs, cut it.
20. **One idea per sentence.** Tell: a sentence the reader must backtrack to parse. Split it or drop clauses.
21. **Name the actor.** Tell: "is/are/was/were + past participle". "Queries are validated" becomes "the compiler validates queries". Passive stays only when the actor is unknown or doesn't matter.
22. **Use the stronger verb or the number.** Tell: an adverb propping up a weak verb. "runs quickly" is "is fast" or the measurement; "significantly improves" is the measured delta.

### Assistant boilerplate

23. **Cut assistant boilerplate wherever it appears.** Tells: "I hope this helps!", "Of course!", "Certainly!", "Great question!", "You're absolutely right!", "Found the smoking gun!". A plain sign-off the author would write ("Let me know if you have questions") is theirs and stays.
24. **Find the source or cut the sentence.** Tell: cutoff disclaimers. "While specific details are limited...".
