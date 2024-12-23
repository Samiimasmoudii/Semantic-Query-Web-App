document.getElementById("sparql-form").addEventListener("submit", async function (event) {
    event.preventDefault();
    const query = document.getElementById("sparql-query").value;
    const resultsDiv = document.getElementById("results");

    resultsDiv.innerHTML = "Executing query...";
    try {
        const response = await fetch("/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({ sparql_query: query })
        });
        const data = await response.json();
        if (data.error) {
            resultsDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            resultsDiv.innerHTML = formatResults(data.results);
        }
    } catch (err) {
        resultsDiv.innerHTML = `<p>Error: ${err.message}</p>`;
    }
});

function formatResults(results) {
    if (results.length === 0) {
        return "<p>No results found.</p>";
    }

    let table = "<table><thead><tr>";
    const headers = Object.keys(results[0]);
    headers.forEach(header => {
        table += `<th>${header}</th>`;
    });
    table += "</tr></thead><tbody>";

    results.forEach(row => {
        table += "<tr>";
        headers.forEach(header => {
            table += `<td>${row[header]?.value || ""}</td>`;
        });
        table += "</tr>";
    });

    table += "</tbody></table>";
    return table;
}
