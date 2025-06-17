// Real-time search for members
if (document.getElementById('member-search')) {
    const memberSearch = document.getElementById('member-search');
    const memberResults = document.getElementById('member-results');

    memberSearch.addEventListener('input', function() {
        const query = this.value.trim();

        if (query.length < 2) {
            memberResults.innerHTML = '';
            memberResults.classList.add('d-none');
            return;
        }

        fetch(`/members/search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                memberResults.innerHTML = '';

                if (data.length === 0) {
                    memberResults.innerHTML = '<div class="dropdown-item">Talaba topilmadi</div>';
                    memberResults.classList.remove('d-none');
                    return;
                }

                data.forEach(member => {
                    const item = document.createElement('a');
                    item.className = 'dropdown-item';
                    item.href = '#';
                    item.innerHTML = `
                        <div>${member.first_name} ${member.last_name}</div>
                        <small class="text-muted">${member.student_id} | ${member.phone}</small>
                    `;
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        document.getElementById('id_member').value = member.id;
                        memberSearch.value = `${member.first_name} ${member.last_name}`;
                        memberResults.classList.add('d-none');
                    });
                    memberResults.appendChild(item);
                });

                memberResults.classList.remove('d-none');
            });
    });

    // Hide results when clicking outside
    document.addEventListener('click', function(e) {
        if (!memberSearch.contains(e.target) && !memberResults.contains(e.target)) {
            memberResults.classList.add('d-none');
        }
    });
}

// Auto-fill book details if book ID exists
if (document.getElementById('id_book_id')) {
    const bookIdField = document.getElementById('id_book_id');
    const bookTitleField = document.getElementById('id_book_title');

    // This would be replaced with actual API call in production
    bookIdField.addEventListener('change', function() {
        if (this.value.length > 3) {
            // Simulate API call to get book details
            setTimeout(() => {
                bookTitleField.value = `Kitob ${this.value} nomi`;
            }, 500);
        }
    });
}