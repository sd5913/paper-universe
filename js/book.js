
const chapters = [
    {
        number: "CHAPTER 01",
        title: "Living World",
        description:
            "Discover a little world where plants grow, nature responds, and tiny wonders come to life.",
        caption: "A little garden awaits...",
        url: "living_world/index.html",
        theme: "living"
    },
    {
        number: "CHAPTER 02",
        title: "Chapter Two",
        description:
            "A new landscape is waiting to be discovered. Replace this text when the second chapter is ready.",
        caption: "Another world is waiting...",
        url: "chapter-02/index.html",
        theme: "weather"
    },
    {
        number: "CHAPTER 03",
        title: "Chapter Three",
        description:
            "Turn one more page and discover the final part of this little universe.",
        caption: "The final adventure...",
        url: "chapter-03/index.html",
        theme: "secret"
    }
];

let currentChapter = 0;
let isTurning = false;

const storybook = document.getElementById("storybook");
const numberText = document.getElementById("chapterNumber");
const titleText = document.getElementById("chapterTitle");
const descriptionText = document.getElementById("chapterDescription");
const captionText = document.getElementById("sceneCaption");
const pageCounter = document.getElementById("pageCounter");

const prevButton = document.getElementById("prevButton");
const nextButton = document.getElementById("nextButton");
const enterButton = document.getElementById("enterButton");

function renderChapter() {
    const chapter = chapters[currentChapter];

    numberText.textContent = chapter.number;
    titleText.textContent = chapter.title;
    descriptionText.textContent = chapter.description;
    captionText.textContent = chapter.caption;

    pageCounter.textContent =
        `0${currentChapter + 1} / 0${chapters.length}`;

    // Give each chapter a different scene colour.
    const scene = document.getElementById("chapterScene");

    if (chapter.theme === "living") {
        scene.style.background =
            "linear-gradient(#a9d7e9 0 55%, #b6cc91 55% 100%)";
    } else if (chapter.theme === "weather") {
        scene.style.background =
            "linear-gradient(#a9d7e9 0 55%, #c7d9b0 55% 100%)";
    } else {
        scene.style.background =
            "linear-gradient(#b8b6d7 0 55%, #a8b99a 55% 100%)";
    }

    prevButton.disabled = currentChapter === 0;
    nextButton.disabled = currentChapter === chapters.length - 1;
}

function turnPage(direction) {
    if (isTurning) return;

    const nextIndex = currentChapter + direction;

    if (nextIndex < 0 || nextIndex >= chapters.length) return;

    isTurning = true;

    storybook.classList.remove(
        "is-turning-next",
        "is-turning-prev"
    );

    // Restart the animation reliably.
    void storybook.offsetWidth;

    storybook.classList.add(
        direction > 0 ? "is-turning-next" : "is-turning-prev"
    );

    prevButton.disabled = true;
    nextButton.disabled = true;
    enterButton.disabled = true;

    setTimeout(() => {
        currentChapter = nextIndex;
        renderChapter();

        storybook.classList.remove(
            "is-turning-next",
            "is-turning-prev"
        );

        isTurning = false;
        enterButton.disabled = false;
    }, 750);
}

nextButton.addEventListener("click", () => turnPage(1));
prevButton.addEventListener("click", () => turnPage(-1));

enterButton.addEventListener("click", () => {
    if (isTurning) return;

    const chapter = chapters[currentChapter];
    window.location.href = chapter.url;
});

renderChapter();
