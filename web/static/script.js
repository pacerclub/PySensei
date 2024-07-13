async function search() {
    const query = document.getElementById('query').value;
    const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
    const snippets = await response.json();
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    snippets.forEach(snippet => {
        const snippetDiv = document.createElement('div');
        snippetDiv.classList.add('snippet');
        snippetDiv.textContent = snippet.code.substring(0, 200);  // Display first 200 characters of code
        resultsDiv.appendChild(snippetDiv);
    });
}
