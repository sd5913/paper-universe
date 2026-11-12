# Weather World — Development Process

**Module A | Paper Universe**

## 1. Concept and Interaction Design

Weather World is an interactive paper-cut environment where users can freely place, drag, and combine weather elements to discover unexpected visual reactions.

The design focuses on creative exploration rather than fixed instructions. Users can experiment with different combinations and observe how their actions affect the environment.

## 2. Visual Development

I developed a consistent paper-cut visual style using pastel colours, layered paper textures, and soft shadows.

The visual assets include the sun, clouds, rain, snowflakes, wind, water droplets, lightning, a rainbow, and a tornado.

AI-assisted image generation was used to support asset creation. I selected and refined the visual direction and integrated the assets into the interactive environment.

## 3. Implementation

The module was developed using Python, Streamlit, HTML, CSS, and JavaScript.

Key features include:

- Drag-and-drop placement and free movement of weather elements.
- Weather combinations that create snow clouds, water droplets, and thunderstorms.
- A rainbow reaction when the sun approaches rain.
- A blizzard triggered by combining wind and snow.
- A tornado triggered by combining two wind elements.
- Background colour changes and animated visual feedback.

## 4. Testing and Iteration

During development, I identified and addressed several issues:

- Adjusted oversized snowflakes and water droplets to improve visual balance.
- Preserved the original background image proportions to prevent distortion.
- Refined snow cloud layering so that the connecting strings appear behind the cloud.
- Changed the thunderstorm design to use a dark cloud and animated lightning instead of rain.
- Replaced an unsuccessful SVG tornado design with a paper-cut PNG asset.
- Fixed an interaction issue that prevented users from adding weather elements during a blizzard.

These changes improved visual consistency and interaction clarity.

## 5. AI Assistance and Reflection

AI tools supported code development, debugging, and the generation of visual assets. However, the design direction, interaction requirements, visual evaluation, and testing decisions were guided by my own observations.

An important lesson from this process was that technically functional interactions do not always produce effective visual experiences. Repeated testing helped identify problems that were not obvious from the code alone.

## 6. Current Status — 12 November 2026

Weather World 6.0 has been implemented and tested locally. The latest version has been pushed to the `feature/weather-world` branch.

The module is ready for further integration testing with the other Paper Universe modules.