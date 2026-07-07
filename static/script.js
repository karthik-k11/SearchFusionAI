document.addEventListener("DOMContentLoaded", () => {

    const uploadInput = document.querySelector('input[type="file"]');
    const searchInput = document.querySelector('input[name="query"]');
    const developerPanel = document.querySelector("details");


    if (uploadInput) {

        uploadInput.addEventListener("change", function () {

            if (this.files.length > 0) {

                console.log("Selected File:", this.files[0].name);

            }

        });

    }


    const searchForm = document.querySelector(".search-form");

    if (searchForm) {

        searchForm.addEventListener("submit", function (event) {

            const query = searchInput.value.trim();

            if (query === "") {

                event.preventDefault();

                alert("Please enter a keyword to search.");

                searchInput.focus();

            }

        });

    }


    if (searchInput) {

        searchInput.addEventListener("keydown", function (event) {

            if (event.key === "Escape") {

                searchInput.value = "";

            }

        });

    }


    if (developerPanel) {

        developerPanel.open = false;

    }

    console.log("SearchFusionAI Ready");

});