
const chapters = [
    {
        number: "CHAPTER 01",
        title: "Living World",
        description:
            "Discover a little world where plants grow, nature responds, and tiny wonders come to life.",
        url: "living-world/index.html",
        previewImage: "assets/living-world-preview.png",
        theme: "living"
    },
    {
        number: "CHAPTER 02",
        title: "Chapter Two",
        description:
            "A new landscape is waiting to be discovered. Replace this text when the second chapter is ready.",
        url: "chapter-02/index.html",
        previewImage: "assets/chapter-02-preview.png",
        theme: "weather"
    },
    {
        number: "CHAPTER 03",
        title: "Chapter Three",
        description:
            "Turn one more page and discover the final part of this little universe.",
        url: "chapter-03/index.html",
        previewImage: "assets/chapter-03-preview.png",
        theme: "secret"
    }
];

let currentChapter = 0;
let isTurning = false;

// Existing book elements
const storybook = document.getElementById("storybook");
const numberText = document.getElementById("chapterNumber");
const titleText = document.getElementById("chapterTitle");
const descriptionText = document.getElementById("chapterDescription");
const pageCounter = document.getElementById("pageCounter");

// New chapter preview elements
const previewLink = document.getElementById("chapterPreviewLink");
const previewImage = document.getElementById("chapterPreviewImage");
const previewTitle = document.getElementById("chapterPreviewTitle");
const previewHint = document.getElementById("chapterPreviewHint");

// Navigation buttons
const prevButton = document.getElementById("prevButton");
const nextButton = document.getElementById("nextButton");


function renderChapter() {
    const chapter = chapters[currentChapter];

    // Update left page
    numberText.textContent = chapter.number;
    titleText.textContent = chapter.title;
    descriptionText.textContent = chapter.description;

    // Update right page preview
    previewLink.href = chapter.url;
    previewImage.onload = () => {
        console.log("Preview image loaded:", chapter.previewImage);
    };

    previewImage.onerror = () => {
        console.error("Preview image failed to load:", chapter.previewImage);
    };

    previewImage.src = chapter.previewImage;
    previewImage.alt = chapter.title + " Preview";
    previewTitle.textContent = chapter.title;

    previewHint.textContent = "Click to explore this world ✧";

    // Update page counter
    pageCounter.textContent =
        `0${currentChapter + 1} / 0${chapters.length}`;

    // Update navigation buttons
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

    // Restart animation
    void storybook.offsetWidth;

    storybook.classList.add(
        direction > 0 ? "is-turning-next" : "is-turning-prev"
    );

    prevButton.disabled = true;
    nextButton.disabled = true;

    setTimeout(() => {
        currentChapter = nextIndex;

        renderChapter();

        storybook.classList.remove(
            "is-turning-next",
            "is-turning-prev"
        );

        isTurning = false;
    }, 750);
}


// Previous and Next buttons
nextButton.addEventListener("click", () => turnPage(1));
prevButton.addEventListener("click", () => turnPage(-1));


// Prevent entering a chapter while the page is turning
previewLink.addEventListener("click", (event) => {
    if (isTurning) {
        event.preventDefault();
    }
});


// Initial display
renderChapter();
console.log("Current chapter:", currentChapter);
console.log("Preview image:", previewImage.src);