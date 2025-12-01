document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function() {
            const type = this.dataset.type; // 'question' или 'answer'
            const id = this.dataset.id;
            const likesCount = this.querySelector('.likes-count');

            this.classList.toggle('active');


            let currentCount = parseInt(likesCount.textContent);
            if (this.classList.contains('active')) {
                likesCount.textContent = currentCount + 1;
            } else {
                likesCount.textContent = currentCount - 1;
            }

            this.style.transform = 'scale(1.1)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);

            // sendLikeToServer(type, id, this.classList.contains('active'));
        });
    });
});


function sendLikeToServer(type, id, isLiked) {
    console.log(`${isLiked ? 'Лайкнул' : 'Убрал лайк'} ${type} с ID: ${id}`);
    /*
    fetch('/api/like/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            type: type,
            id: id,
            action: isLiked ? 'like' : 'unlike'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            // Откатываем изменения если ошибка
        }
    });
    */
}