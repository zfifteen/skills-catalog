document.addEventListener('DOMContentLoaded', () => {
  const skillsGrid = document.getElementById('skillsGrid');
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

  // Render cards based on current data
  function renderCards(data) {
    skillsGrid.innerHTML = '';
    
    if (data.length === 0) {
      skillsGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-secondary);">No skills found matching your criteria.</p>';
      return;
    }

    data.forEach((skill, index) => {
      const card = document.createElement('div');
      card.className = 'skill-card';
      // Stagger animation delay slightly for a cascading effect
      card.style.animationDelay = `${index * 0.05}s`;
      
      card.innerHTML = `
        <div class="skill-header">
          <h2 class="skill-title">${skill.name}</h2>
          <span class="skill-category">${skill.category}</span>
        </div>
        <p class="skill-description">${skill.description}</p>
        <a href="${skill.localPath}/SKILL.md" class="skill-link" target="_blank" rel="noopener noreferrer">View Skill Path &rarr;</a>
      `;
      skillsGrid.appendChild(card);
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

    renderCards(filtered);
  }

  searchInput.addEventListener('input', applyFilters);
  categorySelect.addEventListener('change', applyFilters);

  // Initial render
  renderCards(skillsData);
});
