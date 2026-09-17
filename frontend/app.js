const analyzeButton =
    document.getElementById("analyzeButton");

const argumentInput =
    document.getElementById("argument");

const result =
    document.getElementById("result");

const loading =
    document.getElementById("loading");


analyzeButton.addEventListener(
    "click",
    analyzeArgument
);


async function analyzeArgument() {

    const text = argumentInput.value.trim();

    if (!text) {
        alert("Please enter an argument.");
        return;
    }


    loading.classList.remove("hidden");

    result.classList.add("hidden");

    analyzeButton.disabled = true;


    try {

        const response = await fetch(
            "http://127.0.0.1:8000/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: text
                })
            }
        );


        if (!response.ok) {
            throw new Error(
                "Server returned an error."
            );
        }


        const data = await response.json();


        document.getElementById("pratijna")
            .textContent = data.pratijna;

        document.getElementById("hetu")
            .textContent = data.hetu;

        document.getElementById("udaharana")
            .textContent = data.udaharana;

        document.getElementById("upanaya")
            .textContent = data.upanaya;

        document.getElementById("nigamana")
            .textContent = data.nigamana;

        document.getElementById("explanation")
            .textContent = data.explanation;

        document.getElementById("validity")
            .textContent =
                "Result: " + data.validity;


        result.classList.remove("hidden");

    }

    catch (error) {

        console.error(error);

        alert(
            "Something went wrong. " +
            "Make sure the backend is running."
        );

    }

    finally {

        loading.classList.add("hidden");

        analyzeButton.disabled = false;
    }
}