Weather World — Development Process
Module A | Paper Universe
Author: Guo Zijun
Last updated: 26 November 2026
1. Concept and Interaction Design
Weather World is an interactive paper-cut environment where users can freely place, drag, and combine weather elements to discover unexpected visual reactions.

The design focuses on creative exploration rather than fixed instructions. Users can experiment with different combinations and observe how their actions affect the environment. I wanted discovery to feel playful and rewarding rather than requiring players to follow a predetermined list of recipes.
2. Visual Development
I developed a consistent paper-cut visual style using pastel colours, layered paper textures, and soft shadows.

The visual assets include the sun, clouds, rain, snowflakes, wind, water droplets, lightning, a rainbow, and a tornado.

AI-assisted image generation was used to support asset creation. I selected and refined the visual direction and integrated the assets into the interactive environment.
3. Implementation
The module was developed using Python, Streamlit, HTML, CSS, and JavaScript.

Key features include:
- Drag-and-drop placement and free movement of weather elements.
- Weather combinations that create snow clouds, water droplets, and thunderstorms.
- A rainbow reaction when the sun approaches rain.
- A blizzard triggered by combining wind and snow.
- A tornado triggered by combining two wind elements.
- Background colour changes and animated visual feedback.
4. Testing and Iteration
During development, I identified and addressed several issues:
- Adjusted oversized snowflakes and water droplets to improve visual balance.
- Preserved the original background image proportions to prevent distortion.
- Refined snow cloud layering so that the connecting strings appear behind the cloud.
- Changed the thunderstorm design to use a dark cloud and animated lightning instead of rain.
- Replaced an unsuccessful SVG tornado design with a paper-cut PNG asset.
- Fixed an interaction issue that prevented users from adding weather elements during a blizzard.
These changes improved visual consistency and interaction clarity.
5. AI Assistance and Reflection
AI tools supported code development, debugging, and the generation of visual assets. However, the design direction, interaction requirements, visual evaluation, and testing decisions were guided by my own observations.

An important lesson from this process was that technically functional interactions do not always produce effective visual experiences. Repeated testing helped identify problems that were not obvious from the code alone.
6. Development Milestone — 12 November 2026
Weather World 6.0 had been implemented and tested locally. The version was pushed to the feature/weather-world branch and was ready for further integration testing with the other Paper Universe modules.
7. Game Design Evolution — Paper Universe 2.0
As the group project developed, we moved from a collection of separate interactive environments towards a more connected experience. The proposed game structure includes a home environment, a magical tree, Weather World, Plant World, and Crystal Cave.

The player is represented by a small spirit. Through exploration and interaction, the player discovers magic and collects different types of energy that are intended to support the growth of the magical tree.

For Weather World, I retained the original experimental interaction design while introducing a clearer purpose for discovering weather combinations. I wanted the module to contribute to the wider game without losing its freedom of exploration.

The intended shared progression system still requires integration across the modules.
8. Sky Energy and Discovery System
I introduced a discovery-based reward system to give weather interactions a clearer sense of progression. Each unique weather discovery rewards one unit of Sky Energy, with six possible discoveries in total.
Combination	Discovery	Trigger
Sun + Rain	Rainbow	Proximity
Cloud + Snow	Snow Cloud	Overlap and release
Sun + Snow	Water	Overlap and release
Cloud + Rain	Thunderstorm	Overlap and release
Snow + Wind	Blizzard	Overlap and release
Wind + Wind	Tornado	Overlap and release


The implementation uses unique discovery identifiers and a JavaScript Set to prevent repeated discoveries from generating additional energy. Resetting the weather scene does not clear the discovery record during the current page session.

This approach rewards experimentation rather than repetitive actions. However, the current discovery record is local to the module's JavaScript page. It does not yet persist across page reloads or communicate with the shared home environment. A common interface must be agreed with the other module owners before cross-world progression can be completed.
9. Formative Feedback and Tutorial Development
Following the formative review on 15 November, I reconsidered how a first-time player would understand Weather World. The feedback highlighted the need for clearer onboarding, an integrated experience, and further playtesting. The review was based on source files and documentation rather than an observed browser playtest.

Previously, players were expected to understand the weather tools and discover their interactions through experimentation. Although this supported freedom, it could also leave new players uncertain about how to begin.

I designed a Weather Goddess dialogue interface to introduce the world and explain its basic interaction principles. Rather than introducing another controllable character, the goddess acts as the narrative voice of the weather environment.

The tutorial includes three pages, Next and Skip controls, and a Help button that allows players to reopen the instructions. I used a pastel lavender and cream paper-cut illustration in which the goddess's flowing hair forms the dialogue area. The artwork was generated with AI assistance and iteratively evaluated to match the existing visual style.

During local testing, I encountered an image-loading issue and corrected the asset location. I also adjusted the text size and positioning after noticing that parts of the dialogue overlapped the decorative illustration. Some overlap remained, indicating that the artwork and text layout need a more clearly defined safe area.

