document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const questionId = this.dataset.id;
            const likeIcon = this.querySelector('.like-icon');
            const countElement = this.querySelector('.likes-count');

            if (this.classList.contains('active')) {
                this.classList.remove('active');
                countElement.textContent = parseInt(countElement.textContent) - 1;
            } else {
                this.classList.add('active');
                countElement.textContent = parseInt(countElement.textContent) + 1;

                likeIcon.style.transform = 'scale(1.3)';
                setTimeout(() => {
                    likeIcon.style.transform = 'scale(1)';
                }, 300);
            }

            updateLikeOnServer(questionId, this.classList.contains('active'));
        });
    });

    function updateLikeOnServer(questionId, isLiked) {
        fetch(`/api/questions/${questionId}/like/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                liked: isLiked
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Like updated successfully');
            if (data.likes_count !== undefined) {
                const button = document.querySelector(`.like-btn[data-id="${questionId}"]`);
                const countElement = button.querySelector('.likes-count');
                countElement.textContent = data.likes_count;
            }
        })
        .catch(error => {
            console.error('Error updating like:', error);
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});