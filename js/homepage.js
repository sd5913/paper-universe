
const worldCards = document.querySelectorAll(".world-card");

worldCards.forEach((card) => {

    card.addEventListener("click", () => {

        card.classList.add("selected");

    });

});
