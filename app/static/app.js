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

    // Execute button logic
    executeBtn.addEventListener('click', async function () {
        const query = editor.getValue(); // Get value from CodeMirror
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
            const data = await response.json();

            console.log("Query results received:", data); // Debug log

            if (data.error) {
                resultsDiv.innerHTML = `<p class="error">${data.error}</p>`;
            } else {
                resultsDiv.innerHTML = formatResults(data.results);
            }
        } catch (error) {
            resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
        }
    });

    // Function to format results into an HTML table
    function formatResults(results) {
        if (results.length === 0) {
            return "<p>No results found.</p>";
        }

        let table = "<table><thead><tr>";
        const headers = Object.keys(results[0]);
        headers.forEach((header) => {
            table += `<th>${header}</th>`;
        });
        table += "</tr></thead><tbody>";

        results.forEach((row) => {
            table += "<tr>";
            headers.forEach((header) => {
                table += `<td>${row[header]?.value || ""}</td>`;
            });
            table += "</tr>";
        });

        table += "</tbody></table>";
        return table;
    }
});
