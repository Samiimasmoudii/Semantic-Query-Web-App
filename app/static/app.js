document.addEventListener('DOMContentLoaded', function () {
    const suggestionsDiv = document.getElementById('suggestions');
    const executeBtn = document.getElementById('execute-btn');
    let typingTimer;

    // Initialize CodeMirror
    const editor = CodeMirror.fromTextArea(document.getElementById('sparql-query'), {
        mode: "sparql",
        lineNumbers: true,
        theme: "default",
        matchBrackets: true,
    });


    console.log("CodeMirror initialized."); // Debug log

    // Function to fetch suggestions
    async function getSuggestions(text) {
        console.log("Fetching suggestions for query:", text); // Debug log

        if (!text.trim()) {
            suggestionsDiv.innerHTML = '';
            return;
        }

        try {
            const response = await fetch(`/test?query=${encodeURIComponent(text)}`);
            const data = await response.json();

            console.log("Suggestions data received:", data); // Debug log

            if (data.elasticsearch_results && data.elasticsearch_results.length > 0) {
                displaySuggestions(data.elasticsearch_results);
            } else {
                suggestionsDiv.innerHTML = "<p>No suggestions available.</p>";
            }
        } catch (error) {
            console.error("Error getting suggestions:", error);
        }
    }

    // Function to display suggestions
    function displaySuggestions(suggestions) {
        if (!document.activeElement || document.activeElement !== editor.getInputField()) {
            return;
        }
        console.log("Displaying suggestions:", suggestions); // Debug log

        suggestionsDiv.innerHTML = suggestions
            .map((suggestion) => {
                const escapedQuery = suggestion.query
                    .replace(/&/g, '&amp;')
                    .replace(/'/g, '&#39;')
                    .replace(/"/g, '&quot;');

                return `
                    <div class="suggestion" data-query="${escapedQuery}">
                        <pre>${suggestion.query}</pre>
                        <small>Score: ${suggestion.score}</small>
                    </div>
                `;
            })
            .join('');

        // Add click handlers to suggestions
        document.querySelectorAll('.suggestion').forEach((suggestionDiv) => {
            suggestionDiv.addEventListener('click', function () {
                const query = this.getAttribute('data-query');
                editor.setValue(query); // Update CodeMirror content with the selected suggestion
                suggestionsDiv.innerHTML = '';
            });
        });
    }

    // Monitor changes in CodeMirror editor
    editor.on('change', function (instance) {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(() => {
            const query = instance.getValue();
            console.log("Query change detected:", query); // Debug log
            getSuggestions(query); // Fetch suggestions for current query
        }, 100);
    });

    executeBtn.addEventListener('click', async function () {
        const query = editor.getValue();
        const resultsDiv = document.getElementById('results');

        console.log("Executing query:", query); // Debug log

        try {
            const response = await fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ sparql_query: query }),
            });

            const text = await response.text();  // Get raw response
            console.log("Raw response:", text);  // Debug log

            try {
                const data = JSON.parse(text);  // Try to parse as JSON
                console.log("Parsed JSON response:", data);

                if (data.error) {
                    resultsDiv.innerHTML = `<p class="error">${data.error}</p>`;
                } else {
                    resultsDiv.innerHTML = formatResults(data.results);
                }
            } catch (jsonError) {
                resultsDiv.innerHTML = `<p class="error">Unexpected response format</p>`;
                console.error("JSON Parsing Error:", jsonError);
            }

        } catch (error) {
            resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
        }
    });
    function formatResults(data) {
        // Check if the API response has the expected structure
        if (!data.results || !data.results.bindings) {
            console.error("Invalid response format:", data);
            return "<p>Error: Unexpected response format.</p>";
        }
    
        let bindings = data.results.bindings;
    
        if (bindings.length === 0) {
            return "<p>No results found.</p>";
        }
    
        let table = "<table style='border-collapse: collapse; width: 100%; text-align: left;' border='1'>";
        table += "<thead><tr>";
    
        // Extract headers dynamically
        const headers = Object.keys(bindings[0]);
        headers.forEach((header) => {
            table += `<th style="padding: 8px; background-color: #f2f2f2;">${header}</th>`;
        });
    
        table += "</tr></thead><tbody>";
    
        // Populate table rows
        bindings.forEach((row) => {
            table += "<tr>";
            headers.forEach((header) => {
                let value = row[header]?.value || "";
                // Remove links by extracting the last part of the URI
                if (value.startsWith("http://") || value.startsWith("https://")) {
                    value = value.split("/").pop().replace(/_/g, " "); // Keep only the readable part
                }
                table += `<td style="padding: 8px;">${value}</td>`;
            });
            table += "</tr>";
        });
    
        table += "</tbody></table>";
        return table;
    }
    
});
document.getElementById('logout-btn').addEventListener('click', function() {
    // Redirect to logout route or perform logout action
    window.location.href = '/logout'; // Example redirect
});

document.addEventListener('DOMContentLoaded', async () => {


    const response = await fetch('/previous-queries');
    const queries = await response.json();
    const previousQueriesDiv = document.getElementById('previous-queries');
    queries.forEach(query => {
        const queryElement = document.createElement('a');
        queryElement.href = '#';
        queryElement.className = 'list-group-item list-group-item-action';
        queryElement.textContent = query;
        previousQueriesDiv.appendChild(queryElement);
    });
});