from db.entities.reviews import Reviews


class CalculateRatingService:
    
    @staticmethod
    def calculate_rating(reviews: list[Reviews]) -> float:
        if len(reviews) < 20:
            return 0.0
        
        return sum([review.calificacion for review in reviews if review.calificacion is not None]) / len(reviews)