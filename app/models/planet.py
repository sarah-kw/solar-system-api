from app import db

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    planet_name = db.Column(db.String)
    description = db.Column(db.String)
    dist_from_star_km = db.Column(db.Integer)

    def make_dict(self):
        planet_dict = {
            "id": self.id,
            "planet_name": self.planet_name,
            "description": self.description,
            "dist_from_star_km": self.dist_from_star_km
            }
        return planet_dict
