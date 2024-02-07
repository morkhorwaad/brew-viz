from marshmallow import Schema, fields

class UntappdBreweryRatingSchema(Schema): 
    count = fields.Int()
    rating_score = fields.Float()
    
class UntappdBreweryLocationSchema(Schema):
    brewery_address = fields.Str()
    brewery_city = fields.Str()
    brewery_lat = fields.Float()
    brewery_lng = fields.Float()
    
class UntappdBrewerySchema(Schema): 
    brewery_id = fields.Int()
    brewery_name = fields.Str()
    brewery_in_production = fields.Bool()
    is_independent = fields.Bool()
    beer_count = fields.Int()
    brewery_type = fields.Str()
    rating = fields.Nested(UntappdBreweryRatingSchema)
    brewery_description = fields.Str()
    location = fields.Nested(UntappdBreweryLocationSchema)
    
class UntappdBeerSchema(Schema): 
    brewery_id = fields.Int(missing=-1)
    beer_id = fields.Int()
    beer_name = fields.Str()
    beer_style = fields.Str()
    beer_ibu = fields.Int()
    beer_abv = fields.Int()
    created_at = fields.DateTime()
    rating_score = fields.Float()
    rating_count = fields.Int()
    total_count = fields.Int() 