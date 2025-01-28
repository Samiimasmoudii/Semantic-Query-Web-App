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

    console.log("CodeMirror initialized.");

    // Function to fetch suggestions
    async function getSuggestions(text) {
        if (!text.trim()) {
            suggestionsDiv.innerHTML = '';
            return;
        }

        try {
            const response = await fetch(`/test?query=${encodeURIComponent(text)}`);
            const data = await response.json();

            if (data.elasticsearch_results?.length > 0) {
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
        if (!document.activeElement || document.activeElement !== editor.getInputField()) return;

        suggestionsDiv.innerHTML = suggestions.map(suggestion => {
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
        }).join('');

        // Add click handlers to suggestions
        document.querySelectorAll('.suggestion').forEach(suggestionDiv => {
            suggestionDiv.addEventListener('click', function () {
                const query = this.getAttribute('data-query');
                editor.setValue(query);
                suggestionsDiv.innerHTML = '';
            });
        });
    }

    // Monitor changes in CodeMirror editor
    editor.on('change', function (instance) {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(() => {
            getSuggestions(instance.getValue());
        }, 100);
    });

    // Execute button logic
    // In the execute button handler
    executeBtn.addEventListener('click', async function () {
        // Get the raw query from the editor
        const rawQuery = editor.getValue();
        const resultsDiv = document.getElementById('results');

        // Add required prefixes
        const fullQuery = `
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX dbp: <http://dbpedia.org/property/>
        ${rawQuery}
    `;

        console.log("Executing query:", fullQuery);

        try {
            const response = await fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ sparql_query: fullQuery }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Enhanced error handling
            if (data.error) {
                resultsDiv.innerHTML = `<div class="alert alert-danger">
                <strong>Error:</strong> ${data.error}
                ${data.details ? `<br>Details: ${data.details}` : ''}
            </div>`;
            } else {
                resultsDiv.innerHTML = formatResults(data.results);
            }
        } catch (error) {
            resultsDiv.innerHTML = `<div class="alert alert-danger">
            <strong>Network Error:</strong> ${error.message}
        </div>`;
            console.error("Execution error:", error);
        }
    });

    // Function to format results
    function formatResults(results) {
        if (results.length === 0) return "<p>No results found.</p>";

        let table = "<table><thead><tr>";
        const headers = Object.keys(results[0]);
        headers.forEach(header => table += `<th>${header}</th>`);
        table += "</tr></thead><tbody>";

        results.forEach(row => {
            table += "<tr>";
            headers.forEach(header => table += `<td>${row[header]?.value || ""}</td>`);
            table += "</tr>";
        });

        return table + "</tbody></table>";
    }

    // Load previous queries
    (async () => {
        try {
            const response = await fetch('/previous-queries');
            const queries = await response.json();
            const previousQueriesDiv = document.getElementById('previous-queries');

            queries.forEach(query => {
                const queryElement = document.createElement('a');
                queryElement.href = '#';
                queryElement.className = 'list-group-item list-group-item-action';
                queryElement.textContent = query;

                // Add click handler to populate editor
                queryElement.addEventListener('click', (e) => {
                    e.preventDefault();
                    editor.setValue(query);
                });

                previousQueriesDiv.appendChild(queryElement);
            });
        } catch (error) {
            console.error('Error loading previous queries:', error);
        }
    })();
});