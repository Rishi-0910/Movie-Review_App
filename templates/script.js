document.addEventListener('DOMContentLoaded', function ()
     {
        const reviewForm = document.getElementById('reviewForm');
        const reviewsList = document.getElementById('reviewsList');

         
        function fetchReviews() 
        {
            fetch('/api/reviews')
                .then(response => response.json())
                .then(reviews => 
                {
                    reviewsList.innerHTML = '';  
                    reviews.forEach(review => 
                    {
                        const reviewItem = document.createElement('li');
                        reviewItem.classList.add('review-item');
                        reviewItem.innerHTML = `<strong>${review.movieTitle}</strong> (Rating: ${review.rating})<br>${review.review}`;
                        reviewsList.appendChild(reviewItem);
                    });
                })
                .catch(error => console.error('Error fetching reviews:', error));
        }

         
        fetchReviews();

         
        reviewForm.addEventListener('submit', function (event) 
        {
            event.preventDefault();

            const movieTitle = document.getElementById('movieTitle').value;
            const rating = document.getElementById('rating').value;
            const review = document.getElementById('review').value;

            
            fetch('/api/reviews',
            {
                method: 'POST',
                headers: 
                {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify
                ({
                    movieTitle: movieTitle,
                    rating: rating,
                    review: review
                }),
            })
                .then(response => response.json())
                .then(data => 
                {
                    console.log('Success:', data);
                    
                    reviewForm.reset();
                    
                    fetchReviews();
                })
                .catch(error => console.error('Error submitting review:', error));
        });
    });