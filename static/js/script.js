document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // DARK MODE
    // =========================

    const darkBtn = document.getElementById("darkModeBtn");

    if (darkBtn) {

        darkBtn.addEventListener("click", function () {

            document.body.classList.toggle("dark-mode");

        });

    }

    // =========================
    // SEARCH
    // =========================

    const searchInput = document.getElementById("searchInput");

    if (searchInput) {

        searchInput.addEventListener("keyup", function () {

            const filter = searchInput.value.toLowerCase();

            const rows = document.querySelectorAll(
                "#expenseTable tbody tr"
            );

            rows.forEach((row) => {

                const text = row.innerText.toLowerCase();

                if (text.includes(filter)) {

                    row.style.display = "";

                } else {

                    row.style.display = "none";

                }

            });

        });

    }

    // =========================
    // CHART
    // =========================

    const ctx = document.getElementById("expenseChart");

    if (
        ctx &&
        window.chartLabels &&
        window.chartAmounts
    ) {

        new Chart(ctx, {

            type: "bar",

            data: {

                labels: window.chartLabels,

                datasets: [{

                    label: "Expenses By Category",

                    data: window.chartAmounts,

                    backgroundColor: [

                        "#4facfe",
                        "#43e97b",
                        "#fa709a",
                        "#f6d365",
                        "#a18cd1",
                        "#ff9a9e",
                        "#667eea",
                        "#00c9ff",
                        "#92fe9d"

                    ],

                    borderRadius: 10

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        display: true

                    }

                },

                scales: {

                    y: {

                        beginAtZero: true

                    }

                }

            }

        });

    }

});