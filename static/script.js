async function analyzeDocument() {
    const form = document.getElementById('analysisForm');
    const formData = new FormData(form);

    const response = await fetch('/analyze', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    if (data.error) {
        document.getElementById('errorMessage').innerText = data.error;
        document.getElementById('results').style.display = 'none'; // Hide results
    } else {
        document.getElementById('errorMessage').innerText = ''; // Clear error
        document.getElementById('results').style.display = 'block'; // Show results
        
        document.getElementById('wordCount').innerText = data.word_count;
        document.getElementById('sentenceCount').innerText = data.sentence_count;
        document.getElementById('complexity').innerText = data.complexity.toFixed(2);

        const translationTimesList = document.getElementById('translationTimes');
        translationTimesList.innerHTML = ''; // Clear previous times
        for (const language in data.translation_times) {
            const time = data.translation_times[language];
            const listItem = document.createElement('li');
            listItem.innerText = `${language}: ${time} hours`;
            translationTimesList.appendChild(listItem);
        }
    }
}