This process taught me that onboarding should provide enough information to help players begin without revealing every hidden combination. It should support discovery rather than replace it.
10. Integration and Fullscreen Experiments — 26 November 2026
To explore how the group's existing modules could form a more cohesive experience, I tested several independent integration prototypes using the available branch snapshots and existing assets. These were experimental versions outside the formal Weather World branch, not completed features of the main repository.
V1 — Storybook Navigation
The first prototype used a storybook interface to connect Weather World, Plant World, and Crystal Cave. It built on the existing homepage and book-navigation work rather than replacing the individual worlds entirely.

The prototype demonstrated a possible navigation structure, but entering a world revealed a significant difference between the immersive storybook interface and the smaller embedded game scenes.
V2 — Initial Fullscreen Adaptation
The second prototype attempted to enlarge the game containers. Browser testing showed that Weather World expanded horizontally but retained a restricted vertical play area, leaving substantial unused space.

This demonstrated that changing the outer container alone was insufficient because individual modules also imposed their own layout constraints.
V3 — Immersive Fullscreen Layout
The third prototype changed the internal layout as well as the outer game container. In Weather World, the background filled the available game window, while the weather toolbar, energy counter, and action buttons were positioned over the scene.

The resulting Weather World layout was more immersive. However, testing revealed a new interaction problem: clicking a weather tool could create an element underneath the toolbar, where it became partially obscured.

An experimental correction was prepared to distinguish click placement from drag placement and keep elements away from interface controls. This correction still requires browser verification and has not been merged into the formal Weather World branch.

The experiment showed that responsive design affects not only visual presentation but also interaction coordinates, object placement, and accessibility of controls. Fullscreen changes must therefore be tested together with the original gameplay.
11. 3D Pop-up Book Experiment
I also explored a more ambitious direction inspired by a reference video of an interactive pop-up storybook. Instead of using a book simply as a menu, I wanted the game itself to take place on the pages, with each completed chapter revealing the next environment.

An independent V4 prototype was developed with AI assistance using CSS 3D transformations, existing PNG assets, temporary geometric scenery, and simplified chapter objectives. It explored perspective, upright paper scenery, sequential progression, and page-turn transitions.

The prototype was not a complete Three.js or WebGL implementation and did not preserve all the original gameplay. When I tested it in the browser, the visual result did not achieve the spatial depth, paper-folding quality, or level of detail I expected from the reference.

I decided not to continue this direction for the current submission. Achieving the intended result would require substantial changes to the rendering architecture, asset preparation, and interaction logic. Given the remaining development time, the cost of rebuilding the experience outweighed the potential visual benefits.

Although the experiment was unsuccessful as a replacement for the existing game, it helped clarify the difference between a decorative book interface and a genuinely interactive three-dimensional paper environment.
12. Critical Reflection and Design Decisions
Visual quality and technical feasibility
Throughout development, I found that a visually attractive concept does not automatically translate into a successful interactive experience. The fullscreen and pop-up book experiments made this particularly clear. A change in presentation can introduce new problems even when the original gameplay is functional.

I therefore decided to prioritise the existing paper-cut visual identity and established interaction mechanisms rather than pursue a major architectural redesign close to the deadline.
Scope and team responsibilities
As well as developing Module A, I contributed to project planning, task organisation, and exploratory integration work. These experiments helped identify technical dependencies between the modules, but they also highlighted the importance of maintaining clear responsibilities within a group project.

The overall home interface, navigation, and presentation are primarily the responsibility of Module D. My responsibility is to maintain Weather World, prepare its integration interface, and participate in shared testing. The final integration requires cooperation from all module owners.
AI-assisted development
AI assistance was used to generate visual assets, propose implementation approaches, produce and revise code, and investigate bugs. I evaluated the generated outputs through local browser testing and made decisions about which approaches to retain, revise, or reject.

The V4 experiment was an example of why AI-generated code should not be accepted solely because it runs. Its visual quality and interaction design did not meet my expectations, so I rejected it as the basis for the final project.

This experience reinforced the importance of critical evaluation, understanding the limitations of generated implementations, and making design decisions based on observed results rather than technical novelty alone.
13. Current Status — 26 November 2026
The formal Weather World module includes five basic weather elements, six unique discoveries, animated weather reactions, a local Sky Energy counter, and a three-page tutorial. The tutorial and dialogue interface were committed and pushed to the feature/weather-world branch in commit ea3b3ba.

The fullscreen and 3D storybook prototypes remain separate experiments. They should not be treated as features already integrated into the main project.
Remaining tasks
- [ ] Verify direct toolbar-to-scene dragging and immediate fusion behaviour.
- [ ] Check environmental state recovery after deleting weather elements or completing special weather effects.
- [ ] Prevent unintended weather interactions while the tutorial is open.
- [ ] Add clear feedback when all six weather discoveries have been completed.
- [ ] Agree and implement the shared energy and progression interface with the group.
- [ ] Adapt the module to the final agreed navigation and layout architecture.
- [ ] Conduct systematic browser testing of all six discoveries, repeated rewards, removal, reset, and recovery from special weather events.
- [ ] Conduct first-time player testing and document actual observations and feedback.
- [ ] Participate in final integration testing and update the documentation before submission.
The testing recorded so far primarily consists of my own development and browser checks. Independent player feedback and final integrated testing results have not yet been documented. These will be added when the tests have been completed.