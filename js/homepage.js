
// The homepage uses a normal link to open book.html.
// This script adds a small visual response before navigation.

const bookLink = document.querySelector(".book-link");

bookLink.addEventListener("click", () => {
    bookLink.classList.add("opening");
});
