document.addEventListener('DOMContentLoaded', function() {
    const queryTextarea = document.getElementById('sparql-query');
    const suggestionsDiv = document.getElementById('suggestions');
    const executeBtn = document.getElementById('execute-btn');
    let typingTimer;

    // Handle input in textarea
    queryTextarea.addEventListener('input', function() {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(() => getSuggestions(this.value), 300); // Debounce
    });

    // Get suggestions from Elasticsearch
    async function getSuggestions(text) {
        if (!text.trim()) {
            suggestionsDiv.innerHTML = '';
            return;
        }

        try {
            const response = await fetch(`/test?query=${encodeURIComponent(text)}`);
            const data = await response.json();
            
            if (data.elasticsearch_results && data.elasticsearch_results.length > 0) {
                displaySuggestions(data.elasticsearch_results);
            }
        } catch (error) {
            console.error('Error getting suggestions:', error);
        }
    }

    // Display suggestions
    function displaySuggestions(suggestions) {
        suggestionsDiv.innerHTML = suggestions
            .map(suggestion => `
                <div class="suggestion" onclick="insertSuggestion(${JSON.stringify(suggestion.query)})">
                    <pre>${suggestion.query}</pre>
                    <small>Score: ${suggestion.score}</small>
                </div>
            `)
            .join('');
    }

    // Handle query execution
    executeBtn.addEventListener('click', async function() {
        const query = queryTextarea.value;
        const resultsDiv = document.getElementById('results');

        try {
            const response = await fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ sparql_query: query })
            });
            const data = await response.json();
            
            if (data.error) {
                resultsDiv.innerHTML = `<p class="error">${data.error}</p>`;
            } else {
                resultsDiv.innerHTML = formatResults(data.results);
            }
        } catch (error) {
            resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
        }
    });
});

// Helper function to insert suggestion into textarea
function insertSuggestion(query) {
    document.getElementById('sparql-query').value = query;
    document.getElementById('suggestions').innerHTML = '';
}

// Add back the formatResults function
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
