document.addEventListener('DOMContentLoaded', () => {
  const skillsList = document.getElementById('skillsList');
  const searchInput = document.getElementById('searchInput');
  const categorySelect = document.getElementById('categorySelect');

  // Extract unique categories and populate the select dropdown
  const categories = [...new Set(skillsData.map(skill => skill.category))].sort();
  categories.forEach(category => {
    const option = document.createElement('option');
    option.value = category;
    option.textContent = category;
    categorySelect.appendChild(option);
  });

  // Render list items based on current data
  function renderList(data) {
    skillsList.innerHTML = '';
    
    if (data.length === 0) {
      skillsList.innerHTML = '<p style="text-align: center; color: var(--text-secondary); width: 100%; padding: 2rem 0;">No skills found matching your criteria.</p>';
      return;
    }

    data.forEach((skill, index) => {
      const row = document.createElement('div');
      row.className = 'skill-row';
      // Stagger animation delay slightly for a cascading effect
      row.style.animationDelay = `${index * 0.02}s`;
      
      row.innerHTML = `
        <div class="skill-meta">
          <span class="skill-category">${skill.category}</span>
          <h2 class="skill-title" title="${skill.name}">${skill.name}</h2>
        </div>
        <p class="skill-description">${skill.description}</p>
        <a href="${skill.localPath}/SKILL.md" class="skill-link" target="_blank" rel="noopener noreferrer">View &rarr;</a>
      `;
      skillsList.appendChild(row);
    });
  }

  // Filter functionality
  function applyFilters() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = categorySelect.value;

    const filtered = skillsData.filter(skill => {
      const matchesSearch = skill.name.toLowerCase().includes(searchTerm) || 
                            skill.description.toLowerCase().includes(searchTerm);
      const matchesCategory = selectedCategory === 'All' || skill.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });

    renderList(filtered);
  }

  searchInput.addEventListener('input', applyFilters);
  categorySelect.addEventListener('change', applyFilters);

  // Initial render
  renderList(skillsData);
});
